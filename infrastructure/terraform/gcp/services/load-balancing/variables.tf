variable "project_id" {
  description = "Google Cloud Project ID"
  type        = string
}
variable "region" {
  description = "Google Cloud region"
  type        = string
}
variable "domain" {
  description = "ドメイン名"
  type        = string
}
variable "web_application_cloud_run_name" {
  description = "Web アプリケーションの Cloud Run 名"
  type        = string
}
variable "public_bucket_name" {
  description = "Cloud Storage で構築された公開用バケットの名前"
  type        = string
}