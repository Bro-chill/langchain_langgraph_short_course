import sqlite3
from agent.utils import SummaryState
from .nodes import agent_node, summarize_conversation, should_continue

from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
from langgraph.graph import StateGraph, START, END

# Initialize memory
db_path = "database/example.db"
conn = sqlite3.connect(db_path, check_same_thread=False)
memory = SqliteSaver(conn)

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

# Compile the graph
graph = workflow.compile(checkpointer=memory)