import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variable
load_dotenv()

# Instantiate client
client = OpenAI(api_key=os.getenv("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"))

def generate_gpt_explanation(prompt: str, model="gpt-3.5-turbo", temperature=0.7) -> str:
    """
    Sends a prompt to the OpenAI API using the new openai>=1.0.0 client.
    """
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are an expert actuarial assistant who explains loss of support calculations clearly."},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"⚠️ An error occurred while calling GPT: {e}"

# Example usage (optional)
if __name__ == "__main__":
    test_prompt = "Explain how future loss of support is calculated for a South African claimant."
    print(generate_gpt_explanation(test_prompt))
