# ECS Module Outputs

output "cluster_id" {
  description = "The ID of the ECS cluster"
  value       = aws_ecs_cluster.main.id
}

output "cluster_arn" {
  description = "The ARN of the ECS cluster"
  value       = aws_ecs_cluster.main.arn
}

output "cluster_name" {
  description = "The name of the ECS cluster"
  value       = aws_ecs_cluster.main.name
}

output "alb_id" {
  description = "The ID of the Application Load Balancer"
  value       = aws_lb.main.id
}

output "alb_arn" {
  description = "The ARN of the Application Load Balancer"
  value       = aws_lb.main.arn
}

output "alb_dns_name" {
  description = "The DNS name of the ALB"
  value       = aws_lb.main.dns_name
}

output "alb_zone_id" {
  description = "The zone ID of the ALB"
  value       = aws_lb.main.zone_id
}

output "alb_security_group_id" {
  description = "The security group ID of the ALB"
  value       = aws_security_group.alb.id
}

output "http_listener_arn" {
  description = "The ARN of the HTTP listener (redirects to HTTPS)"
  value       = aws_lb_listener.http.arn
}

output "https_listener_arn" {
  description = "The ARN of the HTTPS listener"
  value       = aws_lb_listener.https.arn
}

output "target_group_backend_arn" {
  description = "The ARN of the backend target group"
  value       = aws_lb_target_group.backend.arn
}

output "target_group_backend_name" {
  description = "The name of the backend target group"
  value       = aws_lb_target_group.backend.name
}

output "target_group_frontend_arn" {
  description = "The ARN of the frontend target group"
  value       = aws_lb_target_group.frontend.arn
}

output "target_group_frontend_name" {
  description = "The name of the frontend target group"
  value       = aws_lb_target_group.frontend.name
}

output "ecs_task_execution_role_arn" {
  description = "The ARN of the ECS task execution role"
  value       = aws_iam_role.task_execution.arn
}

output "ecs_task_execution_role_name" {
  description = "The name of the ECS task execution role"
  value       = aws_iam_role.task_execution.name
}

output "ecs_task_role_arn" {
  description = "The ARN of the ECS task role"
  value       = aws_iam_role.task.arn
}

output "ecs_task_role_name" {
  description = "The name of the ECS task role"
  value       = aws_iam_role.task.name
}

output "service_backend_name" {
  description = "The name of the backend ECS service"
  value       = aws_ecs_service.backend.name
}

output "service_backend_arn" {
  description = "The ARN of the backend ECS service"
  value       = aws_ecs_service.backend.arn
}

output "service_frontend_name" {
  description = "The name of the frontend ECS service"
  value       = aws_ecs_service.frontend.name
}

output "service_frontend_arn" {
  description = "The ARN of the frontend ECS service"
  value       = aws_ecs_service.frontend.arn
}

output "service_worker_name" {
  description = "The name of the worker ECS service"
  value       = aws_ecs_service.worker.name
}

output "service_worker_arn" {
  description = "The ARN of the worker ECS service"
  value       = aws_ecs_service.worker.arn
}

output "task_definition_backend_arn" {
  description = "The ARN of the backend task definition"
  value       = aws_ecs_task_definition.backend.arn
}

output "task_definition_backend_family" {
  description = "The family of the backend task definition"
  value       = aws_ecs_task_definition.backend.family
}

output "task_definition_backend_revision" {
  description = "The revision of the backend task definition"
  value       = aws_ecs_task_definition.backend.revision
}

output "task_definition_frontend_arn" {
  description = "The ARN of the frontend task definition"
  value       = aws_ecs_task_definition.frontend.arn
}

output "task_definition_frontend_family" {
  description = "The family of the frontend task definition"
  value       = aws_ecs_task_definition.frontend.family
}

output "task_definition_frontend_revision" {
  description = "The revision of the frontend task definition"
  value       = aws_ecs_task_definition.frontend.revision
}

output "task_definition_worker_arn" {
  description = "The ARN of the worker task definition"
  value       = aws_ecs_task_definition.worker.arn
}

output "task_definition_worker_family" {
  description = "The family of the worker task definition"
  value       = aws_ecs_task_definition.worker.family
}

output "task_definition_worker_revision" {
  description = "The revision of the worker task definition"
  value       = aws_ecs_task_definition.worker.revision
}

output "cloudwatch_log_group_backend_arn" {
  description = "The ARN of the backend log group"
  value       = aws_cloudwatch_log_group.backend.arn
}

output "cloudwatch_log_group_backend_name" {
  description = "The name of the backend log group"
  value       = aws_cloudwatch_log_group.backend.name
}

output "cloudwatch_log_group_frontend_arn" {
  description = "The ARN of the frontend log group"
  value       = aws_cloudwatch_log_group.frontend.arn
}

output "cloudwatch_log_group_frontend_name" {
  description = "The name of the frontend log group"
  value       = aws_cloudwatch_log_group.frontend.name
}

output "cloudwatch_log_group_worker_arn" {
  description = "The ARN of the worker log group"
  value       = aws_cloudwatch_log_group.worker.arn
}

output "cloudwatch_log_group_worker_name" {
  description = "The name of the worker log group"
  value       = aws_cloudwatch_log_group.worker.name
}

output "autoscaling_policy_backend_cpu_arn" {
  description = "The ARN of the backend CPU autoscaling policy"
  value       = aws_appautoscaling_policy.backend_cpu.arn
}

output "autoscaling_policy_backend_memory_arn" {
  description = "The ARN of the backend memory autoscaling policy"
  value       = aws_appautoscaling_policy.backend_memory.arn
}

output "autoscaling_policy_frontend_cpu_arn" {
  description = "The ARN of the frontend CPU autoscaling policy"
  value       = aws_appautoscaling_policy.frontend_cpu.arn
}

output "autoscaling_policy_frontend_memory_arn" {
  description = "The ARN of the frontend memory autoscaling policy"
  value       = aws_appautoscaling_policy.frontend_memory.arn
}

output "autoscaling_policy_worker_cpu_arn" {
  description = "The ARN of the worker CPU autoscaling policy"
  value       = aws_appautoscaling_policy.worker_cpu.arn
}

output "autoscaling_policy_worker_memory_arn" {
  description = "The ARN of the worker memory autoscaling policy"
  value       = aws_appautoscaling_policy.worker_memory.arn
}

output "service_discovery_namespace_id" {
  description = "The ID of the service discovery namespace"
  value       = aws_service_discovery_private_dns_namespace.main.id
}

output "service_discovery_namespace_arn" {
  description = "The ARN of the service discovery namespace"
  value       = aws_service_discovery_private_dns_namespace.main.arn
}

output "service_discovery_service_backend_arn" {
  description = "The ARN of the backend service discovery service"
  value       = aws_service_discovery_service.backend.arn
}

output "service_discovery_service_frontend_arn" {
  description = "The ARN of the frontend service discovery service"
  value       = aws_service_discovery_service.frontend.arn
}

output "service_discovery_service_worker_arn" {
  description = "The ARN of the worker service discovery service"
  value       = aws_service_discovery_service.worker.arn
}