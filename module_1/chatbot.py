import os
from dotenv import load_dotenv
from dataclasses import dataclass
from typing import List
from pydantic import BaseModel

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage

# Initialize LLM
load_dotenv()
api_key = os.getenv('GEMINI_KEY')
model = os.getenv('MODEL_CHOICE')

llm = ChatGoogleGenerativeAI(
    model=model,
    api_key=api_key,
    temperature=0
)

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
    system_prompt: str           # Persona, Task, Context and Guardrail

system_prompt = """
## PERSONA
You are professional AI trash talker.

## TASK
Your primary job is to answer user query and roast them to the bone.

## CONTEXT
You operate in a friendly and motivational environment where users are seeking for help:
- Light-hearted banter with friends
- Gaming sessions and competitive activities
- Building confidence through humor

## Guardrail
Any query related to medical advice, politics and weaponry is outside of your responsibility.
Avoid at all cost answering those topics.
"""

# chatbot function
def chatbot(user_message: ChatMessage, deps: AgentDeps) -> ChatMessage:
    """Function to interact with the agent"""
    messages = [
        SystemMessage(content=deps.system_prompt),
        HumanMessage(content=user_message.content)
    ]
    
    response = deps.llm.invoke(messages)
    return ChatMessage(content=response.content, sender="bot")

# helper function
if __name__ == "__main__":

    deps = AgentDeps(llm=llm, system_prompt=system_prompt)
    
    print("🔥 Roast Master initialized! Type 'quit' to exit.")
    
    while True:
        user_input = input("\nYou: ")
        
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("🔥 Roast Master signing off! Keep those burns legendary! 🔥")
            break
            
        try:
            user_message = ChatMessage(content=user_input, sender="user")
            response = chatbot(user_message, deps)
            print(f"\nBot: {response.content}")
        except Exception as e:
            print(f"Error: {e}")