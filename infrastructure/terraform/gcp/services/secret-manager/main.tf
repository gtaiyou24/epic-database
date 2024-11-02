# 🔐 シークレットマネージャーに保存するデータを指定
resource "google_secret_manager_secret" "secrets" {
  for_each   = var.secrets
  secret_id  = each.key
  replication {
    auto {}
  }
}
# 各シークレットのバージョンリソースを作成
resource "google_secret_manager_secret_version" "secret_versions" {
  for_each    = var.secrets
  secret      = google_secret_manager_secret.secrets[each.key].id
  secret_data = each.value
}

# 🤖 Secret Manager にアクセスするサービスアカウントを指定
resource "google_project_iam_member" "cloud_sql_client" {
  for_each = { for idx, sa in var.accessor_service_accounts : idx => "serviceAccount:${sa}" }
  project = var.project_id
  role    = "roles/secretmanager.secretAccessor"
  member  = each.value
}