import json
from openai import OpenAI
import streamlit as st


def generate_questions(text, config, prompt):
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    prompt = prompt.format(n=config.num_questions, text=text)
    try:
        response = client.chat.completions.create(
            model=config.llm_model,
            messages=[{"role": "user", "content": prompt}],
            temperature=config.llm_temperature
        )
        return json.loads(response.choices[0].message.content)
    except json.JSONDecodeError:
        st.error("❌ Could not parse LLM response as JSON. Try again or adjust prompt.")
    except Exception as e:
        st.error(f"LLM call failed: {e}")
    return []