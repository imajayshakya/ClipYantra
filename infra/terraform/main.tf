# ClipYantra Infrastructure - Main Terraform Configuration
# AWS Infrastructure for ClipYantra Application

terraform {
  required_version = ">= 1.5.0"
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.0"
    }
    tls = {
      source  = "hashicorp/tls"
      version = "~> 4.0"
    }
  }

  backend "s3" {
    bucket         = "clipyantra-terraform-state"
    key            = "infrastructure/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
}

provider "aws" {
  region = var.aws_region
  
  default_tags {
    tags = {
      Project     = "ClipYantra"
      Environment = var.environment
      ManagedBy   = "Terraform"
      Owner       = "platform-team"
    }
  }
}

# Data sources
data "aws_availability_zones" "available" {
  state = "available"
}

data "aws_caller_identity" "current" {}

# Random suffix for unique resource names
resource "random_id" "suffix" {
  byte_length = 4
}

# VPC Module
module "vpc" {
  source = "./modules/vpc"
  
  environment       = var.environment
  vpc_cidr          = var.vpc_cidr
  public_subnet_cidrs  = var.public_subnet_cidrs
  private_subnet_cidrs = var.private_subnet_cidrs
  database_subnet_cidrs = var.database_subnet_cidrs
  availability_zones = data.aws_availability_zones.available.names
  
  tags = var.common_tags
}

# RDS Module
module "rds" {
  source = "./modules/rds"
  
  environment           = var.environment
  vpc_id                = module.vpc.vpc_id
  database_subnet_ids   = module.vpc.database_subnet_ids
  security_group_ids    = [module.vpc.database_sg_id]
  
  engine_version        = var.db_engine_version
  instance_class        = var.db_instance_class
  allocated_storage     = var.db_allocated_storage
  max_allocated_storage = var.db_max_allocated_storage
  
  db_name               = var.db_name
  username              = var.db_username
  password              = var.db_password
  
  backup_retention_period = var.db_backup_retention_period
  deletion_protection     = var.db_deletion_protection
  
  tags = var.common_tags
}

# ElastiCache Redis Module
module "redis" {
  source = "./modules/redis"
  
  environment         = var.environment
  vpc_id              = module.vpc.vpc_id
  private_subnet_ids  = module.vpc.private_subnet_ids
  security_group_ids  = [module.vpc.redis_sg_id]
  
  engine_version      = var.redis_engine_version
  node_type           = var.redis_node_type
  num_cache_nodes     = var.redis_num_cache_nodes
  parameter_group_name = var.redis_parameter_group_name
  
  tags = var.common_tags
}

# ECS Cluster Module
module "ecs" {
  source = "./modules/ecs"
  
  environment       = var.environment
  vpc_id            = module.vpc.vpc_id
  private_subnet_ids = module.vpc.private_subnet_ids
  security_group_ids = [module.vpc.ecs_sg_id]
  
  cluster_name      = "${var.environment}-clipyantra"
  
  # Service configurations
  backend_service = var.backend_service
  frontend_service = var.frontend_service
  worker_service  = var.worker_service
  
  # Task definitions
  backend_task_definition = var.backend_task_definition
  frontend_task_definition = var.frontend_task_definition
  worker_task_definition  = var.worker_task_definition
  
  tags = var.common_tags
}

# S3 Bucket for Media Storage
resource "aws_s3_bucket" "media" {
  bucket = "${var.environment}-clipyantra-media-${random_id.suffix.hex}"
  
  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }
  
  versioning {
    enabled = true
  }
  
  lifecycle_rule {
    id      = "cleanup-incomplete-multipart"
    enabled = true
    abort_incomplete_multipart_upload {
      days_after_initiation = 7
    }
  }
  
  cors_rule {
    allowed_headers = ["*"]
    allowed_methods = ["GET", "PUT", "POST", "DELETE", "HEAD"]
    allowed_origins = var.cors_origins
    expose_headers  = ["ETag"]
    max_age_seconds = 3600
  }
  
  tags = var.common_tags
}

resource "aws_s3_bucket_public_access_block" "media" {
  bucket = aws_s3_bucket.media.id
  
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# CloudFront Distribution for Media CDN
resource "aws_cloudfront_distribution" "media" {
  origin {
    domain_name = aws_s3_bucket.media.bucket_regional_domain_name
    origin_id   = "S3-${aws_s3_bucket.media.bucket}"
    
    s3_origin_config {
      origin_access_identity = aws_cloudfront_origin_access_identity.media.cloudfront_access_identity_path
    }
  }
  
  enabled             = true
  is_ipv6_enabled     = true
  comment             = "ClipYantra Media CDN - ${var.environment}"
  default_root_object = "index.html"
  
  default_cache_behavior {
    allowed_methods  = ["GET", "HEAD", "OPTIONS"]
    cached_methods   = ["GET", "HEAD"]
    
    target_origin_id = "S3-${aws_s3_bucket.media.bucket}"
    
    forwarded_values {
      query_string = false
      cookies {
        forward = "none"
      }
    }
    
    viewer_protocol_policy = "redirect-to-https"
    min_ttl                = 0
    default_ttl            = 86400
    max_ttl                = 31536000
    
    compress = true
  }
  
  price_class = "PriceClass_All"
  
  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }
  
  viewer_certificate {
    cloudfront_default_certificate = true
  }
  
  tags = var.common_tags
}

resource "aws_cloudfront_origin_access_identity" "media" {
  comment = "ClipYantra Media OAI - ${var.environment}"
}

# IAM Roles
resource "aws_iam_role" "ecs_task_execution" {
  name = "${var.environment}-clipyantra-ecs-task-execution"
  
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "ecs-tasks.amazonaws.com"
      }
    }]
  })
  
  tags = var.common_tags
}

resource "aws_iam_role_policy_attachment" "ecs_task_execution" {
  role       = aws_iam_role.ecs_task_execution.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

resource "aws_iam_role" "ecs_task" {
  name = "${var.environment}-clipyantra-ecs-task"
  
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "ecs-tasks.amazonaws.com"
      }
    }]
  })
  
  tags = var.common_tags
}

resource "aws_iam_policy" "media_access" {
  name = "${var.environment}-clipyantra-media-access"
  
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Action = [
        "s3:GetObject",
        "s3:PutObject",
        "s3:DeleteObject",
        "s3:ListBucket"
      ]
      Resource = [
        aws_s3_bucket.media.arn,
        "${aws_s3_bucket.media.arn}/*"
      ]
    }]
  })
  
  tags = var.common_tags
}

resource "aws_iam_role_policy_attachment" "media_access" {
  role       = aws_iam_role.ecs_task.name
  policy_arn = aws_iam_policy.media_access.arn
}

# Secrets Manager for sensitive values
resource "aws_secretsmanager_secret" "db_credentials" {
  name = "${var.environment}/clipyantra/db-credentials"
  
  tags = var.common_tags
}

resource "aws_secretsmanager_secret_version" "db_credentials" {
  secret_id = aws_secretsmanager_secret.db_credentials.id
  secret_string = jsonencode({
    username = var.db_username
    password = var.db_password
    host     = module.rds.db_endpoint
    port     = 5432
    dbname   = var.db_name
  })
}

resource "aws_secretsmanager_secret" "redis_credentials" {
  name = "${var.environment}/clipyantra/redis-credentials"
  
  tags = var.common_tags
}

resource "aws_secretsmanager_secret_version" "redis_credentials" {
  secret_id = aws_secretsmanager_secret.redis_credentials.id
  secret_string = jsonencode({
    host     = module.redis.cache_endpoint
    port     = 6379
    password = var.redis_password
  })
}

resource "aws_secretsmanager_secret" "app_secrets" {
  name = "${var.environment}/clipyantra/app-secrets"
  
  tags = var.common_tags
}

resource "aws_secretsmanager_secret_version" "app_secrets" {
  secret_id = aws_secretsmanager_secret.app_secrets.id
  secret_string = jsonencode({
    secret_key      = var.secret_key
    jwt_secret_key  = var.jwt_secret_key
    encryption_key  = var.encryption_key
  })
}

# CloudWatch Log Groups
resource "aws_cloudwatch_log_group" "backend" {
  name              = "/ecs/${var.environment}-clipyantra-backend"
  retention_in_days = var.log_retention_days
  tags              = var.common_tags
}

resource "aws_cloudwatch_log_group" "frontend" {
  name              = "/ecs/${var.environment}-clipyantra-frontend"
  retention_in_days = var.log_retention_days
  tags              = var.common_tags
}

resource "aws_cloudwatch_log_group" "worker" {
  name              = "/ecs/${var.environment}-clipyantra-worker"
  retention_in_days = var.log_retention_days
  tags              = var.common_tags
}

resource "aws_cloudwatch_log_group" "nginx" {
  name              = "/ecs/${var.environment}-clipyantra-nginx"
  retention_in_days = var.log_retention_days
  tags              = var.common_tags
}

# Outputs
output "vpc_id" {
  value       = module.vpc.vpc_id
  description = "VPC ID"
}

output "database_endpoint" {
  value       = module.rds.db_endpoint
  description = "RDS Database Endpoint"
  sensitive   = true
}

output "redis_endpoint" {
  value       = module.redis.cache_endpoint
  description = "ElastiCache Redis Endpoint"
}

output "ecs_cluster_name" {
  value       = module.ecs.cluster_name
  description = "ECS Cluster Name"
}

output "media_bucket_name" {
  value       = aws_s3_bucket.media.bucket
  description = "Media S3 Bucket Name"
}

output "cloudfront_domain" {
  value       = aws_cloudfront_distribution.media.domain_name
  description = "CloudFront Distribution Domain"
}