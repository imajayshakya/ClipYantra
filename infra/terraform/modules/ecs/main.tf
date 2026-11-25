# ECS Module for ClipYantra

# ECS Cluster
resource "aws_ecs_cluster" "main" {
  name = var.cluster_name

  setting {
    name  = "containerInsights"
    value = var.enable_container_insights ? "enabled" : "disabled"
  }

  configuration {
    execute_command_configuration {
      logging = "OVERRIDE"
      log_configuration {
        cloud_watch_log_group_name = aws_cloudwatch_log_group.ecs_exec.name
      }
    }
  }

  tags = merge(var.tags, {
    Name = var.cluster_name
  })
}

resource "aws_cloudwatch_log_group" "ecs_exec" {
  name              = "/ecs/${var.cluster_name}/exec"
  retention_in_days = var.log_retention_days
  tags              = var.tags
}

# ECS Capacity Provider (Fargate)
resource "aws_ecs_cluster_capacity_providers" "main" {
  cluster_name = aws_ecs_cluster.main.name
  capacity_providers = ["FARGATE", "FARGATE_SPOT"]
  default_capacity_provider_strategy {
    capacity_provider = "FARGATE"
    weight            = 1
    base              = 1
  }
}

# IAM Roles
resource "aws_iam_role" "execution" {
  name = "${var.cluster_name}-execution"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "ecs-tasks.amazonaws.com"
      }
    }]
  })

  tags = var.tags
}

resource "aws_iam_role_policy_attachment" "execution" {
  role       = aws_iam_role.execution.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

resource "aws_iam_role" "task" {
  name = "${var.cluster_name}-task"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "ecs-tasks.amazonaws.com"
      }
    }]
  })

  tags = var.tags
}

# Attach custom policies to task role
resource "aws_iam_role_policy_attachment" "task_media" {
  count      = var.media_policy_arn != "" ? 1 : 0
  role       = aws_iam_role.task.name
  policy_arn = var.media_policy_arn
}

# CloudWatch Log Groups
resource "aws_cloudwatch_log_group" "backend" {
  name              = "/ecs/${var.cluster_name}-backend"
  retention_in_days = var.log_retention_days
  tags              = var.tags
}

resource "aws_cloudwatch_log_group" "frontend" {
  name              = "/ecs/${var.cluster_name}-frontend"
  retention_in_days = var.log_retention_days
  tags              = var.tags
}

resource "aws_cloudwatch_log_group" "worker" {
  name              = "/ecs/${var.cluster_name}-worker"
  retention_in_days = var.log_retention_days
  tags              = var.tags
}

resource "aws_cloudwatch_log_group" "nginx" {
  name              = "/ecs/${var.cluster_name}-nginx"
  retention_in_days = var.log_retention_days
  tags              = var.tags
}

# ALB
resource "aws_lb" "main" {
  name               = "${var.cluster_name}-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [var.alb_security_group_id]
  subnets            = var.public_subnet_ids

  enable_deletion_protection = var.environment == "prod"
  enable_http2               = true
  enable_waf_fail_open       = false

  access_logs {
    bucket  = var.access_logs_bucket
    prefix  = "${var.cluster_name}/alb"
    enabled = var.access_logs_bucket != ""
  }

  tags = var.tags
}

# Target Groups
resource "aws_lb_target_group" "backend" {
  name        = "${var.cluster_name}-backend"
  port        = var.backend_task_definition.container_port
  protocol    = "HTTP"
  vpc_id      = var.vpc_id
  target_type = "ip"

  health_check {
    path                = var.backend_task_definition.health_check_path
    protocol            = "HTTP"
    matcher             = "200"
    interval            = 30
    timeout             = 10
    healthy_threshold   = 2
    unhealthy_threshold = 3
  }

  tags = var.tags
}

resource "aws_lb_target_group" "frontend" {
  name        = "${var.cluster_name}-frontend"
  port        = var.frontend_task_definition.container_port
  protocol    = "HTTP"
  vpc_id      = var.vpc_id
  target_type = "ip"

  health_check {
    path                = var.frontend_task_definition.health_check_path
    protocol            = "HTTP"
    matcher             = "200"
    interval            = 30
    timeout             = 10
    healthy_threshold   = 2
    unhealthy_threshold = 3
  }

  tags = var.tags
}

# ALB Listeners
resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.main.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type = "redirect"
    redirect {
      port        = "443"
      protocol    = "HTTPS"
      status_code = "HTTP_301"
    }
  }
}

resource "aws_lb_listener" "https" {
  load_balancer_arn = aws_lb.main.arn
  port              = 443
  protocol          = "HTTPS"
  ssl_policy        = "ELBSecurityPolicy-TLS13-1-2-2021-06"
  certificate_arn   = var.acm_certificate_arn

  default_action {
    type = "forward"
    target_group_arn = aws_lb_target_group.frontend.arn
  }
}

# Backend listener rule
resource "aws_lb_listener_rule" "backend" {
  listener_arn = aws_lb_listener.https.arn
  priority     = 100

  action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.backend.arn
  }

  condition {
    path_pattern {
      values = ["/api/*", "/ws/*", "/health"]
    }
  }
}

# Task Definitions

# Backend Task Definition
resource "aws_ecs_task_definition" "backend" {
  family                   = var.backend_task_definition.family
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = var.backend_service.cpu
  memory                   = var.backend_service.memory
  execution_role_arn       = aws_iam_role.execution.arn
  task_role_arn            = aws_iam_role.task.arn

  container_definitions = jsonencode([
    {
      name      = "backend"
      image     = var.backend_image
      essential = true
      portMappings = [{
        containerPort = var.backend_task_definition.container_port
        protocol      = "tcp"
      }]
      environment = [
        for k, v in var.backend_task_definition.environment_variables : {
          name  = k
          value = v
        }
      ]
      secrets = [
        for s in var.backend_task_definition.secrets : {
          name      = s
          valueFrom = "${var.secrets_prefix}/${s}"
        }
      ]
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-group"         = aws_cloudwatch_log_group.backend.name
          "awslogs-region"        = var.aws_region
          "awslogs-stream-prefix" = "backend"
        }
      }
      healthCheck = {
        command  = ["CMD-SHELL", "curl -f http://localhost:${var.backend_task_definition.container_port}${var.backend_task_definition.health_check_path} || exit 1"]
        interval = 30
        timeout  = 10
        retries  = 3
      }
    }
  ])

  tags = var.tags
}

# Frontend Task Definition
resource "aws_ecs_task_definition" "frontend" {
  family                   = var.frontend_task_definition.family
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = var.frontend_service.cpu
  memory                   = var.frontend_service.memory
  execution_role_arn       = aws_iam_role.execution.arn
  task_role_arn            = aws_iam_role.task.arn

  container_definitions = jsonencode([
    {
      name      = "frontend"
      image     = var.frontend_image
      essential = true
      portMappings = [{
        containerPort = var.frontend_task_definition.container_port
        protocol      = "tcp"
      }]
      environment = [
        for k, v in var.frontend_task_definition.environment_variables : {
          name  = k
          value = v
        }
      ]
      secrets = [
        for s in var.frontend_task_definition.secrets : {
          name      = s
          valueFrom = "${var.secrets_prefix}/${s}"
        }
      ]
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-group"         = aws_cloudwatch_log_group.frontend.name
          "awslogs-region"        = var.aws_region
          "awslogs-stream-prefix" = "frontend"
        }
      }
      healthCheck = {
        command  = ["CMD-SHELL", "curl -f http://localhost:${var.frontend_task_definition.container_port}${var.frontend_task_definition.health_check_path} || exit 1"]
        interval = 30
        timeout  = 10
        retries  = 3
      }
    }
  ])

  tags = var.tags
}

# Worker Task Definition
resource "aws_ecs_task_definition" "worker" {
  family                   = var.worker_task_definition.family
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = var.worker_service.cpu
  memory                   = var.worker_service.memory
  execution_role_arn       = aws_iam_role.execution.arn
  task_role_arn            = aws_iam_role.task.arn

  container_definitions = jsonencode([
    {
      name      = "worker"
      image     = var.worker_image
      essential = true
      environment = [
        for k, v in var.worker_task_definition.environment_variables : {
          name  = k
          value = v
        }
      ]
      secrets = [
        for s in var.worker_task_definition.secrets : {
          name      = s
          valueFrom = "${var.secrets_prefix}/${s}"
        }
      ]
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-group"         = aws_cloudwatch_log_group.worker.name
          "awslogs-region"        = var.aws_region
          "awslogs-stream-prefix" = "worker"
        }
      }
    }
  ])

  tags = var.tags
}

# ECS Services

# Backend Service
resource "aws_ecs_service" "backend" {
  name            = "${var.cluster_name}-backend"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.backend.arn
  desired_count   = var.backend_service.desired_count
  launch_type     = "FARGATE"
  platform_version = "LATEST"

  network_configuration {
    subnets         = var.private_subnet_ids
    security_groups = var.security_group_ids
    assign_public_ip = false
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.backend.arn
    container_name   = "backend"
    container_port   = var.backend_task_definition.container_port
  }

  deployment_controller {
    type = "ECS"
  }

  deployment_circuit_breaker {
    enable   = true
    rollback = true
  }

  tags = var.tags
}

# Frontend Service
resource "aws_ecs_service" "frontend" {
  name            = "${var.cluster_name}-frontend"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.frontend.arn
  desired_count   = var.frontend_service.desired_count
  launch_type     = "FARGATE"
  platform_version = "LATEST"

  network_configuration {
    subnets         = var.private_subnet_ids
    security_groups = var.security_group_ids
    assign_public_ip = false
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.frontend.arn
    container_name   = "frontend"
    container_port   = var.frontend_task_definition.container_port
  }

  deployment_controller {
    type = "ECS"
  }

  deployment_circuit_breaker {
    enable   = true
    rollback = true
  }

  tags = var.tags
}

# Worker Service
resource "aws_ecs_service" "worker" {
  name            = "${var.cluster_name}-worker"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.worker.arn
  desired_count   = var.worker_service.desired_count
  launch_type     = "FARGATE"
  platform_version = "LATEST"

  network_configuration {
    subnets         = var.private_subnet_ids
    security_groups = var.security_group_ids
    assign_public_ip = false
  }

  deployment_controller {
    type = "ECS"
  }

  deployment_circuit_breaker {
    enable   = true
    rollback = true
  }

  tags = var.tags
}

# Auto Scaling

# Backend Auto Scaling
resource "aws_appautoscaling_target" "backend" {
  max_capacity       = var.backend_service.max_capacity
  min_capacity       = var.backend_service.min_capacity
  resource_id        = "service/${aws_ecs_cluster.main.name}/${aws_ecs_service.backend.name}"
  scalable_dimension = "ecs:service:DesiredCount"
  service_namespace  = "ecs"
}

resource "aws_appautoscaling_policy" "backend_cpu" {
  name               = "${var.cluster_name}-backend-cpu"
  policy_type        = "TargetTrackingScaling"
  resource_id        = aws_appautoscaling_target.backend.resource_id
  scalable_dimension = aws_appautoscaling_target.backend.scalable_dimension
  service_namespace  = aws_appautoscaling_target.backend.service_namespace

  target_tracking_scaling_policy_configuration {
    target_value       = 70
    predefined_metric_specification {
      predefined_metric_type = "ECSServiceAverageCPUUtilization"
    }
    scale_in_cooldown  = 300
    scale_out_cooldown = 60
  }
}

resource "aws_appautoscaling_policy" "backend_memory" {
  name               = "${var.cluster_name}-backend-memory"
  policy_type        = "TargetTrackingScaling"
  resource_id        = aws_appautoscaling_target.backend.resource_id
  scalable_dimension = aws_appautoscaling_target.backend.scalable_dimension
  service_namespace  = aws_appautoscaling_target.backend.service_namespace

  target_tracking_scaling_policy_configuration {
    target_value       = 80
    predefined_metric_specification {
      predefined_metric_type = "ECSServiceAverageMemoryUtilization"
    }
    scale_in_cooldown  = 300
    scale_out_cooldown = 60
  }
}

# Frontend Auto Scaling
resource "aws_appautoscaling_target" "frontend" {
  max_capacity       = var.frontend_service.max_capacity
  min_capacity       = var.frontend_service.min_capacity
  resource_id        = "service/${aws_ecs_cluster.main.name}/${aws_ecs_service.frontend.name}"
  scalable_dimension = "ecs:service:DesiredCount"
  service_namespace  = "ecs"
}

resource "aws_appautoscaling_policy" "frontend_cpu" {
  name               = "${var.cluster_name}-frontend-cpu"
  policy_type        = "TargetTrackingScaling"
  resource_id        = aws_appautoscaling_target.frontend.resource_id
  scalable_dimension = aws_appautoscaling_target.frontend.scalable_dimension
  service_namespace  = aws_appautoscaling_target.frontend.service_namespace

  target_tracking_scaling_policy_configuration {
    target_value       = 70
    predefined_metric_specification {
      predefined_metric_type = "ECSServiceAverageCPUUtilization"
    }
    scale_in_cooldown  = 300
    scale_out_cooldown = 60
  }
}

# Worker Auto Scaling
resource "aws_appautoscaling_target" "worker" {
  max_capacity       = var.worker_service.max_capacity
  min_capacity       = var.worker_service.min_capacity
  resource_id        = "service/${aws_ecs_cluster.main.name}/${aws_ecs_service.worker.name}"
  scalable_dimension = "ecs:service:DesiredCount"
  service_namespace  = "ecs"
}

resource "aws_appautoscaling_policy" "worker_cpu" {
  name               = "${var.cluster_name}-worker-cpu"
  policy_type        = "TargetTrackingScaling"
  resource_id        = aws_appautoscaling_target.worker.resource_id
  scalable_dimension = aws_appautoscaling_target.worker.scalable_dimension
  service_namespace  = aws_appautoscaling_target.worker.service_namespace

  target_tracking_scaling_policy_configuration {
    target_value       = 70
    predefined_metric_specification {
      predefined_metric_type = "ECSServiceAverageCPUUtilization"
    }
    scale_in_cooldown  = 300
    scale_out_cooldown = 60
  }
}

resource "aws_appautoscaling_policy" "worker_memory" {
  name               = "${var.cluster_name}-worker-memory"
  policy_type        = "TargetTrackingScaling"
  resource_id        = aws_appautoscaling_target.worker.resource_id
  scalable_dimension = aws_appautoscaling_target.worker.scalable_dimension
  service_namespace  = aws_appautoscaling_target.worker.service_namespace

  target_tracking_scaling_policy_configuration {
    target_value       = 80
    predefined_metric_specification {
      predefined_metric_type = "ECSServiceAverageMemoryUtilization"
    }
    scale_in_cooldown  = 300
    scale_out_cooldown = 60
  }
}

# Outputs
output "cluster_name" {
  value = aws_ecs_cluster.main.name
}

output "cluster_arn" {
  value = aws_ecs_cluster.main.arn
}

output "backend_service_name" {
  value = aws_ecs_service.backend.name
}

output "backend_service_arn" {
  value = aws_ecs_service.backend.arn
}

output "frontend_service_name" {
  value = aws_ecs_service.frontend.name
}

output "frontend_service_arn" {
  value = aws_ecs_service.frontend.arn
}

output "worker_service_name" {
  value = aws_ecs_service.worker.name
}

output "worker_service_arn" {
  value = aws_ecs_service.worker.arn
}

output "backend_task_definition_arn" {
  value = aws_ecs_task_definition.backend.arn
}

output "frontend_task_definition_arn" {
  value = aws_ecs_task_definition.frontend.arn
}

output "worker_task_definition_arn" {
  value = aws_ecs_task_definition.worker.arn
}

output "execution_role_arn" {
  value = aws_iam_role.execution.arn
}

output "task_role_arn" {
  value = aws_iam_role.task.arn
}

output "alb_arn" {
  value = aws_lb.main.arn
}

output "alb_dns_name" {
  value = aws_lb.main.dns_name
}

output "alb_zone_id" {
  value = aws_lb.main.zone_id
}

output "alb_security_group_id" {
  value = var.alb_security_group_id
}

output "backend_target_group_arn" {
  value = aws_lb_target_group.backend.arn
}

output "frontend_target_group_arn" {
  value = aws_lb_target_group.frontend.arn
}