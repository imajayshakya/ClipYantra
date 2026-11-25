# Redis (ElastiCache) Module Outputs

output "replication_group_id" {
  description = "The ID of the ElastiCache replication group (cluster mode)"
  value       = var.cluster_mode_enabled ? aws_elasticache_replication_group.main.id : null
}

output "replication_group_arn" {
  description = "The ARN of the ElastiCache replication group"
  value       = var.cluster_mode_enabled ? aws_elasticache_replication_group.main.arn : null
}

output "replication_group_primary_endpoint_address" {
  description = "The primary endpoint address (writer)"
  value       = var.cluster_mode_enabled ? aws_elasticache_replication_group.main.primary_endpoint_address : null
}

output "replication_group_primary_endpoint_port" {
  description = "The primary endpoint port"
  value       = var.cluster_mode_enabled ? aws_elasticache_replication_group.main.primary_endpoint_port : null
}

output "replication_group_reader_endpoint_address" {
  description = "The reader endpoint address"
  value       = var.cluster_mode_enabled ? aws_elasticache_replication_group.main.reader_endpoint_address : null
}

output "replication_group_reader_endpoint_port" {
  description = "The reader endpoint port"
  value       = var.cluster_mode_enabled ? aws_elasticache_replication_group.main.reader_endpoint_port : null
}

output "replication_group_configuration_endpoint_address" {
  description = "The configuration endpoint address"
  value       = var.cluster_mode_enabled ? aws_elasticache_replication_group.main.configuration_endpoint_address : null
}

output "replication_group_configuration_endpoint_port" {
  description = "The configuration endpoint port"
  value       = var.cluster_mode_enabled ? aws_elasticache_replication_group.main.configuration_endpoint_port : null
}

output "replication_group_member_clusters" {
  description = "List of member cluster IDs"
  value       = var.cluster_mode_enabled ? aws_elasticache_replication_group.main.member_clusters : null
}

output "replication_group_node_type" {
  description = "The node type of the replication group"
  value       = var.cluster_mode_enabled ? aws_elasticache_replication_group.main.node_type : null
}

output "replication_group_engine_version" {
  description = "The Redis engine version"
  value       = var.cluster_mode_enabled ? aws_elasticache_replication_group.main.engine_version : null
}

output "replication_group_port" {
  description = "The Redis port"
  value       = var.cluster_mode_enabled ? aws_elasticache_replication_group.main.port : null
}

output "replication_group_auth_token_enabled" {
  description = "Whether auth token is enabled"
  value       = var.cluster_mode_enabled ? aws_elasticache_replication_group.main.auth_token_enabled : null
}

output "replication_group_transit_encryption_enabled" {
  description = "Whether in-transit encryption is enabled"
  value       = var.cluster_mode_enabled ? aws_elasticache_replication_group.main.transit_encryption_enabled : null
}

output "replication_group_at_rest_encryption_enabled" {
  description = "Whether at-rest encryption is enabled"
  value       = var.cluster_mode_enabled ? aws_elasticache_replication_group.main.at_rest_encryption_enabled : null
}

output "replication_group_automatic_failover_enabled" {
  description = "Whether automatic failover is enabled"
  value       = var.cluster_mode_enabled ? aws_elasticache_replication_group.main.automatic_failover_enabled : null
}

output "replication_group_multi_az_enabled" {
  description = "Whether Multi-AZ is enabled"
  value       = var.cluster_mode_enabled ? aws_elasticache_replication_group.main.multi_az_enabled : null
}

output "replication_group_kms_key_id" {
  description = "The KMS key ID for at-rest encryption"
  value       = var.cluster_mode_enabled ? aws_elasticache_replication_group.main.kms_key_id : null
}

output "replication_group_security_group_ids" {
  description = "List of security group IDs"
  value       = var.cluster_mode_enabled ? aws_elasticache_replication_group.main.security_group_ids : null
}

output "replication_group_subnet_group_name" {
  description = "The subnet group name"
  value       = var.cluster_mode_enabled ? aws_elasticache_replication_group.main.subnet_group_name : null
}

output "replication_group_parameter_group_name" {
  description = "The parameter group name"
  value       = var.cluster_mode_enabled ? aws_elasticache_replication_group.main.parameter_group_name : null
}

# Single-node cluster outputs (non-cluster mode)
output "cluster_id" {
  description = "The ID of the ElastiCache cluster (single node)"
  value       = !var.cluster_mode_enabled ? aws_elasticache_cluster.main.id : null
}

output "cluster_arn" {
  description = "The ARN of the ElastiCache cluster"
  value       = !var.cluster_mode_enabled ? aws_elasticache_cluster.main.arn : null
}

output "cluster_endpoint_address" {
  description = "The cluster endpoint address"
  value       = !var.cluster_mode_enabled ? aws_elasticache_cluster.main.cache_nodes[0].address : null
}

output "cluster_endpoint_port" {
  description = "The cluster endpoint port"
  value       = !var.cluster_mode_enabled ? aws_elasticache_cluster.main.cache_nodes[0].port : null
}

output "cluster_node_type" {
  description = "The node type of the cluster"
  value       = !var.cluster_mode_enabled ? aws_elasticache_cluster.main.node_type : null
}

output "cluster_engine_version" {
  description = "The Redis engine version"
  value       = !var.cluster_mode_enabled ? aws_elasticache_cluster.main.engine_version : null
}

output "cluster_port" {
  description = "The Redis port"
  value       = !var.cluster_mode_enabled ? aws_elasticache_cluster.main.port : null
}

output "cluster_auth_token_enabled" {
  description = "Whether auth token is enabled"
  value       = !var.cluster_mode_enabled ? aws_elasticache_cluster.main.auth_token_enabled : null
}

output "cluster_transit_encryption_enabled" {
  description = "Whether in-transit encryption is enabled"
  value       = !var.cluster_mode_enabled ? aws_elasticache_cluster.main.transit_encryption_enabled : null
}

output "cluster_at_rest_encryption_enabled" {
  description = "Whether at-rest encryption is enabled"
  value       = !var.cluster_mode_enabled ? aws_elasticache_cluster.main.at_rest_encryption_enabled : null
}

output "cluster_security_group_ids" {
  description = "List of security group IDs"
  value       = !var.cluster_mode_enabled ? aws_elasticache_cluster.main.security_group_ids : null
}

output "cluster_subnet_group_name" {
  description = "The subnet group name"
  value       = !var.cluster_mode_enabled ? aws_elasticache_cluster.main.subnet_group_name : null
}

output "cluster_parameter_group_name" {
  description = "The parameter group name"
  value       = !var.cluster_mode_enabled ? aws_elasticache_cluster.main.parameter_group_name : null
}

output "cluster_num_cache_nodes" {
  description = "Number of cache nodes"
  value       = !var.cluster_mode_enabled ? aws_elasticache_cluster.main.num_cache_nodes : null
}

output "cluster_preferred_maintenance_window" {
  description = "The preferred maintenance window"
  value       = !var.cluster_mode_enabled ? aws_elasticache_cluster.main.preferred_maintenance_window : null
}

output "cluster_snapshot_retention_limit" {
  description = "The snapshot retention limit in days"
  value       = !var.cluster_mode_enabled ? aws_elasticache_cluster.main.snapshot_retention_limit : null
}

output "cluster_snapshot_window" {
  description = "The snapshot window"
  value       = !var.cluster_mode_enabled ? aws_elasticache_cluster.main.snapshot_window : null
}

# Unified outputs (works for both modes)
output "primary_endpoint_address" {
  description = "Primary endpoint address (writer) - works for both modes"
  value       = var.cluster_mode_enabled ? aws_elasticache_replication_group.main.primary_endpoint_address : aws_elasticache_cluster.main.cache_nodes[0].address
}

output "primary_endpoint_port" {
  description = "Primary endpoint port - works for both modes"
  value       = var.cluster_mode_enabled ? aws_elasticache_replication_group.main.primary_endpoint_port : aws_elasticache_cluster.main.cache_nodes[0].port
}

output "reader_endpoint_address" {
  description = "Reader endpoint address - works for both modes (same as primary for single node)"
  value       = var.cluster_mode_enabled ? aws_elasticache_replication_group.main.reader_endpoint_address : aws_elasticache_cluster.main.cache_nodes[0].address
}

output "reader_endpoint_port" {
  description = "Reader endpoint port - works for both modes (same as primary for single node)"
  value       = var.cluster_mode_enabled ? aws_elasticache_replication_group.main.reader_endpoint_port : aws_elasticache_cluster.main.cache_nodes[0].port
}

output "redis_port" {
  description = "Redis port - works for both modes"
  value       = var.cluster_mode_enabled ? aws_elasticache_replication_group.main.port : aws_elasticache_cluster.main.port
}

output "engine_version" {
  description = "Redis engine version - works for both modes"
  value       = var.cluster_mode_enabled ? aws_elasticache_replication_group.main.engine_version : aws_elasticache_cluster.main.engine_version
}

output "node_type" {
  description = "Node type - works for both modes"
  value       = var.cluster_mode_enabled ? aws_elasticache_replication_group.main.node_type : aws_elasticache_cluster.main.node_type
}

output "auth_token_enabled" {
  description = "Whether auth token is enabled - works for both modes"
  value       = var.cluster_mode_enabled ? aws_elasticache_replication_group.main.auth_token_enabled : aws_elasticache_cluster.main.auth_token_enabled
}

output "transit_encryption_enabled" {
  description = "Whether in-transit encryption is enabled - works for both modes"
  value       = var.cluster_mode_enabled ? aws_elasticache_replication_group.main.transit_encryption_enabled : aws_elasticache_cluster.main.transit_encryption_enabled
}

output "at_rest_encryption_enabled" {
  description = "Whether at-rest encryption is enabled - works for both modes"
  value       = var.cluster_mode_enabled ? aws_elasticache_replication_group.main.at_rest_encryption_enabled : aws_elasticache_cluster.main.at_rest_encryption_enabled
}

output "security_group_ids" {
  description = "Security group IDs - works for both modes"
  value       = var.cluster_mode_enabled ? aws_elasticache_replication_group.main.security_group_ids : aws_elasticache_cluster.main.security_group_ids
}

output "subnet_group_name" {
  description = "Subnet group name - works for both modes"
  value       = var.cluster_mode_enabled ? aws_elasticache_replication_group.main.subnet_group_name : aws_elasticache_cluster.main.subnet_group_name
}

output "parameter_group_name" {
  description = "Parameter group name - works for both modes"
  value       = var.cluster_mode_enabled ? aws_elasticache_replication_group.main.parameter_group_name : aws_elasticache_cluster.main.parameter_group_name
}

output "kms_key_id" {
  description = "KMS key ID for at-rest encryption - works for both modes"
  value       = var.cluster_mode_enabled ? aws_elasticache_replication_group.main.kms_key_id : null
}

output "subnet_group_id" {
  description = "The ID of the ElastiCache subnet group"
  value       = aws_elasticache_subnet_group.main.id
}

output "subnet_group_arn" {
  description = "The ARN of the ElastiCache subnet group"
  value       = aws_elasticache_subnet_group.main.arn
}

output "subnet_group_description" {
  description = "The description of the ElastiCache subnet group"
  value       = aws_elasticache_subnet_group.main.description
}

output "subnet_ids" {
  description = "List of subnet IDs in the subnet group"
  value       = aws_elasticache_subnet_group.main.subnet_ids
}

output "parameter_group_id" {
  description = "The ID of the ElastiCache parameter group"
  value       = aws_elasticache_parameter_group.main.id
}

output "parameter_group_arn" {
  description = "The ARN of the ElastiCache parameter group"
  value       = aws_elasticache_parameter_group.main.arn
}

output "parameter_group_family" {
  description = "The parameter group family"
  value       = aws_elasticache_parameter_group.main.family
}

output "parameter_group_description" {
  description = "The parameter group description"
  value       = aws_elasticache_parameter_group.main.description
}