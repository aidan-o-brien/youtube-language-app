import json
from openai import OpenAI


def generate_questions(text, n_questions=3):
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

    prompt = f"""
Generate {n_questions} multiple-choice questions from the following text.
Format your output as a JSON list, where each item has:
- question: string
- options: list of 4 strings
- answer: the correct option (must match one of the options exactly)

Transcript:
{text[:2000]}
"""
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return json.loads(response.choices[0].message.content)
    except json.JSONDecodeError:
        st.error("❌ Could not parse LLM response as JSON. Try again or adjust prompt.")
    except Exception as e:
        st.error(f"LLM call failed: {e}")
    return []