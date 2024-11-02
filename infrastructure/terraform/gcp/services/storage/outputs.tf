output "public_bucket_name" {
  value = google_storage_bucket.public.name
  description = "公開用のバケット名"
}