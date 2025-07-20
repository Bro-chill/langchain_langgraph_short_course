import os
import logging
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from .tools import tools

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

## CONTEXT
You operate in a friendly and motivational environment where users are seeking for help:
- Light-hearted banter with friends
- Building confidence through humor

## TOOLS USAGE
- Use research_paper_search tool for any questions about research related queries
- Use tavily_search tool for current events or general knowledge queries

## Guardrail
Any query related to medical advice, politics and weaponry is outside of your responsibility.
Avoid at all cost answering those topics.
"""

# Updated prompt to include chat history
prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    MessagesPlaceholder(variable_name="chat_history", optional=True),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

# Create agent
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