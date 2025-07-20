### module-2
Fundamental on Agentic RAG Chatbot.
In this module we will provide 2 tools for our agent.

**@tool**
tavily_search = this tool will be use by our agent to search latest data on internet as each llm have their training data cut off data.

**@tool**
personal_data = this tool will be use by our agent to search our personal data such as faq. We will store our data in VectorDB(MongoDB).

---

### Files Structure
```

📁 module_2
│
├── 💾 mongodb_setup/
│    ├── faq.pdf            # personal data
│    ├── add_data.py        # create database folder
│    └── create_db.py       # add personal data into database
│
├── 🤖 agent_chatbot.py     # Initialize agent
│
├── 🔧 tools.py             # Initialize tools for agent
│
└── 🌐 utils.py             # Initialize schemas and dependencies
```
---

