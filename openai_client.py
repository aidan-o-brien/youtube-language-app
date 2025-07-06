import json
from openai import OpenAI


class OpenAIClientError(Exception):
    """Custom exception for OpenAI client errors."""

def generate_questions(text, config, prompt):
    client = OpenAI(api_key=config.openai_api_key)
    prompt = prompt.format(n=config.num_questions, text=text)
    try:
        response = client.chat.completions.create(
            model=config.llm_model,
            messages=[{"role": "user", "content": prompt}],
            temperature=config.llm_temperature
        )
        return json.loads(response.choices[0].message.content)
    except json.JSONDecodeError:
        raise OpenAIClientError("Could not parse LLM response as JSON. Try again or adjust prompt.")
    except Exception as e:
        raise OpenAIClientError(f"LLM call failed: {e}")