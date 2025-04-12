from dataclasses import dataclass
from pydantic_ai import Agent, RunContext
import os
from httpx import AsyncClient
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List, Optional
import asyncio

load_dotenv()

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
GEO_API_KEY = os.getenv('GEO_API_KEY')
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
NEWS_API_KEY = os.getenv('NEWS_API_KEY')

os.environ["GEMINI_API_KEY"] = GOOGLE_API_KEY
os.environ["GEO_API_KEY"] = GEO_API_KEY
os.environ['WEATHER_API_KEY'] = WEATHER_API_KEY
os.environ["NEWS_API_KEY"] = NEWS_API_KEY

@dataclass
class Deps:
    news_api_key: str | None
    client: AsyncClient

# Pydantic news api response obj
class Source(BaseModel):
    id: Optional[str]
    name: str

class Article(BaseModel):
    source: Source
    author: Optional[str]
    title: str
    description: Optional[str]
    publishedAt: str
    content: Optional[str]

class NewsAPIResponse(BaseModel):
    articles: List[Article]

def checkIfNewsResponseEmpty(response: NewsAPIResponse) -> bool:
    return not response.articles # empty list ret T else F

'''
Be  concise, reply with one sentence
use the `get_top_headlines_country` tool when user prompts what country to search news in

Top headlines for request country
Top headlines for category
Top headlines for certain query


Function for add to daily digest preferences

'''

# Agent singleton
news_agent = Agent(
    "google-gla:gemini-2.0-flash",
    system_prompt=('Be concise, reply with one sentence.'
        'use the `get_top_headlines_country` tool when user prompts what country to search news in'
        'use the `get_top_headlines_source` tool when user prompts what news source name to search news in'
        'use the `get_top_headlines_query` tool when user prompts a simple keyword query to search for news in'
        'be careful to convert country to 2-letter ISO 3166-1 code and if not recognized throw error'),
    result_type=NewsAPIResponse,
    deps_type=Deps,
    retries=3,
)


@news_agent.tool
async def get_top_headlines_country(ctx: RunContext[Deps], country: str) -> NewsAPIResponse:

    # Http arguement params
    # makesure arguement var names match api ones
    params = {
        'country': country.lower(),
        'apikey': ctx.deps.news_api_key,
        'pageSize': 3,
    }

    response = await ctx.deps.client.get("https://newsapi.org/v2/top-headlines", params=params)
    response.raise_for_status() # Auto raise exe if bad err code
    response_data = NewsAPIResponse.model_validate(response.json())

    return response_data

@news_agent.tool
async def get_top_headlines_source(ctx: RunContext[Deps], source: str) -> NewsAPIResponse:
    # Http arguement params
    # makesure arguement var names match api ones
    params = {
        'apikey': ctx.deps.news_api_key,
        'pageSize': 3,
        'sources': source
    }

    response = await ctx.deps.client.get("https://newsapi.org/v2/top-headlines", params=params)
    response.raise_for_status() # Auto raise exe if bad err code
    response_data = NewsAPIResponse.model_validate(response.json())

    return response_data
    


@news_agent.tool
async def get_top_headlines_query(ctx: RunContext[Deps], query: str) -> NewsAPIResponse:

    # Http arguement params
    # makesure arguement var names match api ones
    params = {
        'apikey': ctx.deps.news_api_key,
        'pageSize': 3,
        'q': query
    }

    response = await ctx.deps.client.get("https://newsapi.org/v2/top-headlines", params=params)
    response.raise_for_status() # Auto raise exe if bad err code
    response_data = NewsAPIResponse.model_validate(response.json())

    return response_data

async def main():
    async with AsyncClient() as client:
        deps: Deps = Deps(client = client, news_api_key=NEWS_API_KEY) # @Dataclass is shrot had for a class so need to use class as constructor
        result = await news_agent.run('What is the current top headlines about cars?', deps=deps) # agent run alawys needs the dependencies
        print(type(result.data))
        print(result.data.articles[0])
        
if __name__ == "__main__":
    asyncio.run(main())