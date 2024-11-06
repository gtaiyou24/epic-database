output "db_host" {
  value = google_compute_global_address.private_ip_address.address
}
output "db_name" {
  value = google_sql_database.database.name
}
output "db_username" {
  value = google_sql_user.user.name
}
output "db_password" {
  value = google_sql_user.user.password
}
output "vpc_connector" {
  value = google_vpc_access_connector.vpc_connector.id
}