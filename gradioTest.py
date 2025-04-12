import gradio as gr
from temporaryGeekedChatbot import news_agent
from temporaryGeekedChatbot import Deps
from temporaryGeekedChatbot import NEWS_API_KEY
import asyncio
from httpx import AsyncClient

client = AsyncClient()
deps: Deps = Deps(client = client, news_api_key=NEWS_API_KEY)


# def test(message, history):
#     if message.endswith("?"):
#         return "Fuck"
#     else:
#         return "Ok man"
    
# async def process_prompt(message, history):
#     result = await news_agent.run(message, deps=deps)
#     return "false" if len(result.data.articles) == 0 else result.data.articles[0]

async def process_prompt(message, history):
    result = await news_agent.run(message, deps=deps)
    return "Sorry, the message resulted either in 0 articles or was unrelated/malformed" if len(result.data.articles) == 0 else result.data.articles[0].title

gr.ChatInterface(
    fn = process_prompt,
    type="messages"
).launch()