terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "6.10.0"
    }
  }
}
# GCPプロバイダー の設定
provider "google" {
  project = var.project_id
  region  = var.region
}

# 🤖 GitHub Actions のサービスアカウントを作成する
resource "google_service_account" "github_actions" {
  account_id   = "github-actions"
  display_name = "GitHub Actions サービスアカウント"
  description  = "GitHub Actions が GCP へアプリをデプロイするためのサービスアカウント"
}
# 🔐 GitHub Actions サービスアカウントにロールを付与
resource "google_project_iam_member" "run-admin" {
  project = var.project_id
  role    = "roles/run.admin"  # Cloud Run デプロイ権限を付与
  member  = "serviceAccount:${google_service_account.github_actions.email}"
}
resource "google_project_iam_member" "artifact-registry-repo-admin" {
  project = var.project_id
  role    = "roles/artifactregistry.repoAdmin"  # Artifact Registry へのプッシュ、削除をするためのロール
  member  = "serviceAccount:${google_service_account.github_actions.email}"
}
resource "google_service_account_iam_member" "iam-service-account-user" {
  for_each           = { for sa in var.deployment_service_account_ids : sa => "projects/${var.project_id}/serviceAccounts/${sa}" }
  service_account_id = each.value
  role               = "roles/iam.serviceAccountUser"  # GitHub Actions サービスアカウントに Cloud Run などのコンピューティングをデプロイする権限を付与
  member             = "serviceAccount:${google_service_account.github_actions.email}"
}

# 🛠️ Workload Identity プール・プロバイダを作成する
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

# 👌 Workload Identity プロバイダが該当のサービスアカウントの権限を借用することを許可する
resource "google_service_account_iam_binding" "allow_workload_identity_user" {
  service_account_id = google_service_account.github_actions.name
  role = "roles/iam.workloadIdentityUser"
  members = [
    "principalSet://iam.googleapis.com/projects/${var.project_number}/locations/global/workloadIdentityPools/${google_iam_workload_identity_pool.github_actions_oidc.workload_identity_pool_id}/attribute.repository/${var.github_repo_owner}/${var.github_repo_name}"
  ]
}