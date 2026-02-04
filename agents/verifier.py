import json

class VerifierAgent:
    def __init__(self, llm_client):
        self.llm_client = llm_client
        self.system_prompt = (
            "You are a verification agent that checks if the AI execution fully satisfied the user's request.\n"
            "ONLY respond with a JSON object.\n\n"
            "Respond with:\n"
            "- {\"status\": \"success\"}  — if all results are correct and complete\n"
            "- OR {\"status\": \"replan\", \"plan\": [...]} — with a revised plan list if something failed\n\n"
            "Do NOT explain. No extra text. Just valid JSON only."
        )

    def verify(self, user_request: str, plan: list, results: dict) -> dict:
        plan_str = json.dumps(plan, indent=2)
        summary_lines = []
        for step in plan:
            key = step.get("result_key")
            res = results.get(key)
            if res is None:
                summary = "None"
            elif isinstance(res, dict) and "error" in res:
                summary = f"Error: {res['error']}"
            else:
                summary = str(res)[:200]
            summary_lines.append(f"{key}: {summary}")
        summary_text = "\n".join(summary_lines)

        user_prompt = (
            f"User Request:\n{user_request}\n\n"
            f"Executed Plan:\n{plan_str}\n\n"
            f"Results:\n{summary_text}\n\n"
            f"Does this completely fulfill the user request?"
        )

        try:
            raw = self.llm_client.generate(self.system_prompt, user_prompt).strip()
            if not raw:
                raise ValueError("Verifier response was empty.")

            # Try to extract JSON block from anywhere in response
            start = raw.find("{")
            end = raw.rfind("}") + 1
            json_text = raw[start:end]

            return json.loads(json_text)
        except json.JSONDecodeError:
            raise RuntimeError(f"Verifier LLM failed or returned invalid JSON.\n\nRaw reply:\n{raw}")
        except Exception as e:
            raise RuntimeError(f"Verifier Error: {e}")

