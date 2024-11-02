# 🗃️ ストレージを作成
resource "google_storage_bucket" "public" {
  # インターネットからアクセス可能なストレージ
  name          = "${var.storage_name}-public"
  location      = var.region
  storage_class = "STANDARD"
  versioning {
    enabled = true
  }
  # ⌚️ ストレージにアップロードされたオブジェクトのタグに応じて TTL を変えるために以下の設定をしました。
  dynamic "lifecycle_rule" {
    for_each = {
      "24h" = 1
      "72h" = 3
    }
    content {
      action {
        type = "Delete"
      }
      condition {
        age = lifecycle_rule.value
        matches_prefix = ["24h", "72h"]
      }
    }
  }
}
resource "google_storage_bucket" "private" {
  # GCP 内部からしかアクセスできないストレージ
  name          = "${var.storage_name}-private"
  location      = var.region
  storage_class = "STANDARD"
  versioning {
    enabled = true
  }
  # ⌚️ ストレージにアップロードされたオブジェクトのタグに応じて TTL を変えるために以下の設定をしました。
  dynamic "lifecycle_rule" {
    for_each = {
      "24h" = 1
      "72h" = 3
    }
    content {
      action {
        type = "Delete"
      }
      condition {
        age = lifecycle_rule.value
        matches_prefix = ["24h", "72h"]
      }
    }
  }
}

# 🔐 アクセス権限を付与
resource "google_project_iam_member" "storage-admin-member" {
  # サービスアカウントのリストに基づいて IAM メンバーを動的に作成
  # for_each = toset(var.admin_role_service_accounts)
  for_each = { for idx, sa in var.admin_role_service_accounts : idx => sa }
  project  = var.project_id
  role     = "roles/storage.objectAdmin"
  member   = "serviceAccount:${each.value}"  # 各サービスアカウントに対して権限を付与
}

# 🔐 public バケットには全てのユーザーが閲覧できるようにする
resource "google_storage_bucket_iam_binding" "public_bucket_iam_binding" {
  bucket = google_storage_bucket.public.name
  role = "roles/storage.legacyObjectReader"
  members = ["allUsers"]
}