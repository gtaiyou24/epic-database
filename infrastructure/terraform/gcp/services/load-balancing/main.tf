# 🔗 グローバル外部アプリケーションロードバランサを作成する
# - https://cloud.google.com/load-balancing/docs/https/setup-global-ext-https-serverless?hl=ja
# - https://zenn.dev/contrea/articles/af698f77953bc5
# - https://cloud.google.com/load-balancing/docs/https/ext-http-lb-tf-module-examples?hl=ja#with_a_backend
# - https://cloud.google.com/blog/ja/products/serverless/serverless-load-balancing-terraform-hard-way


# 📌 グローバル静的外部 IP アドレスを予約する
resource "google_compute_global_address" "alb_ip" {
  name = "alb-ip"
  description = "グローバル外部アプリケーションロードバランサー の IP アドレス"
  ip_version = "IPV4"
}

# Google が発行および更新するマネージド SSL 証明書を作成
resource "google_compute_managed_ssl_certificate" "default" {
  provider = google-beta

  name = "${var.domain}-cert"
  managed {
    domains = ["${var.domain}"]
  }
}

# 🤖 Load Balancing のサービスアカウントを作成
resource "google_service_account" "alb" {
  account_id   = "global-external-alb"
  display_name = "グローバル外部アプリケーションロードバランサーのサービスアカウント"
}
resource "google_project_iam_member" "run_invoker" {
  project = var.project_id
  role    = "roles/run.invoker"  # ALB から Cloud Run へルーティングするために Cloud Run の起動権限を付与
  member  = "serviceAccount:${google_service_account.alb.email}"
}

# ALB のためのバックエンドサービスを作成
resource "google_compute_backend_service" "compute" {
  name                  = "compute-backend"
  description           = "ALB と Compute システムの間にあるサービス"
  load_balancing_scheme = "EXTERNAL_MANAGED"  # アプリケーション ロードバランサ（HTTP / HTTPS）
  port_name             = "http"
  protocol              = "HTTP"

  backend {
    group = google_compute_region_network_endpoint_group.web_application_neg.id
  }
}
resource "google_compute_backend_bucket" "public_bucket" {
  name        = "public-bucket-backend"
  description = "ALB と Storage システムの間にあるサービス"
  bucket_name = var.public_bucket_name
  enable_cdn  = true
  cdn_policy {
    cache_mode        = "CACHE_ALL_STATIC"
    client_ttl        = 3600
    default_ttl       = 3600
    max_ttl           = 86400
    negative_caching  = true
    serve_while_stale = 86400
  }
}

# Compute システムをまとめた Network Endpoint Group (NEG)
resource "google_compute_region_network_endpoint_group" "web_application_neg" {
  name                  = "web-application-neg"
  network_endpoint_type = "SERVERLESS"
  region                = var.region
  cloud_run {
    service = var.web_application_cloud_run_name
  }
}

# ALB ルーティングのための URL マップ
# リクエストがきたURLの振り分け設定をしています。
resource "google_compute_url_map" "alb_url_map" {
  name            = "alb-url-map"
  default_service = google_compute_backend_service.compute.id

  host_rule {
    hosts = ["*"]
    path_matcher = ""
  }
  path_matcher {
    name = "all"
    default_service = google_compute_backend_service.compute.id

    route_rules {  # /static のパスは Cloud Storage に遷移させる
      match_rules {
        path_template_match = "/static/*"
      }
      service = google_compute_backend_bucket.public_bucket.id
      priority = 1
    }
  }

  # host_rule {
  #   hosts        = ["epicdatabase.com", "www.epicdatabase.com"]
  #   path_matcher = "frontend"
  # }
  # host_rule {
  #   hosts        = ["api.epicdatabase.com"]
  #   path_matcher = "backend"
  # }
  # path_matcher {
  #   name            = "frontend"
  #   default_service = google_compute_backend_service.default.id
  # }
  # path_matcher {
  #   name            = "backend"
  #   default_service = google_compute_backend_service.default.id
  # }
}

# Target HTTPS Proxy for ALB
# HTTPS プロキシを構成して、Google が管理する証明書を使用してトラフィックを終了し、URL マップにルーティング
resource "google_compute_target_https_proxy" "alb" {
  name    = "alb-https-proxy"
  url_map = google_compute_url_map.alb_url_map.id
  ssl_certificates = [
    google_compute_managed_ssl_certificate.default.id
  ]
}

# Cloud Load Balancer (ALB) frontend IP and TCP connection
resource "google_compute_global_forwarding_rule" "alb_rule" {
  name       = "alb-rule"
  target     = google_compute_target_https_proxy.alb.id
  port_range = "443"
  load_balancing_scheme = "EXTERNAL_MANAGED"
  ip_address = google_compute_global_address.alb_ip.address
}


# 🚫 HTTP から HTTPS にリダイレクト
resource "google_compute_url_map" "https_redirect" {
  name            = "${var.domain}-https-redirect"

  default_url_redirect {
    https_redirect         = true
    redirect_response_code = "MOVED_PERMANENTLY_DEFAULT"
    strip_query            = false
  }
}
resource "google_compute_target_http_proxy" "https_redirect" {
  name   = "${var.domain}-http-proxy"
  url_map          = google_compute_url_map.https_redirect.id
}
resource "google_compute_global_forwarding_rule" "https_redirect" {
  name   = "${var.domain}-fwdrule-http"
  target = google_compute_target_http_proxy.https_redirect.id
  port_range = "80"
  ip_address = google_compute_global_address.alb_ip.address
}