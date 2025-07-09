from typing import Optional

from .cloudwatch import get_failure_rate, fetch_recent_logs
from .analysis import find_common_errors
from .ai_assistant import summarize_errors
from .alerts import send_email_alert


def alert_on_failure(
    function_name: str,
    topic_arn: str,
    minutes: int = 5,
    threshold: float = 0.05,
    region: str = "us-east-1",
    openai_api_key: Optional[str] = None,
) -> bool:

    """Check the failure rate and send an email alert if it exceeds the threshold.

    Returns True if an alert was sent.
    """
    rate = get_failure_rate(function_name, minutes, region)
    if rate > threshold:
        logs = fetch_recent_logs(function_name, minutes, region)
        top_errors = [e for e, _ in find_common_errors(logs)]
        summary = summarize_errors(top_errors, logs, api_key=openai_api_key)
        subject = f"Lambda {function_name} failure rate {rate:.1%}"
        send_email_alert(topic_arn, subject, summary, region)
        return True
    return False
