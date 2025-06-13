import os
from dotenv import load_dotenv
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI
from tools.weather_tool import get_weather
from tools.attraction_tool import get_attractions

load_dotenv()

# Gemini LLM setup
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.7
)

# Tools
tools = [get_weather, get_attractions]

# Prompt Template: must include input and agent_scratchpad
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful travel assistant that provides weather and top tourist attractions."),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad")
])

# Create agent
agent = create_tool_calling_agent(
    llm=llm,
    tools=tools,
    prompt=prompt
)

# Agent executor
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Function to call agent
def run_travel_assistant(city: str) -> str:
    user_prompt = f"Give me the current weather and top tourist attractions in {city}."
    result = agent_executor.invoke({"input": user_prompt})
    return result["output"]
