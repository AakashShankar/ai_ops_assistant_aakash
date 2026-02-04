import streamlit as st
from dotenv import load_dotenv
import os

from agents.planner import PlannerAgent
from agents.executor import ExecutorAgent
from agents.verifier import VerifierAgent
from tools.weather_api import OpenWeatherTool
from tools.news_api import NewsAPITool
from llm.llm_client import LLMClient

st.set_page_config(page_title="AI Operations Assistant", layout="centered")
load_dotenv()  # Load .env file if present

st.title("🌐 AI Operations Assistant")
st.write("Ask me about weather, news, or both. Example: 'What's the weather in Paris and latest tech news?'")

# Input from user
user_input = st.text_input("Your Request:", value="")

if user_input:
    try:
        # Initialize tools and LLM client
        weather_tool = OpenWeatherTool()
        news_tool = NewsAPITool()
        llm_client = LLMClient()

        # Initialize agents
        planner = PlannerAgent(llm_client)
        executor = ExecutorAgent({
            "OpenWeather": weather_tool,
            "NewsAPI": news_tool
        })
        verifier = VerifierAgent(llm_client)

        # PLAN
        st.subheader("📋 Planner Output")
        plan = planner.create_plan(user_input)
        st.json(plan)

        # EXECUTE
        st.subheader("🔧 Execution Results")
        results = executor.execute_plan(plan)
        st.json(results)

        # VERIFY
        st.subheader("🧪 Verifier Verdict")
        verdict = verifier.verify(user_input, plan, results)
        st.json(verdict)

        # REPLAN if needed
        final_output = results
        if verdict.get("status") == "replan" and "plan" in verdict:
            st.warning("Verifier suggested a new plan. Re-executing...")
            new_plan = verdict["plan"]
            st.subheader("🔁 Revised Plan")
            st.json(new_plan)
            final_output = executor.execute_plan(new_plan)
            st.subheader("✅ Final Output")
            st.json(final_output)
        else:
            st.success("Verifier approved the results.")
            st.subheader("✅ Final Output")
            st.json(final_output)

    except Exception as e:
        st.error(f"❌ Error: {e}")
