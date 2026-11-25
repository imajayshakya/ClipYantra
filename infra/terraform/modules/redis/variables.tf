# Redis Module Variables

variable "environment" {
  description = "Environment name"
  type        = string
}

variable "vpc_id" {
  description = "VPC ID"
  type        = string
}

variable "private_subnet_ids" {
  description = "Private subnet IDs"
  type        = list(string)
}

variable "security_group_ids" {
  description = "Security group IDs for Redis access"
  type        = list(string)
}

variable "engine_version" {
  description = "Redis engine version"
  type        = string
  default     = "7.1"
}

variable "node_type" {
  description = "ElastiCache node type"
  type        = string
  default     = "cache.t3.medium"
}

variable "num_cache_nodes" {
  description = "Number of cache nodes"
  type        = number
  default     = 1
}

variable "parameter_group_family" {
  description = "Parameter group family"
  type        = string
  default     = "redis7"
}

variable "parameter_group_name" {
  description = "Parameter group name"
  type        = string
  default     = "default.redis7"
}

variable "auth_token" {
  description = "Redis auth token"
  type        = string
  sensitive   = true
}

variable "tags" {
  description = "Tags for resources"
  type        = map(string)
  default     = {}
}