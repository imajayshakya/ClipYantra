# Development Environment Configuration

module "infrastructure" {
  source = "../../"

  environment = "dev"
  aws_region  = "us-east-1"

  # VPC - Smaller CIDR for dev
  vpc_cidr = "10.1.0.0/16"
  public_subnet_cidrs  = ["10.1.1.0/24", "10.1.2.0/24"]
  private_subnet_cidrs = ["10.1.11.0/24", "10.1.12.0/24"]
  database_subnet_cidrs = ["10.1.21.0/24", "10.1.22.0/24"]

  # RDS - Small instance for dev
  db_engine_version        = "15.4"
  db_instance_class        = "db.t3.micro"
  db_allocated_storage     = 20
  db_max_allocated_storage = 100
  db_backup_retention_period = 1
  db_deletion_protection   = false

  # Redis - Single node for dev
  redis_engine_version = "7.1"
  redis_node_type      = "cache.t3.micro"
  redis_num_cache_nodes = 1

  # ECS - Minimal resources for dev
  backend_service = {
    desired_count = 1
    min_capacity  = 1
    max_capacity  = 2
    cpu           = 256
    memory        = 512
  }

  frontend_service = {
    desired_count = 1
    min_capacity  = 1
    max_capacity  = 2
    cpu           = 256
    memory        = 512
  }

  worker_service = {
    desired_count = 1
    min_capacity  = 1
    max_capacity  = 2
    cpu           = 512
    memory        = 1024
  }

  # Images - Use local/latest for dev
  backend_image  = "clipyantra/backend:dev"
  frontend_image = "clipyantra/frontend:dev"
  worker_image   = "clipyantra/worker:dev"

  # Secrets - Use dev values
  secret_key      = "dev-secret-key-not-for-production"
  jwt_secret_key  = "dev-jwt-secret-not-for-production"
  encryption_key  = "dev-encryption-key-not-for-production"
  db_password     = "dev-db-password"
  redis_password  = "dev-redis-password"

  # Domain
  cors_origins = ["http://localhost:3000", "http://dev.clipyantra.local"]
  domain_name  = "dev.clipyantra.local"

  # Logging
  log_retention_days = 7

  common_tags = {
    Environment = "development"
    Team        = "platform"
  }
}