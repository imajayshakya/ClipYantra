# Staging Environment Configuration

module "infrastructure" {
  source = "../../"

  environment = "staging"
  aws_region  = "us-east-1"

  # VPC
  vpc_cidr = "10.2.0.0/16"
  public_subnet_cidrs  = ["10.2.1.0/24", "10.2.2.0/24", "10.2.3.0/24"]
  private_subnet_cidrs = ["10.2.11.0/24", "10.2.12.0/24", "10.2.13.0/24"]
  database_subnet_cidrs = ["10.2.21.0/24", "10.2.22.0/24", "10.2.23.0/24"]

  # RDS - Medium instance for staging
  db_engine_version        = "15.4"
  db_instance_class        = "db.t3.small"
  db_allocated_storage     = 50
  db_max_allocated_storage = 200
  db_backup_retention_period = 7
  db_deletion_protection   = true

  # Redis - Single node for staging
  redis_engine_version = "7.1"
  redis_node_type      = "cache.t3.small"
  redis_num_cache_nodes = 1

  # ECS - Moderate resources for staging
  backend_service = {
    desired_count = 2
    min_capacity  = 1
    max_capacity  = 4
    cpu           = 512
    memory        = 1024
  }

  frontend_service = {
    desired_count = 2
    min_capacity  = 1
    max_capacity  = 4
    cpu           = 256
    memory        = 512
  }

  worker_service = {
    desired_count = 2
    min_capacity  = 1
    max_capacity  = 6
    cpu           = 1024
    memory        = 2048
  }

  # Images - Use staging tags
  backend_image  = "clipyantra/backend:staging"
  frontend_image = "clipyantra/frontend:staging"
  worker_image   = "clipyantra/worker:staging"

  # Secrets - Staging values (should be from parameter store/secrets manager in reality)
  secret_key      = var.secret_key
  jwt_secret_key  = var.jwt_secret_key
  encryption_key  = var.encryption_key
  db_password     = var.db_password
  redis_password  = var.redis_password

  # Domain
  cors_origins = ["https://staging.clipyantra.com"]
  domain_name  = "staging.clipyantra.com"
  acm_certificate_arn = var.acm_certificate_arn

  # Logging
  log_retention_days = 14

  common_tags = {
    Environment = "staging"
    Team        = "platform"
  }
}

# Variables for staging (would be passed via TF_VAR_* or tfvars file)
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
  default = ""
}