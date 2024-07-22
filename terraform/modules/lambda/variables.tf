variable "lambda_role_arn" {
  type        = string
}

variable "lambda_function_name" {
  type        = string
  default     = "sg-alert"
}

variable "webhook_url" {
  type        = map(string)
  default     = {
    WEBHOOK_URL = "https://hooks.slack.com/services/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"
  }
}
