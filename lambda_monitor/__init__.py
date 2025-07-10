"""Lambda observability utilities."""

from .cloudwatch import fetch_recent_logs, get_failure_rate, list_lambda_functions
from .analysis import find_common_errors
from .ai_assistant import summarize_errors
from .alerts import send_email_alert
from .monitor import alert_on_failure

__all__ = [
    "fetch_recent_logs",
    "find_common_errors",
    "summarize_errors",
    "send_email_alert",
    "get_failure_rate",
    "list_lambda_functions",
    "alert_on_failure",
]
