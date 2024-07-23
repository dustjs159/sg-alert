resource "aws_lambda_function" "lambda_function" {
  function_name = "${var.lambda_function_name}"
  role = "${var.lambda_role_arn}"
  filename = "${path.cwd}/../src/lambda_function.zip"
  handler = "lambda_function.lambda_handler"
  runtime = "python3.12"
  source_code_hash = filebase64sha256("${path.cwd}/../src/lambda_function.zip")
  environment {
    variables = "${var.lambda_envs}"
  }
}