variable "lambda_role_arn" {
  type        = string
}

variable "lambda_function_name" {
  type        = string
  default     = "sg-alert"
}

variable "lambda_envs" {
  type        = map(string)
}
