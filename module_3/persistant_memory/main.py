import asyncio
from langchain_core.messages import HumanMessage
from graph.graph import graph
from agent.utils import SummaryState

async def chat_session():
    config = {"configurable": {"thread_id": "conversation-1"}}
    print("🤖 AI Trash Talker is ready! Type 'quit' to exit.")
    
    while True:
        user_input = input("\n👤 You: ")
        
        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("👋 See ya later! Don't let the door hit you on the way out!")
            break
            
        try:
            # Just pass the new message, let the graph handle state
            result = graph.invoke(
                {"messages": [HumanMessage(content=user_input)]}, 
                config=config
            )
            
            if result["messages"]:
                bot_response = result["messages"][-1].content
                print(f"\n🤖 Bot: {bot_response}")
                
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(chat_session())