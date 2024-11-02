variable "project_id" {
  description = "Google Cloud Project ID"
  type        = string
}
variable "region" {
  description = "Google Cloud region"
  type        = string
}
variable "storage_name" {
  description = "ストレージ名"
  type        = string
}
variable "admin_role_service_accounts" {
  description = "ストレージの管理者権限を付与するサービスアカウント一覧"
  type        = list(string)
  default     = []
}