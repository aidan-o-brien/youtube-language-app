from dataclasses import dataclass


@dataclass
class Prompts:
    prompt = """
Generate {n} multiple-choice questions from the following text.
Format your output as a JSON list, where each item has:
- question: string
- options: list of 4 strings
- answer: the correct option (must match one of the options exactly)

Transcript:
{text}
"""
