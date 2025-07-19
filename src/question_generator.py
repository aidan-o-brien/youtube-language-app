import json

from openai import OpenAI


class OpenAIClientError(Exception):
    """Custom exception for OpenAI client errors."""


class OpenAIQuestionGenerator:
    def __init__(self, api_key, llm_model, llm_temperature, prompt, num_questions):
        self.client = OpenAI(api_key=api_key)
        self.llm_model = llm_model
        self.prompt = prompt
        self.llm_temperature = llm_temperature
        self.num_questions = num_questions

    def generate_questions(self, text):
        prompt = self.prompt.format(n=self.num_questions, text=text)
        try:
            response = self.client.chat.completions.create(
                model=self.llm_model,
                messages=[{"role": "user", "content": prompt}],
                temperature=self.llm_temperature,
            )
            return json.loads(response.choices[0].message.content)
        except json.JSONDecodeError as e:
            raise OpenAIClientError("Could not parse LLM response as JSON.") from e
        except Exception as e:
            raise OpenAIClientError(f"LLM call failed: {e}") from e
