# RDS Module for ClipYantra

# DB Subnet Group
resource "aws_db_subnet_group" "main" {
  name       = "${var.environment}-clipyantra-db-subnet-group"
  subnet_ids = var.database_subnet_ids

  tags = merge(var.tags, {
    Name = "${var.environment}-clipyantra-db-subnet-group"
  })
}

# DB Parameter Group
resource "aws_db_parameter_group" "main" {
  name        = "${var.environment}-clipyantra-db-pg"
  family      = "postgres15"
  description = "Parameter group for ClipYantra PostgreSQL"

  parameter {
    name  = "shared_preload_libraries"
    value = "pg_stat_statements,auto_explain"
  }

  parameter {
    name  = "track_activity_query_size"
    value = "4096"
  }

  parameter {
    name  = "log_min_duration_statement"
    value = "1000"
  }

  parameter {
    name  = "idle_in_transaction_session_timeout"
    value = "300000"
  }

  tags = merge(var.tags, {
    Name = "${var.environment}-clipyantra-db-pg"
  })
}

# RDS Instance
resource "aws_db_instance" "main" {
  identifier             = "${var.environment}-clipyantra-db"
  engine                 = "postgres"
  engine_version         = var.engine_version
  instance_class         = var.instance_class
  allocated_storage      = var.allocated_storage
  max_allocated_storage  = var.max_allocated_storage
  storage_type           = "gp3"
  storage_encrypted      = true

  db_name  = var.db_name
  username = var.username
  password = var.password

  vpc_security_group_ids = var.security_group_ids
  db_subnet_group_name   = aws_db_subnet_group.main.name
  parameter_group_name   = aws_db_parameter_group.main.name

  backup_retention_period = var.backup_retention_period
  backup_window           = "03:00-04:00"
  maintenance_window      = "sun:04:00-sun:05:00"

  deletion_protection = var.deletion_protection
  skip_final_snapshot = false
  final_snapshot_identifier = "${var.environment}-clipyantra-db-final-snapshot-${formatdate("YYYY-MM-DD-hhmm", timestamp())}"

  performance_insights_enabled = true
  monitoring_interval         = 60
  monitoring_role_arn         = aws_iam_role.rds_monitoring.arn

  enabled_cloudwatch_logs_exports = ["postgresql", "upgrade"]

  tags = merge(var.tags, {
    Name = "${var.environment}-clipyantra-db"
  })
}

# IAM Role for RDS Enhanced Monitoring
resource "aws_iam_role" "rds_monitoring" {
  name = "${var.environment}-clipyantra-rds-monitoring"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "monitoring.rds.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "rds_monitoring" {
  role       = aws_iam_role.rds_monitoring.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonRDSEnhancedMonitoringRole"
}

# Read Replica (for production)
resource "aws_db_instance" "replica" {
  count = var.environment == "prod" ? 1 : 0

  identifier            = "${var.environment}-clipyantra-db-replica"
  replicate_source_db   = aws_db_instance.main.identifier
  instance_class        = var.instance_class
  parameter_group_name  = aws_db_parameter_group.main.name
  monitoring_interval   = 60
  monitoring_role_arn   = aws_iam_role.rds_monitoring.arn

  tags = merge(var.tags, {
    Name = "${var.environment}-clipyantra-db-replica"
  })
}

# Outputs
output "db_endpoint" {
  value = aws_db_instance.main.endpoint
}

output "db_port" {
  value = aws_db_instance.main.port
}

output "db_name" {
  value = var.db_name
}

output "db_username" {
  value = var.username
}

output "db_instance_arn" {
  value = aws_db_instance.main.arn
}

output "db_parameter_group_name" {
  value = aws_db_parameter_group.main.name
}

output "db_subnet_group_name" {
  value = aws_db_subnet_group.main.name
}

output "replica_endpoint" {
  value = var.environment == "prod" ? aws_db_instance.replica[0].endpoint : null
}