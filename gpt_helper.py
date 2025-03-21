import requests

def generate_gpt_explanation(prompt: str, model="mistral") -> str:
    """
    Uses a local LLM via Ollama to generate explanations.
    Requires Ollama running locally (http://localhost:11434).
    """
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False
            }
        )
        return response.json()["response"].strip()
    except Exception as e:
        return f"⚠️ An error occurred calling the local LLM: {e}"

# Example usage (optional)
if __name__ == "__main__":
    test_prompt = "Explain how future loss of support is calculated in South African actuarial practice."
    print(generate_gpt_explanation(test_prompt))
