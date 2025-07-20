import os
import logging
from dotenv import load_dotenv
from dataclasses import dataclass
from typing import List
from pydantic import BaseModel

from pymongo import MongoClient

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_tool_calling_agent, tool
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.tools.tavily_search import TavilySearchResults

from tools import tools
from utils import ChatMessage, AgentDeps

logger = logging.getLogger(__name__)

# Initialize .env
load_dotenv()
api_key = os.getenv('GEMINI_KEY')
model = os.getenv('MODEL_CHOICE')

llm = ChatGoogleGenerativeAI(
    model=model,
    api_key=api_key,
    temperature=0
)

system_prompt = """
## PERSONA
You are professional AI trash talker.

## TASK
Your primary job is to answer user query and roast them to the bone.
When users ask personal questions about you (like your name, preferences, etc.), 
ALWAYS use the personal_data tool first to get accurate information, then incorporate that into your roasted response.

## CONTEXT
You operate in a friendly and motivational environment where users are seeking for help:
- Light-hearted banter with friends
- Gaming sessions and competitive activities
- Building confidence through humor

## TOOLS USAGE
- Use personal_data tool for any questions about personal information, identity, preferences, or FAQ
- Use tavily_search tool for current events, general knowledge, or research queries

## Guardrail
Any query related to medical advice, politics and weaponry is outside of your responsibility.
Avoid at all cost answering those topics.
"""

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

# FIXED: Use proper prompt template
agent = create_tool_calling_agent(
    llm=llm,
    tools=tools,
    prompt=prompt
)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    max_iterations=5
)

def chatbot_agent(user_message: ChatMessage, deps: AgentDeps) -> ChatMessage:
    """Function to interact with the agent"""
    
    # FIXED: Use agent_executor instead of deps.llm
    response = agent_executor.invoke({"input": user_message.content})
    
    return ChatMessage(content=response["output"], sender="bot")

if __name__ == "__main__":
    
    deps = AgentDeps(llm=llm, system_prompt=system_prompt)

    print("Agentic Bot initialized! Type 'quit' to exit")

    while True:
        user_input = input("\nYou: ")

        if user_input.lower() in ['quit', 'exit', 'q']:
            print("Agentic bot signing off!")
            break
        
        try:
            user_message = ChatMessage(content=user_input, sender="user")
            response = chatbot_agent(user_message=user_message, deps=deps)
            print(f"\nBot: {response.content}")

        except Exception as e:
            print(f"Error: {e}")