variable "project_id" {
  description = "Google Cloud Project ID"
  type        = string
}
variable "project_number" {
  description = "Google Cloud Project Number"
  type        = string
}
# variable "deployment_service_account_id" {
#   description = "デプロイ先のサービスアカウント"
#   type        = string
# }
variable "github_repo_owner" {
  description = "デプロイする GitHub リポジトリのオーナー名"
  type        = string
}
variable "github_repo_name" {
  description = "デプロイする GitHub リポジトリ名"
  type        = string
}