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
    WEBHOOK_URL = ""
  }
}
