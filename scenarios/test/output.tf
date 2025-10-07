output "s3_name" {
  value       = aws_s3_bucket.s3.bucket
  description = "S3 bucket Name"
}

output "s3_id" {
  value       = aws_s3_bucket.s3.id
  description = "S3 bucket ID"
}

output "s3_arn" {
  value       = aws_s3_bucket.s3.arn
  description = "S3 bucket ARN"
}
