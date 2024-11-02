variable "project_id" {
  description = "Google Cloud Project ID"
  type        = string
}
variable "secrets" {
  description = "Secret Manager に保存するデータIDと値の一覧"
  type        = map(string)
}
variable "accessor_service_accounts" {
  description = "Secret Manager へのアクセス権限を付与するサービスアカウント一覧"
  type        = list(string)
  default     = []
}