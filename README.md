# Lambda Monitor

This project is a lightweight observability assistant for AWS Lambda functions.
It demonstrates how to pull logs, analyze error patterns, and leverage OpenAI
to summarize failures. If the error rate exceeds a threshold (5% by default),
the tool emails a summary and suggested fix via SNS.

## Folder layout

```
.
├── lambda_monitor/        # Python package with monitoring helpers
│   ├── __init__.py
│   ├── ai_assistant.py    # OpenAI integration for summaries
│   ├── analysis.py        # log analysis utilities
│   ├── alerts.py          # send email alerts via SNS
│   ├── cloudwatch.py      # fetch logs and metrics from CloudWatch
│   └── monitor.py         # orchestration helpers
└── README.md
```

Install dependencies with:

```bash
pip install -r requirements.txt
```

## Example functions

### Pull logs from CloudWatch

```python
from lambda_monitor import fetch_recent_logs

logs = fetch_recent_logs("my-lambda-function", minutes=10)
```

### Analyze common errors

```python
from lambda_monitor import find_common_errors

errors = find_common_errors(logs)
```

### Summarize with AI

```python
from lambda_monitor import summarize_errors

summary = summarize_errors([e for e, _ in errors], logs, api_key="sk-...")
print(summary)
```

### Alert when failures exceed 5%

```python
from lambda_monitor import alert_on_failure

alert_on_failure(
    "my-lambda-function",
    "arn:aws:sns:us-east-1:123456789012:my-topic",
    minutes=10,
    threshold=0.05,
    openai_api_key="sk-...",  # optional
)
```

`alert_on_failure` automatically calls OpenAI to summarize the recent logs and
sends the result via SNS email when the failure rate crosses the threshold.

## Packaging with Pants

This repo includes a basic [Pants](https://www.pantsbuild.org/) setup to
build a deployment package and Lambda layer. Install Pants by running:

```bash
curl -L -O https://static.pantsbuild.org/setup/pants && chmod +x pants
```

Package everything with:

```bash
./pants package ::
```

The resulting ZIP files will be placed in the `dist/` directory and can be
uploaded directly to AWS.
