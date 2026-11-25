# ElastiCache Redis Module for ClipYantra

# Redis Subnet Group
resource "aws_elasticache_subnet_group" "main" {
  name       = "${var.environment}-clipyantra-redis-subnet"
  subnet_ids = var.private_subnet_ids

  tags = merge(var.tags, {
    Name = "${var.environment}-clipyantra-redis-subnet"
  })
}

# Redis Parameter Group
resource "aws_elasticache_parameter_group" "main" {
  name        = "${var.environment}-clipyantra-redis-pg"
  family      = var.parameter_group_family
  description = "Parameter group for ClipYantra Redis"

  parameter {
    name  = "maxmemory-policy"
    value = "allkeys-lru"
  }

  parameter {
    name  = "timeout"
    value = "300"
  }

  parameter {
    name  = "tcp-keepalive"
    value = "60"
  }

  tags = merge(var.tags, {
    Name = "${var.environment}-clipyantra-redis-pg"
  })
}

# Redis Security Group
resource "aws_security_group" "redis" {
  name        = "${var.environment}-clipyantra-redis-sg"
  description = "Security group for ElastiCache Redis"
  vpc_id      = var.vpc_id

  ingress {
    from_port       = 6379
    to_port         = 6379
    protocol        = "tcp"
    security_groups = var.security_group_ids
  }

  tags = merge(var.tags, {
    Name = "${var.environment}-clipyantra-redis-sg"
  })
}

# Redis Replication Group (for production with replicas)
resource "aws_elasticache_replication_group" "main" {
  count = var.num_cache_nodes > 1 ? 1 : 0

  replication_group_id       = "${var.environment}-clipyantra-redis"
  replication_group_description = "ClipYantra Redis Cluster - ${var.environment}"

  engine               = "redis"
  engine_version       = var.engine_version
  node_type            = var.node_type
  number_cache_clusters = var.num_cache_nodes
  parameter_group_name = aws_elasticache_parameter_group.main.name
  port                 = 6379

  subnet_group_name    = aws_elasticache_subnet_group.main.name
  security_group_ids   = [aws_security_group.redis.id]

  automatic_failover_enabled = true
  multi_az_enabled           = var.environment == "prod"

  at_rest_encryption_enabled = true
  transit_encryption_enabled = true
  auth_token                 = var.auth_token

  snapshot_retention_limit = 7
  snapshot_window          = "03:00-04:00"
  maintenance_window       = "sun:05:00-sun:06:00"

  tags = merge(var.tags, {
    Name = "${var.environment}-clipyantra-redis"
  })
}

# Redis Cluster (single node for dev/staging)
resource "aws_elasticache_cluster" "main" {
  count = var.num_cache_nodes == 1 ? 1 : 0

  cluster_id           = "${var.environment}-clipyantra-redis"
  engine               = "redis"
  engine_version       = var.engine_version
  node_type            = var.node_type
  num_cache_nodes      = 1
  parameter_group_name = aws_elasticache_parameter_group.main.name
  port                 = 6379

  subnet_group_name  = aws_elasticache_subnet_group.main.name
  security_group_ids = [aws_security_group.redis.id]

  at_rest_encryption_enabled = true
  transit_encryption_enabled = true
  auth_token                 = var.auth_token

  snapshot_retention_limit = 7
  snapshot_window          = "03:00-04:00"
  maintenance_window       = "sun:05:00-sun:06:00"

  tags = merge(var.tags, {
    Name = "${var.environment}-clipyantra-redis"
  })
}

# Outputs
output "cache_endpoint" {
  value = var.num_cache_nodes > 1 ? aws_elasticache_replication_group.main[0].primary_endpoint_address : aws_elasticache_cluster.main[0].cache_nodes[0].address
}

output "cache_port" {
  value = var.num_cache_nodes > 1 ? aws_elasticache_replication_group.main[0].primary_endpoint_port : aws_elasticache_cluster.main[0].cache_nodes[0].port
}

output "replication_group_id" {
  value = var.num_cache_nodes > 1 ? aws_elasticache_replication_group.main[0].replication_group_id : null
}

output "cluster_id" {
  value = var.num_cache_nodes == 1 ? aws_elasticache_cluster.main[0].cluster_id : null
}

output "security_group_id" {
  value = aws_security_group.redis.id
}

output "parameter_group_name" {
  value = aws_elasticache_parameter_group.main.name
}

output "subnet_group_name" {
  value = aws_elasticache_subnet_group.main.name
}