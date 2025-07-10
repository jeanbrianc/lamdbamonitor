"""Simple alerting utilities using Amazon SNS."""

import logging
import boto3


def send_email_alert(topic_arn: str, subject: str, message: str, region: str = "us-east-1") -> None:
    """Publish an alert to an SNS topic that emails subscribers."""
    logger = logging.getLogger(__name__)
    logger.info("Sending SNS email alert: %s", subject)
    client = boto3.client("sns", region_name=region)
    client.publish(TopicArn=topic_arn, Subject=subject, Message=message)
