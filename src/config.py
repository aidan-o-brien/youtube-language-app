from dataclasses import dataclass


@dataclass
class Config:
    num_questions: int = 3
    llm_model: str = "gpt-4.1-nano"
    llm_temperature: float = 0.7
