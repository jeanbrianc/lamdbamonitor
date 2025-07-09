"""Simple alerting utilities using Amazon SNS."""

import boto3


def send_email_alert(topic_arn: str, subject: str, message: str, region: str = "us-east-1") -> None:
    """Publish an alert to an SNS topic that emails subscribers."""
    client = boto3.client("sns", region_name=region)
    client.publish(TopicArn=topic_arn, Subject=subject, Message=message)
