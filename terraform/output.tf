output "ec2_public_ip" {
  description = "Public IP of AIOps server"
  value       = aws_instance.aiops_server.public_ip
}

output "ec2_public_dns" {
  description = "Public DNS of AIOps server"
  value       = aws_instance.aiops_server.public_dns
}