python_sources()

python_requirements()

python_awslambda_layer(
    name="lambda_layer",
    requirements=["boto3", "openai"],
)

python_awslambda(
    name="monitor_zip",
    handler="lambda_handler.handler",
    runtime="python3.11",
    include_requirements=False,
    dependencies=[":lambda_layer"],
)
