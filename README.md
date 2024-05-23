# AWS Config Notifier

This is a helpful lambda that will notify you about various `aws-config`
 compliance notifications to a given SNS topic.

## Deployment

It is recommended you use the
[transcom/lambda/aws](https://github.com/transcom/terraform-aws-lambda)
module to do the deployment.
 Below is an example:

```hcl

module "config_notifier" {
  source                 = "transcom/lambda/aws"
  version                = "3.0.0"
  name                   = "config_notifier"
  handler                = "handler.handler"
  job_identifier         = "config_notifier"
  runtime                = "python3.11"
  timeout                = "500"
  role_policy_arns_count = 2
  role_policy_arns = [
    aws_iam_policy.config_notifier_policy.arn,
    "arn:${data.aws_partition.current.partition}:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole",
  ]

  github_project = "transcom/aws-config-notifier"
  github_release = "v0.1.16"
  validation_sha = "c4cf3787ac722e01805b5bc7109926aca4e8dfaed3c555d13a8b6e95a27fc250"


  s3_bucket = "example-lambda-builds-us-west-1"
  s3_key    = "config-notifier/1.6.0/deployment.zip"

  cloudwatch_logs_retention_days = var.log_retention_days

  source_types = ["events"]
  source_arns  = [aws_cloudwatch_event_rule.config_notifier_lambda_rule_trigger.arn]

  publish = true

  env_vars = {
    ENVIRONMENT        = "exmaple-us-west-1-demo"
    NOTIFICATION_TITLE = "Non-Compliant Resource Report"
    SNS_TOPIC          = aws_sns_topic.infra_notif_us_gov_west_1.arn
  }

  tags = {
    "Service" = "config_notifier"
  }

}

```
