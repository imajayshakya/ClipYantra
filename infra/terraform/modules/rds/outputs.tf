# RDS Module Outputs

output "db_instance_id" {
  description = "The ID of the RDS instance"
  value       = aws_db_instance.main.id
}

output "db_instance_arn" {
  description = "The ARN of the RDS instance"
  value       = aws_db_instance.main.arn
}

output "db_instance_endpoint" {
  description = "The connection endpoint for the database"
  value       = aws_db_instance.main.endpoint
}

output "db_instance_port" {
  description = "The database port"
  value       = aws_db_instance.main.port
}

output "db_instance_address" {
  description = "The database address"
  value       = aws_db_instance.main.address
}

output "db_instance_status" {
  description = "The RDS instance status"
  value       = aws_db_instance.main.status
}

output "db_instance_engine" {
  description = "The database engine"
  value       = aws_db_instance.main.engine
}

output "db_instance_engine_version" {
  description = "The database engine version"
  value       = aws_db_instance.main.engine_version
}

output "db_instance_class" {
  description = "The instance class"
  value       = aws_db_instance.main.instance_class
}

output "db_instance_allocated_storage" {
  description = "The allocated storage in GB"
  value       = aws_db_instance.main.allocated_storage
}

output "db_instance_storage_encrypted" {
  description = "Whether storage is encrypted"
  value       = aws_db_instance.main.storage_encrypted
}

output "db_instance_kms_key_id" {
  description = "The KMS key ID for encryption"
  value       = aws_db_instance.main.kms_key_id
}

output "db_subnet_group_name" {
  description = "The DB subnet group name"
  value       = aws_db_subnet_group.main.name
}

output "db_parameter_group_name" {
  description = "The DB parameter group name"
  value       = aws_db_parameter_group.main.name
}

output "db_option_group_name" {
  description = "The DB option group name"
  value       = aws_db_option_group.main.name
}

output "read_replica_id" {
  description = "The ID of the read replica (if enabled)"
  value       = var.create_read_replica ? aws_db_instance.read_replica[0].id : null
}

output "read_replica_arn" {
  description = "The ARN of the read replica (if enabled)"
  value       = var.create_read_replica ? aws_db_instance.read_replica[0].arn : null
}

output "read_replica_endpoint" {
  description = "The connection endpoint for the read replica (if enabled)"
  value       = var.create_read_replica ? aws_db_instance.read_replica[0].endpoint : null
}

output "read_replica_address" {
  description = "The read replica address (if enabled)"
  value       = var.create_read_replica ? aws_db_instance.read_replica[0].address : null
}

output "security_group_ids" {
  description = "List of security group IDs attached to the database"
  value       = aws_db_instance.main.vpc_security_group_ids
}

output "ca_cert_identifier" {
  description = "The CA certificate identifier"
  value       = aws_db_instance.main.ca_cert_identifier
}

output "performance_insights_enabled" {
  description = "Whether Performance Insights is enabled"
  value       = aws_db_instance.main.performance_insights_enabled
}

output "performance_insights_kms_key_id" {
  description = "The KMS key ID for Performance Insights encryption"
  value       = aws_db_instance.main.performance_insights_kms_key_id
}

output "enhanced_monitoring_role_arn" {
  description = "The IAM role ARN for enhanced monitoring"
  value       = aws_iam_role.enhanced_monitoring.arn
}

output "backup_retention_period" {
  description = "The backup retention period in days"
  value       = aws_db_instance.main.backup_retention_period
}

output "preferred_backup_window" {
  description = "The preferred backup window"
  value       = aws_db_instance.main.preferred_backup_window
}

output "preferred_maintenance_window" {
  description = "The preferred maintenance window"
  value       = aws_db_instance.main.preferred_maintenance_window
}

output "deletion_protection" {
  description = "Whether deletion protection is enabled"
  value       = aws_db_instance.main.deletion_protection
}

output "multi_az" {
  description = "Whether Multi-AZ is enabled"
  value       = aws_db_instance.main.multi_az
}

output "publicly_accessible" {
  description = "Whether the database is publicly accessible"
  value       = aws_db_instance.main.publicly_accessible
}

output "secret_arn" {
  description = "The ARN of the database credentials secret"
  value       = aws_secretsmanager_secret.db_credentials.arn
}

output "secret_name" {
  description = "The name of the database credentials secret"
  value       = aws_secretsmanager_secret.db_credentials.name
}