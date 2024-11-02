output "service_account_email" {
  value = google_service_account.subscriber.email
  description = "Subscriber サービスアカウントのメールアドレス"
}