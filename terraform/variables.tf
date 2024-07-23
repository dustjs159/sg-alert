variable "AWS_REGION" {
  type        = string
  default     = "ap-northeast-2"
}

variable "lambda_envs" {
  type        = map(string)
}
