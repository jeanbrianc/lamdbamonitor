import boto3
from datetime import datetime, timedelta
from typing import List


def get_failure_rate(function_name: str, minutes: int = 5, region: str = "us-east-1") -> float:
    """Return the ratio of errors to invocations for the Lambda in the window."""
    client = boto3.client("cloudwatch", region_name=region)
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=minutes)

    def metric_sum(name: str) -> float:
        resp = client.get_metric_statistics(
            Namespace="AWS/Lambda",
            MetricName=name,
            Dimensions=[{"Name": "FunctionName", "Value": function_name}],
            StartTime=start_time,
            EndTime=end_time,
            Period=minutes * 60,
            Statistics=["Sum"],
        )
        return sum(dp.get("Sum", 0.0) for dp in resp.get("Datapoints", []))

    invocations = metric_sum("Invocations")
    errors = metric_sum("Errors")
    return (errors / invocations) if invocations else 0.0


def fetch_recent_logs(function_name: str, minutes: int = 5, region: str = "us-east-1") -> List[str]:
    """Fetch CloudWatch log messages for the Lambda from the last ``minutes``.

    Parameters
    ----------
    function_name:
        Name of the Lambda function.
    minutes:
        Time window to fetch logs for.
    region:
        AWS region where the function runs.

    Returns
    -------
    List[str]
        Collected log messages.
    """
    client = boto3.client("logs", region_name=region)
    log_group = f"/aws/lambda/{function_name}"
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=minutes)

    events = []
    paginator = client.get_paginator("filter_log_events")
    for page in paginator.paginate(
        logGroupName=log_group,
        startTime=int(start_time.timestamp() * 1000),
        endTime=int(end_time.timestamp() * 1000),
    ):
        for event in page.get("events", []):
            message = event.get("message")
            if message:
                events.append(message)
    return events
