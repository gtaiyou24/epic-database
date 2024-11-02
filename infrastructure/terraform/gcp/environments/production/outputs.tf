output "cloud_sql_vpc_connector" {
  value = module.db.vpc_connector
  description = "Cloud SQL に接続する VPC コネクタ"
}
output "cloud_sql_db_password" {
  description = "Cloud SQL の Password"
  value = module.db.db_password
  sensitive = true
}
output "load_balancer_ip" {
  value = module.load_balancing.load_balancer_ip
  description = "ロードバランサーの IP アドレス。この IP アドレスをドメインの DNS レコードに指定してください。"
}