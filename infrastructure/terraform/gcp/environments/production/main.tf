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

module "apis" {
  source = "../../services/apis"
  project_id = var.project_id
  enable_apis = [
    "artifactregistry.googleapis.com",  # Artifact Registry
    "run.googleapis.com",               # Cloud Run
    "compute.googleapis.com",           # Compute Engine
    "iam.googleapis.com",               # IAM
    "iamcredentials.googleapis.com",    # IAM

    # Subscriber
    "pubsub.googleapis.com",            # Cloud Pub/Sub
    "cloudscheduler.googleapis.com",    # Cloud Scheduler

    # Database
    "vpcaccess.googleapis.com",         # Serverless VPC Access
    "servicenetworking.googleapis.com", # Service Networking API

    # Secret Manager
    "secretmanager.googleapis.com"
  ]
  wait_for_seconds = 180
}

module "web_application" {
  source = "../../services/web-application"
  project_id = var.project_id
  region = var.region

  depends_on = [module.apis]
}

module "subscriber" {
  source = "../../services/subscriber"

  project_id = var.project_id
  region = var.region
  subscriber_cloud_run_name = "subscriber"
  publisher_service_accounts = [
    module.web_application.service_account_email,
  ]

  depends_on = [module.web_application]
}

module "batch" {
  source = "../../services/batch"

  project_id = var.project_id
  project_number = var.project_number
  region = var.region
}

module "storage" {
  source = "../../services/storage"

  project_id = var.project_id
  region = var.region
  storage_name = "application-objects"
  admin_role_service_accounts = [
    module.subscriber.service_account_email,
    module.web_application.service_account_email
  ]

  depends_on = [module.web_application, module.subscriber]
}

module "load_balancing" {
  source = "../../services/load-balancing"
  project_id = var.project_id
  region = var.region
  domain = var.domain
  web_application_cloud_run_name = module.web_application.name
  public_bucket_name = module.storage.public_bucket_name

  depends_on = [module.web_application, module.storage]
}

resource "random_password" "password" {
  length           = 16
  special          = true
  override_special = "!#$%&*()-_=+[]{}<>:?"
}

module "db" {
  source = "../../services/database"
  project_id = var.project_id
  region = var.region
  db_name = var.database_name
  db_username = var.database_username
  db_password = random_password.password.result

  db_client_service_accounts = [
    module.subscriber.service_account_email,
    module.web_application.service_account_email,
    module.batch.service_account_email
  ]

  depends_on = [module.web_application, module.subscriber, module.batch]
}

module "secretmanager" {
  source = "../../services/secret-manager"

  project_id = var.project_id
  secrets = {
    DATABASE_URL = "postgresql://${module.db.db_username}:${module.db.db_password}@${module.db.db_host}:5432/${module.db.db_name}"
  }
  accessor_service_accounts = [
    module.web_application.service_account_email,
    module.subscriber.service_account_email,
    module.batch.service_account_email
  ]

  depends_on = [module.db, module.web_application, module.subscriber]
}