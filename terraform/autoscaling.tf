provider "aws" {
region = "us-east-1"
}

resource "aws_launch_template" "cost_optimized_template" {
  name_prefix   = "cost-optimized"
  image_id      = "ami-0e449927258d45bc4"
  instance_type = "t2.micro"
}

resource "aws_autoscaling_group" "cost_optimized_asg" {
  name                = "cost-optimized-asg"
  desired_capacity    = 1
  max_size            = 3
  min_size            = 1
  vpc_zone_identifier = ["subnet-013d81361b0cc204a"]  
  launch_template {
    id      = aws_launch_template.cost_optimized_template.id
    version = "$Latest"
  }
}

resource "aws_autoscaling_policy" "scale_up" {
  name                   = "scale-up"
  scaling_adjustment     = 1
  adjustment_type        = "ChangeInCapacity"
  cooldown               = 60
  autoscaling_group_name = aws_autoscaling_group.cost_optimized_asg.name
}

resource "aws_autoscaling_policy" "scale_down" {
  name                   = "scale-down"
  scaling_adjustment     = -1
  adjustment_type        = "ChangeInCapacity"
  cooldown               = 60
  autoscaling_group_name = aws_autoscaling_group.cost_optimized_asg.name
}
