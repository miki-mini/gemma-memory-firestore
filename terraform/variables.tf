variable "project_id" {
  description = "The ID of the Google Cloud project"
  type        = string
}

variable "region" {
  description = "The region for resources"
  type        = string
  default     = "asia-northeast1"
}
