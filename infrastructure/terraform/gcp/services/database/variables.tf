variable "project_id" {
  description = "Google Cloud Project ID"
  type        = string
}
variable "region" {
  description = "Google Cloud region"
  type        = string
}
variable "db_name" {
  description = "Cloud SQL のデータベース名"
  type        = string
}
variable "db_username" {
  description = "Cloud SQL データベースのユーザー名"
  type        = string
}
variable "db_password" {
  description = "Cloud SQL データベースのパスワード"
  type        = string
}
variable "db_client_service_accounts" {
  description = "Cloud SQL へのアクセス権限を付与するサービスアカウント一覧"
  type        = list(string)
  default     = []
}