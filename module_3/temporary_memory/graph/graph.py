from agent.utils import SummaryState
from .nodes import agent_node, summarize_conversation, should_continue

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, END

# Create the workflow
workflow = StateGraph(SummaryState)

# Add nodes
workflow.add_node("agent", agent_node)
workflow.add_node("summarize_conversation", summarize_conversation)

# Add edges
workflow.add_edge(START, "agent")
workflow.add_conditional_edges(
    "agent", 
    should_continue,
    {
        "summarize_conversation": "summarize_conversation",
        END: END
    }
)
workflow.add_edge("summarize_conversation", END)

# Add memory
# memory = MemorySaver()

# Compile the graph
graph = workflow.compile()