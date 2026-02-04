import json

class PlannerAgent:
    def __init__(self, llm_client):
        self.llm_client = llm_client
        self.tool_descriptions = {
            "OpenWeather": "Get current weather by city. Needs 'city' as input.",
            "NewsAPI": "Search news by keyword or get top headlines. Use 'query', 'category', or 'country'."
        }

    def create_plan(self, user_request: str) -> list:
        tools_info = "\n".join(f"- {name}: {desc}" for name, desc in self.tool_descriptions.items())

        system_prompt = (
            "You are a planning assistant that converts a user's natural language task "
            "into a JSON step-by-step plan using real tools.\n\n"
            f"Available tools:\n{tools_info}\n\n"
            "Each step MUST include:\n"
            "- 'tool': the tool name (OpenWeather or NewsAPI)\n"
            "- 'action': the operation (e.g. 'current_weather' or 'search')\n"
            "- 'params': the input values (e.g. city or query)\n"
            "- 'result_key': a short label for storing this step’s result\n\n"
            "DO NOT use placeholders like 'user_input_city' — use actual values from the request.\n"
            "Return only valid JSON like:\n"
            "[{\"tool\": \"OpenWeather\", \"action\": \"current_weather\", \"params\": {\"city\": \"Tokyo\"}, \"result_key\": \"weather_tokyo\"}]"
        )

        plan_text = self.llm_client.generate(system_prompt, user_request)

        try:
            start = plan_text.index("[")
            end = plan_text.rindex("]") + 1
            json_plan = plan_text[start:end]
            parsed = json.loads(json_plan)
            if not isinstance(parsed, list):
                raise ValueError("Plan must be a list of steps.")
            return parsed
        except Exception as e:
            raise RuntimeError(f" Failed to parse plan JSON: {e}\n\nRaw output:\n{plan_text}")
