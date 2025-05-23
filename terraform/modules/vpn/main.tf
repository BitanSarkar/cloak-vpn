# VPC
resource "aws_vpc" "vpn_vpc" {
  count = var.instance_count > 0 ? 1 : 0
  cidr_block           = "10.0.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name = "vpn-vpc-${var.region}"
  }
}

# Internet Gateway
resource "aws_internet_gateway" "vpn_igw" {
  count = var.instance_count > 0 ? 1 : 0
  vpc_id = aws_vpc.vpn_vpc[0].id
  tags = {
    Name = "vpn-igw-${var.region}"
  }
}


data "aws_availability_zones" "available" {
  state = "available"
}

locals {
  bad_list = lookup(var.bad_azs, var.region, [])

  filtered_azs = [
    for az in data.aws_availability_zones.available.names : az
    if !(contains(local.bad_list, az))
  ]

  available_az = local.filtered_azs[0]
}

resource "aws_subnet" "vpn_subnet" {
  count      = var.instance_count > 0 ? 1 : 0
  vpc_id     = aws_vpc.vpn_vpc[0].id
  cidr_block = "10.0.1.0/24"
  availability_zone = local.available_az
  map_public_ip_on_launch = true

  tags = {
    Name = "vpn-subnet-${var.region}"
  }
}

# Route Table
resource "aws_route_table" "vpn_route_table" {
  count = var.instance_count > 0 ? 1 : 0
  vpc_id = aws_vpc.vpn_vpc[0].id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.vpn_igw[0].id
  }

  tags = {
    Name = "vpn-rt-${var.region}"
  }
}

resource "aws_route_table_association" "vpn_rt_assoc" {
  count = var.instance_count > 0 ? 1 : 0
  subnet_id      = aws_subnet.vpn_subnet[0].id
  route_table_id = aws_route_table.vpn_route_table[0].id
}

# SSH Key
resource "aws_key_pair" "vpn_key" {
  count = var.instance_count > 0 ? 1 : 0
  key_name   = "vpn-key-${var.region}"
  public_key = file("~/.ssh/ghostvpn.pub")
}

# Security Group
resource "aws_security_group" "vpn_sg" {
  count = var.instance_count > 0 ? 1 : 0
  name   = "vpn-sg-${var.region}"
  vpc_id = aws_vpc.vpn_vpc[0].id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 1194
    to_port     = 1194
    protocol    = "udp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "vpn-sg-${var.region}"
  }
}

# EC2 VPN Instance
resource "aws_instance" "vpn" {
  ami                         = var.ami
  instance_type               = "t4g.micro"
  subnet_id                   = aws_subnet.vpn_subnet[0].id
  vpc_security_group_ids      = [aws_security_group.vpn_sg[0].id]
  key_name                    = aws_key_pair.vpn_key[0].key_name
  associate_public_ip_address = true
  count                       = var.instance_count
  user_data                   = file("${path.module}/user-data.sh")

  tags = {
    Name = "vpn-${var.region}"
  }
}

output "public_ips" {
  value = [for inst in aws_instance.vpn : inst.public_ip]
}