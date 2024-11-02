output "load_balancer_ip" {
  value = google_compute_global_address.alb_ip.address
  description = "Load Balancer の IP アドレス。この IP アドレスをドメインの DNS レコードに指定してください。"
}