from pydantic_ai import Agent, RunContext
import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
GEO_API_KEY = os.getenv('GEO_API_KEY')
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')

os.environ["GEMINI_API_KEY"] = GOOGLE_API_KEY
os.environ["GEO_API_KEY"] = GEO_API_KEY
os.environ['WEATHER_API_KEY'] = WEATHER_API_KEY


# agent = Agent(
#     "google-gla:gemini-2.0-flash",
#     system_prompt='Be concise, reply with one sentence.',
# )

'''
Note:

About system prompts:
There can be dynamic and static
the static one is in constructor of agent
the dyanmic one is at runtime and should be defiend via functions decorated with @agent.system_prompt

Dynamic system prompt defined via a decorator with RunContext, this is called just after run_sync, not when the agent is created, so can benefit from runtime information like the dependencies used on that run.

'''
agent = Agent(
    "google-gla:gemini-2.0-flash",
    system_prompt='Use the `test` function to see if the `user` has guessed correct number but respond in sentence ',
    deps_type=int
)


# RunContext is a container that provides contextual info to dependencies during a funciton execution
# The thing inside run context is the agent dependent type as defined in agent decl
@agent.tool
async def test(ctx: RunContext[int], number: int) -> str:
    return 'winner' if number == ctx.deps else 'loser'

# result = agent.run_sync('ok man')  
# print(result.data)

result = agent.run_sync('I want to choose 33', deps=18) # returns RunResult
print(result.data)
print(result.usage())
