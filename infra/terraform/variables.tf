# ClipYantra Terraform Variables

# =============================================================================
# General Configuration
# =============================================================================

variable "aws_region" {
  description = "AWS region for resources"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Environment name (dev, staging, prod)"
  type        = string
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}

variable "common_tags" {
  description = "Common tags for all resources"
  type        = map(string)
  default     = {}
}

# =============================================================================
# VPC Configuration
# =============================================================================

variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "public_subnet_cidrs" {
  description = "CIDR blocks for public subnets"
  type        = list(string)
  default     = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
}

variable "private_subnet_cidrs" {
  description = "CIDR blocks for private subnets"
  type        = list(string)
  default     = ["10.0.11.0/24", "10.0.12.0/24", "10.0.13.0/24"]
}

variable "database_subnet_cidrs" {
  description = "CIDR blocks for database subnets"
  type        = list(string)
  default     = ["10.0.21.0/24", "10.0.22.0/24", "10.0.23.0/24"]
}

# =============================================================================
# RDS Configuration
# =============================================================================

variable "db_engine_version" {
  description = "PostgreSQL engine version"
  type        = string
  default     = "15.4"
}

variable "db_instance_class" {
  description = "RDS instance class"
  type        = string
  default     = "db.t3.medium"
}

variable "db_allocated_storage" {
  description = "Initial allocated storage in GB"
  type        = number
  default     = 100
}

variable "db_max_allocated_storage" {
  description = "Maximum allocated storage in GB for autoscaling"
  type        = number
  default     = 500
}

variable "db_name" {
  description = "Database name"
  type        = string
  default     = "clipyantra"
}

variable "db_username" {
  description = "Database master username"
  type        = string
  default     = "clipyantra"
}

variable "db_password" {
  description = "Database master password"
  type        = string
  sensitive   = true
}

variable "db_backup_retention_period" {
  description = "Backup retention period in days"
  type        = number
  default     = 7
}

variable "db_deletion_protection" {
  description = "Enable deletion protection"
  type        = bool
  default     = true
}

# =============================================================================
# Redis Configuration
# =============================================================================

variable "redis_engine_version" {
  description = "Redis engine version"
  type        = string
  default     = "7.1"
}

variable "redis_node_type" {
  description = "ElastiCache node type"
  type        = string
  default     = "cache.t3.medium"
}

variable "redis_num_cache_nodes" {
  description = "Number of cache nodes (1 for dev, 2+ for prod with replication)"
  type        = number
  default     = 1
}

variable "redis_parameter_group_name" {
  description = "Redis parameter group name"
  type        = string
  default     = "default.redis7"
}

variable "redis_password" {
  description = "Redis auth password"
  type        = string
  sensitive   = true
}

# =============================================================================
# ECS Configuration
# =============================================================================

variable "backend_service" {
  description = "Backend service configuration"
  type = object({
    desired_count = number
    min_capacity  = number
    max_capacity  = number
    cpu           = number
    memory        = number
  })
  default = {
    desired_count = 2
    min_capacity  = 1
    max_capacity  = 10
    cpu           = 1024
    memory        = 2048
  }
}

variable "frontend_service" {
  description = "Frontend service configuration"
  type = object({
    desired_count = number
    min_capacity  = number
    max_capacity  = number
    cpu           = number
    memory        = number
  })
  default = {
    desired_count = 2
    min_capacity  = 1
    max_capacity  = 10
    cpu           = 512
    memory        = 1024
  }
}

variable "worker_service" {
  description = "Worker service configuration"
  type = object({
    desired_count = number
    min_capacity  = number
    max_capacity  = number
    cpu           = number
    memory        = number
  })
  default = {
    desired_count = 2
    min_capacity  = 1
    max_capacity  = 20
    cpu           = 2048
    memory        = 4096
  }
}

variable "backend_task_definition" {
  description = "Backend task definition configuration"
  type = object({
    family                   = string
    container_port           = number
    health_check_path        = string
    environment_variables    = map(string)
    secrets                  = list(string)
    log_configuration        = map(string)
  })
  default = {
    family                = "clipyantra-backend"
    container_port        = 8000
    health_check_path     = "/health"
    environment_variables = {}
    secrets               = []
    log_configuration     = {}
  }
}

variable "frontend_task_definition" {
  description = "Frontend task definition configuration"
  type = object({
    family                = string
    container_port        = number
    health_check_path     = string
    environment_variables = map(string)
    secrets               = list(string)
    log_configuration     = map(string)
  })
  default = {
    family                = "clipyantra-frontend"
    container_port        = 3000
    health_check_path     = "/"
    environment_variables = {}
    secrets               = []
    log_configuration     = {}
  }
}

variable "worker_task_definition" {
  description = "Worker task definition configuration"
  type = object({
    family                = string
    container_port        = number
    environment_variables = map(string)
    secrets               = list(string)
    log_configuration     = map(string)
  })
  default = {
    family                = "clipyantra-worker"
    container_port        = 8000
    environment_variables = {}
    secrets               = []
    log_configuration     = {}
  }
}

# =============================================================================
# Application Secrets
# =============================================================================

variable "secret_key" {
  description = "Django/Flask secret key"
  type        = string
  sensitive   = true
}

variable "jwt_secret_key" {
  description = "JWT signing secret"
  type        = string
  sensitive   = true
}

variable "encryption_key" {
  description = "Encryption key for sensitive data"
  type        = string
  sensitive   = true
}

# =============================================================================
# CORS & Domain
# =============================================================================

variable "cors_origins" {
  description = "Allowed CORS origins"
  type        = list(string)
  default     = ["http://localhost:3000"]
}

variable "domain_name" {
  description = "Primary domain name"
  type        = string
  default     = ""
}

# =============================================================================
# Monitoring & Logging
# =============================================================================

variable "log_retention_days" {
  description = "CloudWatch log retention in days"
  type        = number
  default     = 30
}

variable "enable_container_insights" {
  description = "Enable ECS Container Insights"
  type        = bool
  default     = true
}

# =============================================================================
# SSL Certificate
# =============================================================================

variable "acm_certificate_arn" {
  description = "ACM certificate ARN for custom domain"
  type        = string
  default     = ""
}