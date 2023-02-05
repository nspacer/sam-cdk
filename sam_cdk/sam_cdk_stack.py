from constructs import Construct
from aws_cdk import (
    Duration,
    Stack,
    aws_iam as iam,
    aws_sqs as sqs,
    aws_sns as sns,
    aws_sns_subscriptions as subs,
    aws_lambda as lambda_function
)


class SamCdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        queue = sqs.Queue(
            self, "SamCdkQueue",
            visibility_timeout=Duration.seconds(300),
        )

        topic = sns.Topic(
            self, "SamCdkTopic"
        )

        topic.add_subscription(subs.SqsSubscription(queue))
        lambda_role = role = iam.Role(self, "DemoRole",
                                      assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"))
        role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("ReadOnlyAccess"))

        lambda_function.Function(
            self, 'sam-cdk',
            function_name="sam-cdk-function-demo",
            runtime=lambda_function.Runtime.PYTHON_3_9,
            code = lambda_function.Code.from_asset('lambda_code'),
            handler = 'demo-lambda-code.lambda_handler',
            timeout=Duration.minutes(1),
            role=lambda_role
        )