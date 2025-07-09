"""Helpers for interacting with an AI model to summarize errors or propose fixes."""

import logging

from typing import List, Optional

import openai

logger = logging.getLogger(__name__)

# Placeholder for integration with your favorite AI library (e.g. OpenAI, Anthropic)
# The function below takes the top error messages and raw logs, then calls the model
# to generate a short summary and potential fix. In a real deployment you would
# provide API keys or use a local model.


def summarize_errors(
    top_errors: List[str],
    logs: List[str],
    model: str = "gpt-3.5-turbo",
    api_key: Optional[str] = None,
) -> str:
    """Return an AI-generated summary for the given errors and logs.

    Parameters
    ----------
    top_errors:
        The most common error messages.
    logs:
        Recent log lines from CloudWatch.
    model:
        The chat model to use.
    api_key:
        Optional OpenAI API key to use for this request.
    """
    if api_key:
        logger.info("Using provided OpenAI API key")
        openai.api_key = api_key
    logger.info("Generating summary with model %s", model)
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
    summary = response["choices"][0]["message"]["content"].strip()
    logger.info("Summary generated")
    return summary
