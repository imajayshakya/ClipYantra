# ClipYantra Terraform Outputs

# =============================================================================
# VPC Outputs
# =============================================================================

output "vpc_id" {
  description = "VPC ID"
  value       = module.vpc.vpc_id
}

output "vpc_cidr" {
  description = "VPC CIDR block"
  value       = module.vpc.vpc_cidr
}

output "public_subnet_ids" {
  description = "Public subnet IDs"
  value       = module.vpc.public_subnet_ids
}

output "private_subnet_ids" {
  description = "Private subnet IDs"
  value       = module.vpc.private_subnet_ids
}

output "database_subnet_ids" {
  description = "Database subnet IDs"
  value       = module.vpc.database_subnet_ids
}

output "vpc_security_group_ids" {
  description = "VPC security group IDs"
  value = {
    ecs        = module.vpc.ecs_sg_id
    rds        = module.vpc.database_sg_id
    redis      = module.vpc.redis_sg_id
    alb        = module.vpc.alb_sg_id
  }
}

# =============================================================================
# RDS Outputs
# =============================================================================

output "db_endpoint" {
  description = "RDS database endpoint"
  value       = module.rds.db_endpoint
  sensitive   = true
}

output "db_port" {
  description = "RDS database port"
  value       = module.rds.db_port
}

output "db_name" {
  description = "Database name"
  value       = module.rds.db_name
}

output "db_username" {
  description = "Database username"
  value       = module.rds.db_username
}

output "db_instance_arn" {
  description = "RDS instance ARN"
  value       = module.rds.db_instance_arn
}

output "db_parameter_group_name" {
  description = "RDS parameter group name"
  value       = module.rds.db_parameter_group_name
}

# =============================================================================
# Redis Outputs
# =============================================================================

output "redis_endpoint" {
  description = "ElastiCache Redis primary endpoint"
  value       = module.redis.cache_endpoint
}

output "redis_port" {
  description = "Redis port"
  value       = module.redis.cache_port
}

output "redis_replication_group_id" {
  description = "Redis replication group ID"
  value       = module.redis.replication_group_id
}

output "redis_security_group_id" {
  description = "Redis security group ID"
  value       = module.redis.security_group_id
}

# =============================================================================
# ECS Outputs
# =============================================================================

output "ecs_cluster_name" {
  description = "ECS cluster name"
  value       = module.ecs.cluster_name
}

output "ecs_cluster_arn" {
  description = "ECS cluster ARN"
  value       = module.ecs.cluster_arn
}

output "ecs_service_names" {
  description = "ECS service names"
  value = {
    backend  = module.ecs.backend_service_name
    frontend = module.ecs.frontend_service_name
    worker   = module.ecs.worker_service_name
  }
}

output "ecs_service_arns" {
  description = "ECS service ARNs"
  value = {
    backend  = module.ecs.backend_service_arn
    frontend = module.ecs.frontend_service_arn
    worker   = module.ecs.worker_service_arn
  }
}

output "ecs_task_definition_arns" {
  description = "ECS task definition ARNs"
  value = {
    backend  = module.ecs.backend_task_definition_arn
    frontend = module.ecs.frontend_task_definition_arn
    worker   = module.ecs.worker_task_definition_arn
  }
}

output "ecs_execution_role_arn" {
  description = "ECS task execution role ARN"
  value       = module.ecs.execution_role_arn
}

output "ecs_task_role_arn" {
  description = "ECS task role ARN"
  value       = module.ecs.task_role_arn
}

# =============================================================================
# ALB Outputs
# =============================================================================

output "alb_arn" {
  description = "Application Load Balancer ARN"
  value       = module.ecs.alb_arn
}

output "alb_dns_name" {
  description = "ALB DNS name"
  value       = module.ecs.alb_dns_name
}

output "alb_zone_id" {
  description = "ALB hosted zone ID"
  value       = module.ecs.alb_zone_id
}

output "alb_security_group_id" {
  description = "ALB security group ID"
  value       = module.ecs.alb_security_group_id
}

output "target_group_arns" {
  description = "Target group ARNs"
  value = {
    backend  = module.ecs.backend_target_group_arn
    frontend = module.ecs.frontend_target_group_arn
  }
}

# =============================================================================
# S3 & CloudFront Outputs
# =============================================================================

output "media_bucket_name" {
  description = "Media S3 bucket name"
  value       = aws_s3_bucket.media.bucket
}

output "media_bucket_arn" {
  description = "Media S3 bucket ARN"
  value       = aws_s3_bucket.media.arn
}

output "media_bucket_domain" {
  description = "Media S3 bucket regional domain"
  value       = aws_s3_bucket.media.bucket_regional_domain_name
}

output "cloudfront_distribution_id" {
  description = "CloudFront distribution ID"
  value       = aws_cloudfront_distribution.media.id
}

output "cloudfront_domain_name" {
  description = "CloudFront distribution domain name"
  value       = aws_cloudfront_distribution.media.domain_name
}

output "cloudfront_origin_access_identity" {
  description = "CloudFront OAI for S3 access"
  value       = aws_cloudfront_origin_access_identity.media.cloudfront_access_identity_path
}

# =============================================================================
# IAM Outputs
# =============================================================================

output "ecs_execution_role_name" {
  description = "ECS task execution role name"
  value       = aws_iam_role.ecs_task_execution.name
}

output "ecs_task_role_name" {
  description = "ECS task role name"
  value       = aws_iam_role.ecs_task.name
}

output "media_access_policy_arn" {
  description = "Media access policy ARN"
  value       = aws_iam_policy.media_access.arn
}

# =============================================================================
# Secrets Manager Outputs
# =============================================================================

output "db_credentials_secret_arn" {
  description = "Database credentials secret ARN"
  value       = aws_secretsmanager_secret.db_credentials.arn
}

output "redis_credentials_secret_arn" {
  description = "Redis credentials secret ARN"
  value       = aws_secretsmanager_secret.redis_credentials.arn
}

output "app_secrets_secret_arn" {
  description = "Application secrets secret ARN"
  value       = aws_secretsmanager_secret.app_secrets.arn
}

# =============================================================================
# CloudWatch Outputs
# =============================================================================

output "log_group_names" {
  description = "CloudWatch log group names"
  value = {
    backend  = aws_cloudwatch_log_group.backend.name
    frontend = aws_cloudwatch_log_group.frontend.name
    worker   = aws_cloudwatch_log_group.worker.name
    nginx    = aws_cloudwatch_log_group.nginx.name
  }
}

output "log_group_arns" {
  description = "CloudWatch log group ARNs"
  value = {
    backend  = aws_cloudwatch_log_group.backend.arn
    frontend = aws_cloudwatch_log_group.frontend.arn
    worker   = aws_cloudwatch_log_group.worker.arn
    nginx    = aws_cloudwatch_log_group.nginx.arn
  }
}

# =============================================================================
# Computed/Derived Outputs
# =============================================================================

output "database_url" {
  description = "Database connection URL (constructed)"
  value       = "postgresql+asyncpg://${module.rds.db_username}:${var.db_password}@${module.rds.db_endpoint}/${module.rds.db_name}"
  sensitive   = true
}

output "redis_url" {
  description = "Redis connection URL (constructed)"
  value       = "redis://:${var.redis_password}@${module.redis.cache_endpoint}:${module.redis.cache_port}/0"
  sensitive   = true
}

output "celery_broker_url" {
  description = "Celery broker URL"
  value       = "redis://:${var.redis_password}@${module.redis.cache_endpoint}:${module.redis.cache_port}/0"
  sensitive   = true
}

output "celery_result_backend_url" {
  description = "Celery result backend URL"
  value       = "redis://:${var.redis_password}@${module.redis.cache_endpoint}:${module.redis.cache_port}/1"
  sensitive   = true
}

output "media_cdn_url" {
  description = "Media CDN URL"
  value       = "https://${aws_cloudfront_distribution.media.domain_name}"
}

output "api_base_url" {
  description = "API base URL (via ALB)"
  value       = "https://${module.ecs.alb_dns_name}"
}

output "frontend_url" {
  description = "Frontend URL (via ALB)"
  value       = "https://${module.ecs.alb_dns_name}"
}

# =============================================================================
# Environment-Specific Outputs
# =============================================================================

output "environment" {
  description = "Current environment"
  value       = var.environment
}

output "aws_region" {
  description = "AWS region"
  value       = var.aws_region
}

output "account_id" {
  description = "AWS account ID"
  value       = data.aws_caller_identity.current.account_id
}