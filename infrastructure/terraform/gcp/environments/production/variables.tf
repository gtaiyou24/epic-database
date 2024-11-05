variable "project_id" {
  description = "Google Cloud Project ID"
  type        = string
}

variable "region" {
  description = "Google Cloud region"
  type        = string
  default     = "asia-northeast1"
}

variable "database_name" {
  description = "データベース名"
  type        = string
}
variable "database_username" {
  description = "データベースにアクセスするユーザー名"
  type        = string
}
variable "domain" {
  description = "Cloud DNS で登録しているドメイン名"
  type        = string
}