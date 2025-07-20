## temporary_memory

Where conversation history is stored in **MemorySaver()**.
Once logout from conversation, all the history is wipe out.

### File Structure
```
📁 temporary_memory
│
├── 🤖 agent/
│    ├── chatbot_agent.py # where llm is initialize and agent + tools is compiled
│    ├── tools.py         # initialize tools
│    └── utils.py         # initialize schemas and dependencies
│
├── 🔗 graph/
│    ├── graph.py         # workflow from start to end
│    └── nodes.py         # building blocks
│
└── 🧠 main.py               # helper function to run chatbot
```

---
## persistant_memory

Where conversation is summarize and store in db.
Next conversation will retrieve the summary before continue the conversation.

### File Structure
```
📁 persistant_memory
│
├── 🤖 agent/
│    ├── chatbot_agent.py # where llm is initialize and agent + tools is compiled
│    ├── tools.py         # initialize tools
│    └── utils.py         # initialize schemas and dependencies
│
├── 🔗 graph/
│    ├── graph.py         # workflow from start to end
│    └── nodes.py         # building blocks
│
├── 💾 database/
│    └── example.db       # example database. Replace with cloud db for production.
└── 🧠 main.py               # helper function to run chatbot
```