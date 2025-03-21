import os
import openai
from dotenv import load_dotenv

# Load from .env locally; ignored on Streamlit Cloud (safe)
load_dotenv()
openai.api_key = os.getenv("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")

def generate_gpt_explanation(prompt: str, model="gpt-3.5-turbo", temperature=0.7) -> str:
    """
    Sends a prompt to the OpenAI API and returns a natural language explanation.
    """
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are an expert actuarial assistant who explains loss of support calculations clearly."},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"⚠️ An error occurred while calling GPT: {e}"
