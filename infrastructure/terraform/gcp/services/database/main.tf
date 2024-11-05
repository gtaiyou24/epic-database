# 🔗 https://zenn.dev/ring_belle/books/gcp-cloudrun-terraform

# 🕸️ VPC ネットワークとサブネット
resource "google_compute_network" "vpc" {
  name = "application-database-network"
  description = "Cloud SQL の前段にある VPC ネットワーク"
}

# 🔌 Serverless VPC コネクタ
resource "google_vpc_access_connector" "vpc_connector" {
  name          = "application-db-vpc-con"
  ip_cidr_range = "10.8.1.0/28"
  network       = google_compute_network.vpc.id
}

# VPC ピアリングを Service Networking 用に設定
resource "google_compute_global_address" "private_ip_address" {
  name     = "application-db-private-ip"
  purpose  = "VPC_PEERING"
  address_type = "INTERNAL"
  prefix_length = 16
  network  = google_compute_network.vpc.id
}
resource "google_service_networking_connection" "private_vpc_connection" {
  network                 = google_compute_network.vpc.id
  service                 = "servicenetworking.googleapis.com"
  reserved_peering_ranges = [google_compute_global_address.private_ip_address.name]
}

# 🏢 Cloud SQL インスタンス
resource "google_sql_database_instance" "postgresql" {
  project          = var.project_id
  region           = var.region
  name             = "application-db"
  database_version = "POSTGRES_14"  # MySQL の場合は MYSQL_8_0 などに変更

  settings {
    tier = "db-f1-micro"
    ip_configuration {
      ipv4_enabled = false  # パブリック IP を無効化
      private_network = google_compute_network.vpc.id
    }
  }
  depends_on = [google_compute_network.vpc, google_service_networking_connection.private_vpc_connection]
}

# 💾 Cloud SQL データベースを作成
resource "google_sql_database" "database" {
  name     = var.db_name
  instance = google_sql_database_instance.postgresql.name

  # MySQL の設定
  # charset   = "utf8mb4"
  # collation = "utf8mb4_bin"
}

# 🤖 Cloud SQL ユーザーを作成
resource "google_sql_user" "user" {
  project  = var.project_id
  name     = var.db_username
  instance = google_sql_database_instance.postgresql.name
  password = var.db_password
}

# # 🔐 Cloud SQL にアクセスするサービスアカウントを指定
# resource "google_project_iam_member" "cloud_sql_client" {
#   for_each = { for idx, sa in var.db_client_service_accounts : idx => "serviceAccount:${sa}" }
#   project = var.project_id
#   role    = "roles/cloudsql.client"
#   member = each.value
# }
