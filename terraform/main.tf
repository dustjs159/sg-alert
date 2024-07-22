module "iam" {
    source = "./modules/iam"
}

module "lambda" {
    source = "./modules/lambda"
    lambda_role_arn = module.iam.role_arn
}

module "eventbridge" {
    source = "./modules/eventbridge"
    lambda_function_arn = module.lambda.lambda_function_arn
}

resource "aws_lambda_permission" "lambda_permission" {
    statement_id  = "AllowExecutionFromCloudWatchEvents"
    action        = "lambda:InvokeFunction"
    function_name = module.lambda.lambda_function_arn
    principal     = "events.amazonaws.com"
    source_arn    = module.eventbridge.event_rule_arn
}