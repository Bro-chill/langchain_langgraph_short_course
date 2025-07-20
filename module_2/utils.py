from dataclasses import dataclass
from pydantic import BaseModel

from langchain_google_genai import ChatGoogleGenerativeAI

# Initialize Schemas
class ChatMessage(BaseModel):
    """Defines what a single chat message should contain"""
    content: str    # Query/Reply
    sender: str     # user/bot

# Initialize dependencies
@dataclass
class AgentDeps:
    """Dependencies for agent"""
    llm: ChatGoogleGenerativeAI  # Bot Brain
    system_prompt: str           # Persona, Task, Context, Tools Usage and Guardrail
