# ✅ Updated `data.tf` with all ENABLED and ENABLED_BY_DEFAULT AWS regions
# ✅ Amazon Linux 2 AMI lookups for each enabled region

# US Regions
data "aws_ami" "amazon_linux_us_east_1" {
  provider    = aws.us-east-1
  most_recent = true
  owners      = ["amazon"]
  filter {
    name = "name"
    values = ["amzn2-ami-hvm-*-arm64-gp2"]
  }
  filter {
    name   = "architecture"
    values = ["arm64"]
  }
}

data "aws_ami" "amazon_linux_us_east_2" {
  provider    = aws.us-east-2
  most_recent = true
  owners      = ["amazon"]
  filter {
    name = "name"
    values = ["amzn2-ami-hvm-*-arm64-gp2"]
  }
  filter {
    name   = "architecture"
    values = ["arm64"]
  }
}

data "aws_ami" "amazon_linux_us_west_1" {
  provider    = aws.us-west-1
  most_recent = true
  owners      = ["amazon"]
  filter {
    name = "name"
    values = ["amzn2-ami-hvm-*-arm64-gp2"]
  }
  filter {
    name   = "architecture"
    values = ["arm64"]
  }
}

data "aws_ami" "amazon_linux_us_west_2" {
  provider    = aws.us-west-2
  most_recent = true
  owners      = ["amazon"]
  filter {
    name = "name"
    values = ["amzn2-ami-hvm-*-arm64-gp2"]
  }
  filter {
    name   = "architecture"
    values = ["arm64"]
  }
}

# Canada, South America, and Mexico
data "aws_ami" "amazon_linux_ca_central_1" {
  provider    = aws.ca-central-1
  most_recent = true
  owners      = ["amazon"]
  filter {
    name = "name"
    values = ["amzn2-ami-hvm-*-arm64-gp2"]
  }
  filter {
    name   = "architecture"
    values = ["arm64"]
  }
}

data "aws_ami" "amazon_linux_sa_east_1" {
  provider    = aws.sa-east-1
  most_recent = true
  owners      = ["amazon"]
  filter {
    name = "name"
    values = ["amzn2-ami-hvm-*-arm64-gp2"]
  }
  filter {
    name   = "architecture"
    values = ["arm64"]
  }
}

# Europe
data "aws_ami" "amazon_linux_eu_west_1" {
  provider    = aws.eu-west-1
  most_recent = true
  owners      = ["amazon"]
  filter {
    name = "name"
    values = ["amzn2-ami-hvm-*-arm64-gp2"]
  }
  filter {
    name   = "architecture"
    values = ["arm64"]
  }
}

data "aws_ami" "amazon_linux_eu_west_2" {
  provider    = aws.eu-west-2
  most_recent = true
  owners      = ["amazon"]
  filter {
    name = "name"
    values = ["amzn2-ami-hvm-*-arm64-gp2"]
  }
  filter {
    name   = "architecture"
    values = ["arm64"]
  }
}

data "aws_ami" "amazon_linux_eu_west_3" {
  provider    = aws.eu-west-3
  most_recent = true
  owners      = ["amazon"]
  filter {
    name = "name"
    values = ["amzn2-ami-hvm-*-arm64-gp2"]
  }
  filter {
    name   = "architecture"
    values = ["arm64"]
  }
}

data "aws_ami" "amazon_linux_eu_central_1" {
  provider    = aws.eu-central-1
  most_recent = true
  owners      = ["amazon"]
  filter {
    name = "name"
    values = ["amzn2-ami-hvm-*-arm64-gp2"]
  }
  filter {
    name   = "architecture"
    values = ["arm64"]
  }
}

data "aws_ami" "amazon_linux_eu_north_1" {
  provider    = aws.eu-north-1
  most_recent = true
  owners      = ["amazon"]
  filter {
    name = "name"
    values = ["amzn2-ami-hvm-*-arm64-gp2"]
  }
  filter {
    name   = "architecture"
    values = ["arm64"]
  }
}

data "aws_ami" "amazon_linux_eu_south_1" {
  provider    = aws.eu-south-1
  most_recent = true
  owners      = ["amazon"]
  filter {
    name = "name"
    values = ["amzn2-ami-hvm-*-arm64-gp2"]
  }
  filter {
    name   = "architecture"
    values = ["arm64"]
  }
}

data "aws_ami" "amazon_linux_eu_south_2" {
  provider    = aws.eu-south-2
  most_recent = true
  owners      = ["amazon"]
  filter {
    name = "name"
    values = ["amzn2-ami-hvm-*-arm64-gp2"]
  }
  filter {
    name   = "architecture"
    values = ["arm64"]
  }
}

data "aws_ami" "amazon_linux_eu_central_2" {
  provider    = aws.eu-central-2
  most_recent = true
  owners      = ["amazon"]
  filter {
    name = "name"
    values = ["amzn2-ami-hvm-*-arm64-gp2"]
  }
  filter {
    name   = "architecture"
    values = ["arm64"]
  }
}

# Middle East & Israel
data "aws_ami" "amazon_linux_me_central_1" {
  provider    = aws.me-central-1
  most_recent = true
  owners      = ["amazon"]
  filter {
    name = "name"
    values = ["amzn2-ami-hvm-*-arm64-gp2"]
  }
  filter {
    name   = "architecture"
    values = ["arm64"]
  }
}

data "aws_ami" "amazon_linux_me_south_1" {
  provider    = aws.me-south-1
  most_recent = true
  owners      = ["amazon"]
  filter {
    name = "name"
    values = ["amzn2-ami-hvm-*-arm64-gp2"]
  }
  filter {
    name   = "architecture"
    values = ["arm64"]
  }
}

data "aws_ami" "amazon_linux_il_central_1" {
  provider    = aws.il-central-1
  most_recent = true
  owners      = ["amazon"]
  filter {
    name = "name"
    values = ["amzn2-ami-hvm-*-arm64-gp2"]
  }
  filter {
    name   = "architecture"
    values = ["arm64"]
  }
}

# Africa

data "aws_ami" "amazon_linux_af_south_1" {
  provider    = aws.af-south-1
  most_recent = true
  owners      = ["amazon"]
  filter {
    name = "name"
    values = ["amzn2-ami-hvm-*-arm64-gp2"]
  }
  filter {
    name   = "architecture"
    values = ["arm64"]
  }
}

# Asia Pacific
data "aws_ami" "amazon_linux_ap_south_1" {
  provider    = aws.ap-south-1
  most_recent = true
  owners      = ["amazon"]
  filter {
    name = "name"
    values = ["amzn2-ami-hvm-*-arm64-gp2"]
  }
  filter {
    name   = "architecture"
    values = ["arm64"]
  }
}

data "aws_ami" "amazon_linux_ap_south_2" {
  provider    = aws.ap-south-2
  most_recent = true
  owners      = ["amazon"]
  filter {
    name = "name"
    values = ["amzn2-ami-hvm-*-arm64-gp2"]
  }
  filter {
    name   = "architecture"
    values = ["arm64"]
  }
}

data "aws_ami" "amazon_linux_ap_southeast_1" {
  provider    = aws.ap-southeast-1
  most_recent = true
  owners      = ["amazon"]
  filter {
    name = "name"
    values = ["amzn2-ami-hvm-*-arm64-gp2"]
  }
  filter {
    name   = "architecture"
    values = ["arm64"]
  }
}

data "aws_ami" "amazon_linux_ap_southeast_2" {
  provider    = aws.ap-southeast-2
  most_recent = true
  owners      = ["amazon"]
  filter {
    name = "name"
    values = ["amzn2-ami-hvm-*-arm64-gp2"]
  }
  filter {
    name   = "architecture"
    values = ["arm64"]
  }
}

data "aws_ami" "amazon_linux_ap_southeast_3" {
  provider    = aws.ap-southeast-3
  most_recent = true
  owners      = ["amazon"]
  filter {
    name = "name"
    values = ["amzn2-ami-hvm-*-arm64-gp2"]
  }
  filter {
    name   = "architecture"
    values = ["arm64"]
  }
}

data "aws_ami" "amazon_linux_ap_southeast_4" {
  provider    = aws.ap-southeast-4
  most_recent = true
  owners      = ["amazon"]
  filter {
    name = "name"
    values = ["amzn2-ami-hvm-*-arm64-gp2"]
  }
  filter {
    name   = "architecture"
    values = ["arm64"]
  }
}

data "aws_ami" "amazon_linux_ap_southeast_5" {
  provider    = aws.ap-southeast-5
  most_recent = true
  owners      = ["amazon"]
  filter {
    name = "name"
    values = ["amzn2-ami-hvm-*-arm64-gp2"]
  }
  filter {
    name   = "architecture"
    values = ["arm64"]
  }
}

data "aws_ami" "amazon_linux_ap_southeast_7" {
  provider    = aws.ap-southeast-7
  most_recent = true
  owners      = ["amazon"]
  filter {
    name = "name"
    values = ["amzn2-ami-hvm-*-arm64-gp2"]
  }
  filter {
    name   = "architecture"
    values = ["arm64"]
  }
}

data "aws_ami" "amazon_linux_ap_east_1" {
  provider    = aws.ap-east-1
  most_recent = true
  owners      = ["amazon"]
  filter {
    name = "name"
    values = ["amzn2-ami-hvm-*-arm64-gp2"]
  }
  filter {
    name   = "architecture"
    values = ["arm64"]
  }
}

data "aws_ami" "amazon_linux_ap_northeast_1" {
  provider    = aws.ap-northeast-1
  most_recent = true
  owners      = ["amazon"]
  filter {
    name = "name"
    values = ["amzn2-ami-hvm-*-arm64-gp2"]
  }
  filter {
    name   = "architecture"
    values = ["arm64"]
  }
}

data "aws_ami" "amazon_linux_ap_northeast_2" {
  provider    = aws.ap-northeast-2
  most_recent = true
  owners      = ["amazon"]
  filter {
    name = "name"
    values = ["amzn2-ami-hvm-*-arm64-gp2"]
  }
  filter {
    name   = "architecture"
    values = ["arm64"]
  }
}

data "aws_ami" "amazon_linux_ap_northeast_3" {
  provider    = aws.ap-northeast-3
  most_recent = true
  owners      = ["amazon"]
  filter {
    name = "name"
    values = ["amzn2-ami-hvm-*-arm64-gp2"]
  }
  filter {
    name   = "architecture"
    values = ["arm64"]
  }
}
