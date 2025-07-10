"""AWS Lambda entry point to invoke the monitoring logic."""
import logging

from lambda_monitor import alert_on_failure

logger = logging.getLogger(__name__)

def handler(event, context):
    """Entry point for AWS Lambda."""
    logger.info("Starting lambda monitor handler")
    # Support single name or list of names
    fn_value = event.get("function_names") or event.get("function_name")
    if isinstance(fn_value, str):
        function_names = [fn_value]
    elif fn_value:
        function_names = list(fn_value)
    else:
        function_names = None

    topic_arn = event.get("sns_topic_arn")
    minutes = event.get("minutes", 5)
    threshold = event.get("threshold", 0.05)
    region = event.get("region", "us-east-1")
    openai_api_key = event.get("openai_api_key")
    if not topic_arn:
        raise ValueError("sns_topic_arn is required")
    if function_names:
        logger.info(
            "Checking failure rates for %s over last %s minutes",
            ", ".join(function_names),
            minutes,
        )
    else:
        logger.info("Checking failure rates for all Lambda functions over %s minutes", minutes)
    return alert_on_failure(
        topic_arn,
        function_names,
        minutes,
        threshold,
        region,
        openai_api_key=openai_api_key,
    )
