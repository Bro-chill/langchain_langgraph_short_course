### AI Agent Course

This course is design to get familiar with langchain and langgraph stack to build agentic application.

---

| |LangChain|LangGraph|
|---------|---------|---------|
|**Functionality**|Toolkit to build AI application|Agent Orchestrator|
|**Evaluator**|LangFuse|LangSmith|

---

### Modules Summary

* **module_1**: Chatbot
* **module_2**: Agent Chatbot + Tool(Agentic RAG)
* **module_3**: Agent Chatbot + Memory(Temporary + Persistant)

---

### How to start

1. **Create & activate virtual environment ( > Python3.11.9)**
```
python -m venv myvenv
cd myvenv\Scripts\activate
```
2. **Install requirements.txt**
```
pip install -r requirements.txt
```

---


3. **Create .env**
```
# Gemini LLM (https://ai.google.dev/gemini-api)
GEMINI_KEY=
MODEL_CHOICE=gemini-2.0-flash

# Tavily (https://app.tavily.com/home)
TAVILY_API_KEY=

# MongoDB
MONGODB_ATLAS_CLUSTER_URI=
MONGODB_DB_NAME=
MONGODB_COLLECTION_NAME=
```