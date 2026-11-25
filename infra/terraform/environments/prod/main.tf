# Production Environment Configuration

module "infrastructure" {
  source = "../../"

  environment = "prod"
  aws_region  = "us-east-1"

  # VPC - Full size for production
  vpc_cidr = "10.0.0.0/16"
  public_subnet_cidrs  = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  private_subnet_cidrs = ["10.0.11.0/24", "10.0.12.0/24", "10.0.13.0/24"]
  database_subnet_cidrs = ["10.0.21.0/24", "10.0.22.0/24", "10.0.23.0/24"]

  # RDS - Production instance with replica
  db_engine_version        = "15.4"
  db_instance_class        = "db.r6g.xlarge"
  db_allocated_storage     = 200
  db_max_allocated_storage = 1000
  db_backup_retention_period = 30
  db_deletion_protection   = true

  # Redis - Cluster with replicas for production
  redis_engine_version = "7.1"
  redis_node_type      = "cache.r6g.large"
  redis_num_cache_nodes = 3

  # ECS - Production resources with auto-scaling
  backend_service = {
    desired_count = 3
    min_capacity  = 2
    max_capacity  = 20
    cpu           = 2048
    memory        = 4096
  }

  frontend_service = {
    desired_count = 3
    min_capacity  = 2
    max_capacity  = 20
    cpu           = 1024
    memory        = 2048
  }

  worker_service = {
    desired_count = 4
    min_capacity  = 2
    max_capacity  = 50
    cpu           = 4096
    memory        = 8192
  }

  # Images - Use production tags (semantic versioning)
  backend_image  = "clipyantra/backend:v1.0.0"
  frontend_image = "clipyantra/frontend:v1.0.0"
  worker_image   = "clipyantra/worker:v1.0.0"

  # Secrets - Production values from Secrets Manager
  secret_key      = var.secret_key
  jwt_secret_key  = var.jwt_secret_key
  encryption_key  = var.encryption_key
  db_password     = var.db_password
  redis_password  = var.redis_password

  # Domain
  cors_origins = ["https://clipyantra.com", "https://www.clipyantra.com"]
  domain_name  = "clipyantra.com"
  acm_certificate_arn = var.acm_certificate_arn

  # Logging
  log_retention_days = 90

  common_tags = {
    Environment = "production"
    Team        = "platform"
    Criticality = "high"
  }
}

# Variables for production (must be passed via TF_VAR_* or secure tfvars)
variable "secret_key" {
  type      = string
  sensitive = true
}

variable "jwt_secret_key" {
  type      = string
  sensitive = true
}

variable "encryption_key" {
  type      = string
  sensitive = true
}

variable "db_password" {
  type      = string
  sensitive = true
}

variable "redis_password" {
  type      = string
  sensitive = true
}

variable "acm_certificate_arn" {
  type = string
}