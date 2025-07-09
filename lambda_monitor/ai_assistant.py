"""Helpers for interacting with an AI model to summarize errors or propose fixes."""

from typing import List

import openai

# Placeholder for integration with your favorite AI library (e.g. OpenAI, Anthropic)
# The function below takes the top error messages and raw logs, then calls the model
# to generate a short summary and potential fix. In a real deployment you would
# provide API keys or use a local model.


def summarize_errors(top_errors: List[str], logs: List[str], model: str = "gpt-3.5-turbo") -> str:
    """Return an AI-generated summary for the given errors and logs."""
    prompt = (
        "You are an observability assistant. Summarize the probable root causes\n"
        "from these Lambda logs and suggest a fix if obvious.\n"
        f"Top errors: {top_errors}\n"
        f"Recent logs:\n" + "\n".join(logs[:20])
    )

    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )
    return response["choices"][0]["message"]["content"].strip()
