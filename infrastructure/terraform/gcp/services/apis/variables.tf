variable "project_id" {
  description = "GCP Project ID"
  type        = string
}
variable "enable_apis" {
  description = "有効化する Google の API 一覧"
  type = list(string)
}
variable "wait_for_seconds" {
  description = "API を有効化した後、数秒待機しないとエラーになるため待機する秒数を指定"
  type = number
}