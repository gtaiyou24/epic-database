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
  default     = "asia-northeast1"
}
variable "deployment_service_account_ids" {
  description = "デプロイ先のサービスアカウント一覧"
  type        = list(string)
}
variable "github_repo_owner" {
  description = "デプロイする GitHub リポジトリのオーナー名"
  type        = string
}
variable "github_repo_name" {
  description = "デプロイする GitHub リポジトリ名"
  type        = string
}