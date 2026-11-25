# VPC Module Outputs

output "vpc_id" {
  description = "The ID of the VPC"
  value       = aws_vpc.main.id
}

output "vpc_arn" {
  description = "The ARN of the VPC"
  value       = aws_vpc.main.arn
}

output "vpc_cidr_block" {
  description = "The CIDR block of the VPC"
  value       = aws_vpc.main.cidr_block
}

output "public_subnet_ids" {
  description = "List of public subnet IDs"
  value       = aws_subnet.public[*].id
}

output "public_subnet_arns" {
  description = "List of public subnet ARNs"
  value       = aws_subnet.public[*].arn
}

output "public_subnet_cidr_blocks" {
  description = "List of public subnet CIDR blocks"
  value       = aws_subnet.public[*].cidr_block
}

output "private_subnet_ids" {
  description = "List of private subnet IDs"
  value       = aws_subnet.private[*].id
}

output "private_subnet_arns" {
  description = "List of private subnet ARNs"
  value       = aws_subnet.private[*].arn
}

output "private_subnet_cidr_blocks" {
  description = "List of private subnet CIDR blocks"
  value       = aws_subnet.private[*].cidr_block
}

output "database_subnet_ids" {
  description = "List of database subnet IDs"
  value       = aws_subnet.database[*].id
}

output "database_subnet_arns" {
  description = "List of database subnet ARNs"
  value       = aws_subnet.database[*].arn
}

output "database_subnet_cidr_blocks" {
  description = "List of database subnet CIDR blocks"
  value       = aws_subnet.database[*].cidr_block
}

output "database_subnet_group_name" {
  description = "Name of the database subnet group"
  value       = aws_db_subnet_group.main.name
}

output "igw_id" {
  description = "Internet Gateway ID"
  value       = aws_internet_gateway.main.id
}

output "nat_gateway_ids" {
  description = "List of NAT Gateway IDs"
  value       = aws_nat_gateway.main[*].id
}

output "nat_gateway_public_ips" {
  description = "List of NAT Gateway public IPs"
  value       = aws_nat_gateway.main[*].public_ip
}

output "vpc_endpoint_s3_id" {
  description = "S3 VPC Endpoint ID"
  value       = aws_vpc_endpoint.s3.id
}

output "vpc_endpoint_ecr_api_id" {
  description = "ECR API VPC Endpoint ID"
  value       = aws_vpc_endpoint.ecr_api.id
}

output "vpc_endpoint_ecr_dkr_id" {
  description = "ECR Docker VPC Endpoint ID"
  value       = aws_vpc_endpoint.ecr_dkr.id
}

output "vpc_endpoint_cloudwatch_id" {
  description = "CloudWatch VPC Endpoint ID"
  value       = aws_vpc_endpoint.cloudwatch.id
}

output "vpc_endpoint_secretsmanager_id" {
  description = "Secrets Manager VPC Endpoint ID"
  value       = aws_vpc_endpoint.secretsmanager.id
}

output "security_group_alb_id" {
  description = "ALB Security Group ID"
  value       = aws_security_group.alb.id
}

output "security_group_ecs_tasks_id" {
  description = "ECS Tasks Security Group ID"
  value       = aws_security_group.ecs_tasks.id
}

output "security_group_rds_id" {
  description = "RDS Security Group ID"
  value       = aws_security_group.rds.id
}

output "security_group_redis_id" {
  description = "Redis Security Group ID"
  value       = aws_security_group.redis.id
}

output "availability_zones" {
  description = "List of availability zones used"
  value       = data.aws_availability_zones.available.names
}