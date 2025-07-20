from agent.chatbot_agent import llm, agent_executor
from agent.utils import SummaryState

from langchain_core.messages import HumanMessage, AIMessage, RemoveMessage

from langgraph.graph import END

def agent_node(state: SummaryState):
    """Execute the agent with the current state"""
    # Get the last message from the user
    last_message = state["messages"][-1]
    
    # Execute the agent
    result = agent_executor.invoke({
        "input": last_message.content,
        "chat_history": state["messages"][:-1]  # All messages except the last one
    })
    
    # Return the agent's response as an AIMessage
    return {"messages": [AIMessage(content=result["output"])]}

def summarize_conversation(state: SummaryState):
    """Summarize the conversation and remove old messages"""
    summary = state.get("summary", "")

    if summary:
        summary_message = (
            f"Conversation summary: {summary}\n\n"
            "Extend the summary by taking into account the new messages above:"
        )
    else:
        summary_message = "Create a summary of the conversation above:"

    messages = state["messages"] + [HumanMessage(content=summary_message)]
    response = llm.invoke(messages)

    # Keep only the last 6 messages and remove the rest
    delete_messages = [RemoveMessage(id=m.id) for m in state["messages"][:-6]]
    return {"summary": response.content, "messages": delete_messages}

def should_continue(state: SummaryState):
    """Determine whether to continue or summarize"""
    messages = state["messages"]
    
    # If we have more than 6 messages, summarize
    if len(messages) > 6:
        return "summarize_conversation"
    
    return END