variable "project_id" {
  description = "Google Cloud Project ID"
  type        = string
  default     = "epic-database-438905"
}

variable "project_number" {
  description = "Google Cloud Project Number"
  type        = string
  default     = "425814525781"
}

variable "region" {
  description = "Google Cloud region"
  type        = string
  default     = "asia-northeast1"
}

variable "image" {
  description = "Docker image for Cloud Run"
  type        = string
  default     = "asia-northeast1-docker.pkg.dev/epic-database-438905/epic-database:latest"
}

variable "github_repo_owner" {
  description = "デプロイする GitHub リポジトリのオーナー名"
  type        = string
  default     = "gtaiyou24"
}

variable "github_repo_name" {
  description = "デプロイする GitHub リポジトリ名"
  type        = string
  default     = "epic-database"
}