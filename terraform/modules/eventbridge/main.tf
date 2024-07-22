resource "aws_cloudwatch_event_rule" "event_rule" {
    name = "${var.rule_name}"
    event_pattern = jsonencode({
        "source" = ["aws.ec2"],
        "detail-type" = ["AWS API Call via CloudTrail"],
        "detail" = {
            "eventSource": ["ec2.amazonaws.com"],
            "eventName": ["AuthorizeSecurityGroupIngress", "AuthorizeSecurityGroupEgress", "RevokeSecurityGroupIngress", "RevokeSecurityGroupEgress", "CreateSecurityGroup", "DeleteSecurityGroup"]
        }
    })
}

resource "aws_cloudwatch_event_target" "event_target" {
  rule = aws_cloudwatch_event_rule.event_rule.name
  arn = "${var.lambda_function_arn}"
}