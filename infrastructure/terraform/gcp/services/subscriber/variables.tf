variable "project_id" {
  description = "Google Cloud Project ID"
  type        = string
}
variable "region" {
  description = "Google Cloud region"
  type        = string
}
variable "subscriber_cloud_run_name" {
  description = "サブスクライバーの Cloud Run 名"
  type        = string
  default     = "subscriber"
}
variable "subscriber_image" {
  description = "Subscriber コンテナの Docker イメージ"
  type        = string
  default     = "us-docker.pkg.dev/cloudrun/container/hello"
}
variable "publisher_service_accounts" {
  description = "Pub/Sub への Push 権限を付与するサービスアカウント一覧"
  type        = list(string)
  default     = []
}