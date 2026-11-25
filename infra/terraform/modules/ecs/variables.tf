# ECS Module Variables

variable "environment" {
  description = "Environment name"
  type        = string
}

variable "cluster_name" {
  description = "ECS cluster name"
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

variable "public_subnet_ids" {
  description = "Public subnet IDs"
  type        = list(string)
}

variable "security_group_ids" {
  description = "Security group IDs for ECS tasks"
  type        = list(string)
}

variable "alb_security_group_id" {
  description = "ALB security group ID"
  type        = string
}

variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "enable_container_insights" {
  description = "Enable Container Insights"
  type        = bool
  default     = true
}

variable "log_retention_days" {
  description = "Log retention days"
  type        = number
  default     = 30
}

variable "access_logs_bucket" {
  description = "S3 bucket for ALB access logs"
  type        = string
  default     = ""
}

variable "acm_certificate_arn" {
  description = "ACM certificate ARN for HTTPS"
  type        = string
  default     = ""
}

variable "backend_image" {
  description = "Backend Docker image URI"
  type        = string
}

variable "frontend_image" {
  description = "Frontend Docker image URI"
  type        = string
}

variable "worker_image" {
  description = "Worker Docker image URI"
  type        = string
}

variable "backend_service" {
  description = "Backend service configuration"
  type = object({
    desired_count = number
    min_capacity  = number
    max_capacity  = number
    cpu           = number
    memory        = number
  })
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
}

variable "backend_task_definition" {
  description = "Backend task definition configuration"
  type = object({
    family                = string
    container_port        = number
    health_check_path     = string
    environment_variables = map(string)
    secrets               = list(string)
    log_configuration     = map(string)
  })
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
}

variable "secrets_prefix" {
  description = "Secrets Manager prefix"
  type        = string
  default     = ""
}

variable "media_policy_arn" {
  description = "Media access policy ARN"
  type        = string
  default     = ""
}

variable "tags" {
  description = "Tags for resources"
  type        = map(string)
  default     = {}
}