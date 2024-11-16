# 📮 Pub/Sub トピックを作成する
resource "google_pubsub_topic" "topic" {
  name = "${var.subscriber_cloud_run_name}-topic"
}

# ========== 🚀 メッセージを処理する Subscriber を構築 ==========

# 🤖 Subscriber サービスのサービスアカウントを作成する
resource "google_service_account" "subscriber" {
  account_id   = var.subscriber_cloud_run_name
  display_name = "${var.subscriber_cloud_run_name} サービスアカウント"
  description  = "${var.subscriber_cloud_run_name} のサービスアカウント"
}
resource "google_project_iam_member" "iam_service_account_user" {
  project = var.project_id
  role    = "roles/iam.serviceAccountUser"  # サービスアカウントユーザー
  member  = "serviceAccount:${google_service_account.subscriber.email}"
}
resource "google_project_iam_member" "run_admin" {  # Cloud Run の管理者権限
  project = var.project_id
  role    = "roles/run.admin"  # Cloud Run の管理者権限
  member  = "serviceAccount:${google_service_account.subscriber.email}"
}

# 🐳 Artifact Registry を作成
resource "google_artifact_registry_repository" "subscriber" {
  provider      = google
  location      = var.region
  repository_id = var.subscriber_cloud_run_name
  format        = "DOCKER"
}

# ⚡️ Push サブスクリプション Cloud Run を作成
resource "google_cloud_run_v2_service" "subscriber" {
  name     = var.subscriber_cloud_run_name
  location = var.region
  # ネットワーキングの上り(内向き)制御：コンテナへのアクセスを内部 + ロードバランサー経由に限定
  ingress = "INGRESS_TRAFFIC_INTERNAL_LOAD_BALANCER"
  template {
    containers {
      image = var.subscriber_image
      resources {
        limits = {
          cpu    = "1"
          memory = "512Mi"
        }
      }
      ports {
        container_port = 8000
      }
    }
    service_account = google_service_account.subscriber.email
  }
  traffic {
    type    = "TRAFFIC_TARGET_ALLOCATION_TYPE_LATEST"
    percent = 100
  }
}

# ========== 🤝 Pub/Sub と Cloud Run を統合する ==========

# 🤖 Cloud Run を呼び出すサービスアカウントを作成する
resource "google_service_account" "subscriber_invoker" {
  account_id   = "${var.subscriber_cloud_run_name}-invoker"
  display_name = "${var.subscriber_cloud_run_name} Pub/Sub Invoker"
  description = "${var.subscriber_cloud_run_name} を呼び出す Pub/Sub のサービスアカウント"
}

# 🔐 Pub/Sub サービスアカウントが Subscriber (Cloud Run) を呼び出すための権限を付与
resource "google_cloud_run_service_iam_binding" "invoker_role" {
  location = google_cloud_run_v2_service.subscriber.location
  service  = google_cloud_run_v2_service.subscriber.name
  role     = "roles/run.invoker"
  members  = ["serviceAccount:${google_service_account.subscriber_invoker.email}"]
}

# 🔐 Pub/Sub がプロジェクトで認証トークンを作成できるようにします
resource "google_project_service_identity" "pubsub_agent" {
  provider = google-beta
  project  = var.project_id
  service  = "pubsub.googleapis.com"
}
resource "google_project_iam_binding" "project_token_creator" {
  project = var.project_id
  role    = "roles/iam.serviceAccountTokenCreator"
  members = ["serviceAccount:${google_project_service_identity.pubsub_agent.email}"]
}

# 📦 Pub/Sub サブスクリプションを作成する
resource "google_pubsub_subscription" "subscription" {
  name  = "${var.subscriber_cloud_run_name}-subscription"
  topic = google_pubsub_topic.topic.name
  ack_deadline_seconds = 300  # 確認応答期限(秒)
  push_config {
    push_endpoint = google_cloud_run_v2_service.subscriber.uri
    oidc_token {
      service_account_email = google_service_account.subscriber_invoker.email
    }
    attributes = {
      x-goog-version = "v1"
    }
  }
  retry_policy {
    // default
    minimum_backoff = "10s"
    maximum_backoff = "600s"
  }
  depends_on = [google_cloud_run_v2_service.subscriber]
}

# ========== 🗓️ Scheduler を定義する ==========
locals {
  jobs = {
    "health_check" = {
      description = "ヘルスチェック"
      schedule    = "0 * * * *"
      body        = "{\"publisher_name\": \"api-gateway\", \"event_type\": \"HealthCheck.1\", \"greeting\": \"こんにちは\"}"
    },
    // ジョブを追記する
  }
}

resource "google_service_account" "scheduler" {
  account_id   = "scheduler"
  description  = "Scheduler サービスアカウント。Subscriber を起動するトリガーとして起動します。"
  display_name = "Scheduler サービスアカウント"
}

# 直接 Subscriber を呼び出す場合は以下のコメントを外す
# resource "google_cloud_run_service_iam_member" "default" {
#   location = google_cloud_run_v2_service.subscriber.location
#   service  = google_cloud_run_v2_service.subscriber.name
#   role     = "roles/run.invoker"
#   member   = "serviceAccount:${google_service_account.scheduler.email}"  # Subscriber (Cloud Run) を呼び出す権限
# }

resource "google_cloud_scheduler_job" "jobs" {
  for_each    = local.jobs
  name        = each.key
  description = each.value.description
  schedule    = each.value.schedule
  time_zone   = "Asia/Tokyo"
  pubsub_target {
    topic_name = google_pubsub_topic.topic.id
    data       = base64encode(each.value.body)
  }
  # http_target {
  #   http_method = "GET"
  #   uri         = google_cloud_run_v2_service.subscriber.uri
  #   headers = {
  #     "Content-Type" = "application/json"
  #   }
  #   body = each.value.body
  # }
}


# ========== 🤝 Pub/Sub へ Push できるようにする ==========

# 🤖 Pub/Sub トピックに Push できるサービスアカウントを指定
resource "google_pubsub_topic_iam_binding" "publisher_role" {
  topic   = google_pubsub_topic.topic.id
  role    = "roles/pubsub.publisher"
  members = concat(
    ["serviceAccount:${google_service_account.scheduler.email}"],   # Scheduler
    ["serviceAccount:${google_service_account.subscriber.email}"],  # Subscriber
    [for sa in var.publisher_service_accounts : "serviceAccount:${sa}"]             # その他のサービスアカウント
  )
}