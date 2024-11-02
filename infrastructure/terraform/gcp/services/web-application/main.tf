# 🤖 Cloud Run サービスのサービスアカウントを作成する
resource "google_service_account" "web_application_sa" {
  account_id   = "web-application"
  display_name = "Cloud Run サービスアカウント"
  description  = "Cloud Run のサービスアカウント"
}
resource "google_project_iam_member" "iam-service-account-user" {
  project = var.project_id
  role    = "roles/iam.serviceAccountUser"  # サービスアカウントユーザー
  member  = "serviceAccount:${google_service_account.web_application_sa.email}"
}
resource "google_project_iam_member" "run-admin" {  # Cloud Run の管理者権限
  project = var.project_id
  role    = "roles/run.admin"  # Cloud Run の管理者権限
  member  = "serviceAccount:${google_service_account.web_application_sa.email}"
}

# 🐳 Artifact Registry を作成
resource "google_artifact_registry_repository" "backend" {
  provider      = google
  location      = var.region
  repository_id = "backend"
  format        = "DOCKER"
}
resource "google_artifact_registry_repository" "frontend" {
  provider      = google
  location      = var.region
  repository_id = "frontend"
  format        = "DOCKER"
}
resource "google_artifact_registry_repository" "proxy" {
  provider      = google
  location      = var.region
  repository_id = "proxy"
  format        = "DOCKER"
}

# ⚡️ Web アプリケーション Cloud Run を作成
resource "google_cloud_run_v2_service" "web_application" {
  name     = "web-application"
  location = var.region
  # ネットワーキングの上り(内向き)制御：コンテナへのアクセスを内部 + ロードバランサー経由に限定
  ingress = "INGRESS_TRAFFIC_INTERNAL_LOAD_BALANCER"

  template {
    containers {
      image = "us-docker.pkg.dev/cloudrun/container/hello"

      resources {
        limits = {
          cpu    = "1"
          memory = "512Mi"
        }
        startup_cpu_boost = true
      }
      ports {
        container_port = 8080
      }
    }
    # サービスアカウントを指定
    service_account = google_service_account.web_application_sa.email
  }

  traffic {
    type    = "TRAFFIC_TARGET_ALLOCATION_TYPE_LATEST"
    percent = 100
  }
}

# 🔐 セキュリティ: 未認証の呼び出しを許可
resource "google_cloud_run_service_iam_member" "public-access" {
  location = google_cloud_run_v2_service.web_application.location
  project  = google_cloud_run_v2_service.web_application.project
  service  = google_cloud_run_v2_service.web_application.name
  role     = "roles/run.invoker"
  member   = "allUsers"  # 未認証の呼び出しを許可
}
