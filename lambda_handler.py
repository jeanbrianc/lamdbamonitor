"""AWS Lambda entry point to invoke the monitoring logic."""
from lambda_monitor import alert_on_failure

def handler(event, context):
    """Entry point for AWS Lambda."""
    function_name = event.get("function_name")
    topic_arn = event.get("sns_topic_arn")
    minutes = event.get("minutes", 5)
    threshold = event.get("threshold", 0.05)
    region = event.get("region", "us-east-1")
    openai_api_key = event.get("openai_api_key")
    if not function_name or not topic_arn:
        raise ValueError("function_name and sns_topic_arn are required")
    return alert_on_failure(
        function_name,
        topic_arn,
        minutes,
        threshold,
        region,
        openai_api_key=openai_api_key,
    )
