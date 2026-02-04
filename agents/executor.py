class ExecutorAgent:
    def __init__(self, tools: dict):
        """
        tools: dict like {'OpenWeather': OpenWeatherTool(), 'NewsAPI': NewsAPITool()}
        """
        self.tools = tools

    def execute_plan(self, plan: list) -> dict:
        results = {}
        for step in plan:
            tool_name = step.get("tool")
            action = step.get("action")
            params = step.get("params", {})
            result_key = step.get("result_key")

            tool = self.tools.get(tool_name)
            if not tool:
                results[result_key] = {"error": f"Tool '{tool_name}' not available"}
                continue

            try:
                if tool_name == "OpenWeather":
                    city = params.get("city")
                    results[result_key] = tool.get_current_weather(city)
                elif tool_name == "NewsAPI":
                    if action == "search":
                        query = params.get("query")
                        count = params.get("count", 5)
                        results[result_key] = tool.search_news(query, count)
                    elif action in ["get_headlines", "top_headlines"]:
                        country = params.get("country", "us")
                        category = params.get("category")
                        count = params.get("count", 5)
                        results[result_key] = tool.get_top_headlines(country, category, count)
                    else:
                        results[result_key] = {"error": f"Unknown NewsAPI action: {action}"}
                else:
                    results[result_key] = {"error": f"Unknown tool: {tool_name}"}
            except Exception as e:
                results[result_key] = {"error": str(e)}
        return results
