# 💡 GCP API を有効にする
locals {
  services = toset(var.enable_apis)
}
resource "google_project_service" "googleapis" {
  project = var.project_id
  for_each = local.services
  service = each.value
  disable_dependent_services = true  # 依存サービスを無効にするためのオプション
}
resource "time_sleep" "wait_for_googleapis" {  # googleapis が有効になるまでの数秒待機する
  depends_on      = [google_project_service.googleapis]
  create_duration = "${var.wait_for_seconds}s"
}