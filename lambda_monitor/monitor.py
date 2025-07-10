from typing import Optional, List
import logging

from .cloudwatch import get_failure_rate, fetch_recent_logs, list_lambda_functions
from .analysis import find_common_errors
from .ai_assistant import summarize_errors
from .alerts import send_email_alert

logger = logging.getLogger(__name__)


def alert_on_failure(
    topic_arn: str,
    function_names: Optional[List[str]] = None,
    minutes: int = 5,
    threshold: float = 0.05,
    region: str = "us-east-1",
    openai_api_key: Optional[str] = None,
) -> bool:
    """Check failure rates for each function and send email alerts when exceeded.

    ``function_names`` may be ``None`` to automatically discover all Lambda
    functions via CloudWatch log groups. Returns ``True`` if any alert was sent.
    """
    if not function_names:
        function_names = list_lambda_functions(region)
        logger.info("Discovered functions: %s", ", ".join(function_names))

    alerted = False
    for function_name in function_names:
        logger.info("Checking failure rate for %s", function_name)
        rate = get_failure_rate(function_name, minutes, region)
        if rate > threshold:
            logger.info(
                "Failure rate %.2f%% exceeds threshold %.2f%%",
                rate * 100,
                threshold * 100,
            )
            logs = fetch_recent_logs(function_name, minutes, region)
            top_errors = [e for e, _ in find_common_errors(logs)]
            summary = summarize_errors(top_errors, logs, api_key=openai_api_key)
            subject = f"Lambda {function_name} failure rate {rate:.1%}"
            send_email_alert(topic_arn, subject, summary, region)
            alerted = True
        else:
            logger.info("Failure rate %.2f%% within threshold for %s", rate * 100, function_name)
    return alerted
