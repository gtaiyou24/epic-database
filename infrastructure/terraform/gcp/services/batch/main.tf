terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.34.0"
    }
  }
}
# ========== 🗓️ Cloud Run Job を定義する ==========

# 🤖 Subscriber サービスのサービスアカウントを作成する
resource "google_service_account" "batch" {
  account_id   = "batcher"
  display_name = "Batch サービスアカウント"
  description  = "Cloud Run Job / Batch のサービスアカウント"
}
resource "google_project_iam_member" "iam_service_account_user" {
  project = var.project_id
  role    = "roles/iam.serviceAccountUser"  # サービスアカウントユーザー
  member  = "serviceAccount:${google_service_account.batch.email}"
}
resource "google_project_iam_member" "run_admin" {  # Cloud Run の管理者権限
  project = var.project_id
  role    = "roles/run.admin"  # Cloud Run の管理者権限
  member  = "serviceAccount:${google_service_account.batch.email}"
}

# 🐳 Artifact Registry を作成
resource "google_artifact_registry_repository" "subscriber" {
  provider      = google
  location      = var.region
  repository_id = "batch"
  format        = "DOCKER"
}

# ⚡️ Cloud Run Job を作成
resource "google_cloud_run_v2_job" "batch" {
  provider = google-beta
  project  = var.project_id
  location = var.region
  name     = "batch"

  template {
    template {
      timeout         = "43200s"  # 12時間
      max_retries     = 0   # リトライ回数
      service_account = google_service_account.batch.email
      containers {
        image   = var.image
        args    = ["api-gateway", "HealthCheck.1"]
      }
    }
  }
}

# ========== 🗓️ Scheduler を定義する ==========

locals {
  jobs = {
    "health_check" = {
      description = "Batch ヘルスチェック"
      schedule    = "0 * * * *"
      args        = ["api-gateway", "HealthCheck.1"]
    },
    "download_gbizinfo" = {
      description = "gBizINFO から法人データをダウンロードする"
      schedule    = "23 01 1 * *"    # 毎月の*月1日の1時23分にクローン起動を設定する。
      args        = ["crawler", "DownloadgBizINFO.1"]
    }
    // ジョブを追記する
  }
}
resource "google_cloud_scheduler_job" "cron" {
  for_each    = local.jobs
  name        = "batch-${each.key}"
  description = each.value.description
  schedule    = each.value.schedule
  time_zone   = "Asia/Tokyo"

  retry_config {
    max_backoff_duration = "3600s"
    max_doublings        = 5
    max_retry_duration   = "0s"
    min_backoff_duration = "300s"
    retry_count          = 0
  }

  http_target {
    http_method = "POST"
    uri         = "https://${google_cloud_run_v2_job.batch.location}-run.googleapis.com/apis/run.googleapis.com/v1/namespaces/${var.project_number}/jobs/${google_cloud_run_v2_job.batch.name}:run"
    oauth_token {
      service_account_email = google_service_account.batch.email
    }
    body = base64encode(jsonencode({
      overrides = {
        containerOverrides = [{
          args = each.value.args
        }]
      }
    }))
  }

  depends_on = [google_cloud_run_v2_job.batch, google_service_account.batch]
}