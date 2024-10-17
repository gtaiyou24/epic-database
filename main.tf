terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.34.0"
    }
  }
}
# GCPプロバイダー の設定
provider "google" {
  project = var.project_id
  region  = var.region
}

# 💡 1. GCP API を有効にする
locals {
  services = toset([
    "iamcredentials.googleapis.com",
    "secretmanager.googleapis.com",
    "artifactregistry.googleapis.com",
    "run.googleapis.com",
    "iam.googleapis.com"
  ])
}
resource "google_project_service" "apis" {
  project = var.project_id
  for_each = local.services
  service = each.value
}

# ⚙️ 2. GitHub Actions のサービスアカウントを作成する
resource "google_service_account" "github_actions" {
  account_id   = "github-actions"
  display_name = "GitHub Actions サービスアカウント"
  description  = "GitHub Actions が GCP へアプリをデプロイするためのサービスアカウント"
}
# Artifact Registry を作成 (Docker イメージを保存)
resource "google_artifact_registry_repository" "artifact-repository" {
  provider    = google
  location    = var.region
  repository_id = var.github_repo_name
  format      = "DOCKER"
}

# GitHub Actions サービスアカウントにロールを付与
resource "google_project_iam_member" "github-actions-deploy-compute" {
  project = var.project_id
  role    = "roles/run.admin"  # Cloud Run デプロイ権限を付与
  member  = "serviceAccount:${google_service_account.github_actions.email}"
}
resource "google_project_iam_member" "github-actions-push-docker-image" {
  project = var.project_id
  role    = "roles/artifactregistry.repoAdmin"  # Artifact Registry へのプッシュ、削除をするためのロール
  member  = "serviceAccount:${google_service_account.github_actions.email}"
}

# 🛠️ 3. Workload Identity プール・プロバイダを作成する
resource "google_iam_workload_identity_pool" "github_actions_oidc" {  # Workload Identity プールを作成
  workload_identity_pool_id = "github-actions-oidc"
  display_name              = "GitHub Actions OIDC"
  project                   = var.project_id
}
resource "google_iam_workload_identity_pool_provider" "github_actions_provider" {  # Workload Identity プロバイダを作成
  workload_identity_pool_id = google_iam_workload_identity_pool.github_actions_oidc.workload_identity_pool_id
  workload_identity_pool_provider_id = "github-actions-oidc-provider"
  display_name = "GitHub Actions OIDC Provider"
  attribute_condition = "assertion.repository == \"${var.github_repo_owner}/${var.github_repo_name}\""

  attribute_mapping = {
    "google.subject"          = "assertion.sub"
    "attribute.repository"    = "assertion.repository"
    "attribute.actor"         = "assertion.actor"
  }
  oidc {
    issuer_uri = "https://token.actions.githubusercontent.com"
  }
}

# 👌 4. Workload Identity プロバイダが該当のサービスアカウントの権限を借用することを許可する
resource "google_service_account_iam_binding" "allow_workload_identity_user" {
  service_account_id = google_service_account.github_actions.name
  role = "roles/iam.workloadIdentityUser"
  members = [
    "principalSet://iam.googleapis.com/projects/${var.project_number}/locations/global/workloadIdentityPools/${google_iam_workload_identity_pool.github_actions_oidc.workload_identity_pool_id}/attribute.repository/${var.github_repo_owner}/${var.github_repo_name}"
  ]
}

# ⚙️ 5. Cloud Run サービスのサービスアカウントを作成する
resource "google_service_account" "cloud_run_service_account" {
  account_id   = "cloud-run-service-account"
  display_name = "Cloud Run サービスアカウント"
  description  = "Cloud Run のサービスアカウント"
}
resource "google_project_iam_member" "cloud_run_iam_role_binding" {
  project = var.project_id
  role    = "roles/iam.serviceAccountUser"  # サービスアカウントユーザー
  member  = "serviceAccount:${google_service_account.cloud_run_service_account.email}"
}
resource "google_project_iam_member" "cloud_run_admin_role_binding" {  # Cloud Run の管理者権限
  project = var.project_id
  role    = "roles/run.admin"
  member  = "serviceAccount:${google_service_account.cloud_run_service_account.email}"
}

# resource "google_cloud_run_v2_service" "compute" {
#   name     = var.github_repo_name
#   location = var.region
#
#   template {
#     containers {
#       image = "${var.region}-docker.pkg.dev/${var.project_id}/${var.github_repo_name}:latest"
#       resources {
#         limits = {
#           cpu    = "1"
#           memory = "512Mi"
#         }
#       }
#     }
#     # サービスアカウントを指定
#     service_account = google_service_account.cloud_run_service_account.email
#   }
#
#   traffic {
#     type    = "TRAFFIC_TARGET_ALLOCATION_TYPE_LATEST"
#     percent = 100
#   }
# }
# # Cloud Run サービスにアクセス権を付与 (全ユーザーに公開する場合)
# resource "google_project_iam_member" "cloud_run_invoker_permission" {
#   project = var.project_id
#   role    = "roles/run.invoker"
#   member  = "allUsers" # 公開する場合。非公開なら特定のIAMメンバーを指定
# }
