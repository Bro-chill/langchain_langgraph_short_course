from dataclasses import dataclass
from pydantic import BaseModel

from langchain_google_genai import ChatGoogleGenerativeAI

from langgraph.graph import MessagesState

# Initialize Schemas
class ChatMessage(BaseModel):
    """Defines what a single chat message should contain"""
    content: str    # Query/Reply
    sender: str     # user/bot

class SummaryState(MessagesState):
    summary: str

# Initialize dependencies
@dataclass
class AgentDeps:
    """Dependencies for agent"""
    llm: ChatGoogleGenerativeAI  # Bot Brain
    system_prompt: str           # Persona, Task, Context, Tools Usage and Guardrail
