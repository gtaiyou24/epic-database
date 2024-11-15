variable "project_id" {
  description = "Google Cloud Project ID"
  type        = string
}
variable "project_number" {
  description = "Google Cloud Project Number"
  type        = string
}
variable "region" {
  description = "Google Cloud region"
  type        = string
}
variable "image" {
  description = "Batch コンテナの Docker イメージ"
  type        = string
  default     = "us-docker.pkg.dev/cloudrun/container/job:latest"
}