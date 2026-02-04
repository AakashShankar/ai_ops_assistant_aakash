# AI Operations Assistant Aakash

This project is a multi-agent AI system that can plan and execute user tasks involving real-world APIs  such as getting weather or the latest news — using LLM reasoning, real-time API calls, and structured output verification.

> Example prompt:  
> _“What’s the weather in Delhi and the latest tech news?”_

---

##  Features

-  **Multi-agent design**: Planner → Executor → Verifier loop
-  **Real API integrations**: OpenWeather + NewsAPI
-  **LLM-based structured planning and verification**
-  **Self-correcting system**: detects failures and replans automatically
-  **Natural language interface** with a Streamlit UI

---

##  Architecture

```text
User Input
   ↓
[Planner Agent] → generates JSON plan using LLM
   ↓
[Executor Agent] → runs plan with real API calls
   ↓
[Verifier Agent] → checks results via LLM
   ↓
 Success or  Replan if needed
