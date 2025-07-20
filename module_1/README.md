### module_1 summary
Fundamental on building chatbot.

---

### Breakdown

1. **Initialize LLM**: LLM settings
2. **Initialize Schemas**: Validate and Standardize Data. Type safety
3. **Initialize Dependencies**: Resource bundle for functions.
4. **Chatbot Function**: Persona, Task, Context, Guardrail
5. **Helper Funtion**: Running chatbot on cli

---

### Extra notes

|Aspect|Schemas|Dependencies|
|------|-------|------------|
|**Purpose**|Data structure/validation|Resource/tool management|
|**Focus**|"What does data should look like"|"What does function need"|
|**Usage**|I/O validation|Function configuration|
|**Lifecycle**|Create per message/request|Create once, reused|