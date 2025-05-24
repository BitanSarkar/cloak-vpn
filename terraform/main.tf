terraform {
  backend "local" {
    path = "./tfstate/terraform.tfstate"
  }

  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# ✅ Modules for each AWS region, dynamically controlled by var.regions
module "vpn_us_east_1" {
  instance_count = contains(keys(var.regions), "us-east-1") ? var.regions["us-east-1"].count : 0
  source         = "./modules/vpn"
  providers      = { aws = aws.us-east-1 }
  region         = "us-east-1"
  ami            = data.aws_ami.amazon_linux_us_east_1.id
  my_public_ip   = var.my_public_ip
}

module "vpn_us_east_2" {
  instance_count = contains(keys(var.regions), "us-east-2") ? var.regions["us-east-2"].count : 0
  source         = "./modules/vpn"
  providers      = { aws = aws.us-east-2 }
  region         = "us-east-2"
  ami            = data.aws_ami.amazon_linux_us_east_2.id
  my_public_ip   = var.my_public_ip
}

module "vpn_us_west_1" {
  instance_count = contains(keys(var.regions), "us-west-1") ? var.regions["us-west-1"].count : 0
  source         = "./modules/vpn"
  providers      = { aws = aws.us-west-1 }
  region         = "us-west-1"
  ami            = data.aws_ami.amazon_linux_us_west_1.id
  my_public_ip   = var.my_public_ip
}

module "vpn_us_west_2" {
  instance_count = contains(keys(var.regions), "us-west-2") ? var.regions["us-west-2"].count : 0
  source         = "./modules/vpn"
  providers      = { aws = aws.us-west-2 }
  region         = "us-west-2"
  ami            = data.aws_ami.amazon_linux_us_west_2.id
  my_public_ip   = var.my_public_ip
}

module "vpn_ca_central_1" {
  instance_count = contains(keys(var.regions), "ca-central-1") ? var.regions["ca-central-1"].count : 0
  source         = "./modules/vpn"
  providers      = { aws = aws.ca-central-1 }
  region         = "ca-central-1"
  ami            = data.aws_ami.amazon_linux_ca_central_1.id
  my_public_ip   = var.my_public_ip
}

module "vpn_sa_east_1" {
  instance_count = contains(keys(var.regions), "sa-east-1") ? var.regions["sa-east-1"].count : 0
  source         = "./modules/vpn"
  providers      = { aws = aws.sa-east-1 }
  region         = "sa-east-1"
  ami            = data.aws_ami.amazon_linux_sa_east_1.id
  my_public_ip   = var.my_public_ip
}

module "vpn_eu_west_1" {
  instance_count = contains(keys(var.regions), "eu-west-1") ? var.regions["eu-west-1"].count : 0
  source         = "./modules/vpn"
  providers      = { aws = aws.eu-west-1 }
  region         = "eu-west-1"
  ami            = data.aws_ami.amazon_linux_eu_west_1.id
  my_public_ip   = var.my_public_ip
}

module "vpn_eu_west_2" {
  instance_count = contains(keys(var.regions), "eu-west-2") ? var.regions["eu-west-2"].count : 0
  source         = "./modules/vpn"
  providers      = { aws = aws.eu-west-2 }
  region         = "eu-west-2"
  ami            = data.aws_ami.amazon_linux_eu_west_2.id
  my_public_ip   = var.my_public_ip
}

module "vpn_eu_west_3" {
  instance_count = contains(keys(var.regions), "eu-west-3") ? var.regions["eu-west-3"].count : 0
  source         = "./modules/vpn"
  providers      = { aws = aws.eu-west-3 }
  region         = "eu-west-3"
  ami            = data.aws_ami.amazon_linux_eu_west_3.id
  my_public_ip   = var.my_public_ip
}

module "vpn_eu_north_1" {
  instance_count = contains(keys(var.regions), "eu-north-1") ? var.regions["eu-north-1"].count : 0
  source         = "./modules/vpn"
  providers      = { aws = aws.eu-north-1 }
  region         = "eu-north-1"
  ami            = data.aws_ami.amazon_linux_eu_north_1.id
  my_public_ip   = var.my_public_ip
}

module "vpn_eu_central_1" {
  instance_count = contains(keys(var.regions), "eu-central-1") ? var.regions["eu-central-1"].count : 0
  source         = "./modules/vpn"
  providers      = { aws = aws.eu-central-1 }
  region         = "eu-central-1"
  ami            = data.aws_ami.amazon_linux_eu_central_1.id
  my_public_ip   = var.my_public_ip
}

module "vpn_eu_central_2" {
  instance_count = contains(keys(var.regions), "eu-central-2") ? var.regions["eu-central-2"].count : 0
  source         = "./modules/vpn"
  providers      = { aws = aws.eu-central-2 }
  region         = "eu-central-2"
  ami            = data.aws_ami.amazon_linux_eu_central_2.id
  my_public_ip   = var.my_public_ip
}

module "vpn_eu_south_1" {
  instance_count = contains(keys(var.regions), "eu-south-1") ? var.regions["eu-south-1"].count : 0
  source         = "./modules/vpn"
  providers      = { aws = aws.eu-south-1 }
  region         = "eu-south-1"
  ami            = data.aws_ami.amazon_linux_eu_south_1.id
  my_public_ip   = var.my_public_ip
}

module "vpn_eu_south_2" {
  instance_count = contains(keys(var.regions), "eu-south-2") ? var.regions["eu-south-2"].count : 0
  source         = "./modules/vpn"
  providers      = { aws = aws.eu-south-2 }
  region         = "eu-south-2"
  ami            = data.aws_ami.amazon_linux_eu_south_2.id
  my_public_ip   = var.my_public_ip
}

module "vpn_me_central_1" {
  instance_count = contains(keys(var.regions), "me-central-1") ? var.regions["me-central-1"].count : 0
  source         = "./modules/vpn"
  providers      = { aws = aws.me-central-1 }
  region         = "me-central-1"
  ami            = data.aws_ami.amazon_linux_me_central_1.id
  my_public_ip   = var.my_public_ip
}

module "vpn_me_south_1" {
  instance_count = contains(keys(var.regions), "me-south-1") ? var.regions["me-south-1"].count : 0
  source         = "./modules/vpn"
  providers      = { aws = aws.me-south-1 }
  region         = "me-south-1"
  ami            = data.aws_ami.amazon_linux_me_south_1.id
  my_public_ip   = var.my_public_ip
}

module "vpn_il_central_1" {
  instance_count = contains(keys(var.regions), "il-central-1") ? var.regions["il-central-1"].count : 0
  source         = "./modules/vpn"
  providers      = { aws = aws.il-central-1 }
  region         = "il-central-1"
  ami            = data.aws_ami.amazon_linux_il_central_1.id
  my_public_ip   = var.my_public_ip
}

module "vpn_af_south_1" {
  instance_count = contains(keys(var.regions), "af-south-1") ? var.regions["af-south-1"].count : 0
  source         = "./modules/vpn"
  providers      = { aws = aws.af-south-1 }
  region         = "af-south-1"
  ami            = data.aws_ami.amazon_linux_af_south_1.id
  my_public_ip   = var.my_public_ip
}

module "vpn_ap_south_1" {
  instance_count = contains(keys(var.regions), "ap-south-1") ? var.regions["ap-south-1"].count : 0
  source         = "./modules/vpn"
  providers      = { aws = aws.ap-south-1 }
  region         = "ap-south-1"
  ami            = data.aws_ami.amazon_linux_ap_south_1.id
  my_public_ip   = var.my_public_ip
}

module "vpn_ap_south_2" {
  instance_count = contains(keys(var.regions), "ap-south-2") ? var.regions["ap-south-2"].count : 0
  source         = "./modules/vpn"
  providers      = { aws = aws.ap-south-2 }
  region         = "ap-south-2"
  ami            = data.aws_ami.amazon_linux_ap_south_2.id
  my_public_ip   = var.my_public_ip
}

module "vpn_ap_southeast_1" {
  instance_count = contains(keys(var.regions), "ap-southeast-1") ? var.regions["ap-southeast-1"].count : 0
  source         = "./modules/vpn"
  providers      = { aws = aws.ap-southeast-1 }
  region         = "ap-southeast-1"
  ami            = data.aws_ami.amazon_linux_ap_southeast_1.id
  my_public_ip   = var.my_public_ip
}

module "vpn_ap_southeast_2" {
  instance_count = contains(keys(var.regions), "ap-southeast-2") ? var.regions["ap-southeast-2"].count : 0
  source         = "./modules/vpn"
  providers      = { aws = aws.ap-southeast-2 }
  region         = "ap-southeast-2"
  ami            = data.aws_ami.amazon_linux_ap_southeast_2.id
  my_public_ip   = var.my_public_ip
}

module "vpn_ap_southeast_3" {
  instance_count = contains(keys(var.regions), "ap-southeast-3") ? var.regions["ap-southeast-3"].count : 0
  source         = "./modules/vpn"
  providers      = { aws = aws.ap-southeast-3 }
  region         = "ap-southeast-3"
  ami            = data.aws_ami.amazon_linux_ap_southeast_3.id
  my_public_ip   = var.my_public_ip
}

module "vpn_ap_southeast_4" {
  instance_count = contains(keys(var.regions), "ap-southeast-4") ? var.regions["ap-southeast-4"].count : 0
  source         = "./modules/vpn"
  providers      = { aws = aws.ap-southeast-4 }
  region         = "ap-southeast-4"
  ami            = data.aws_ami.amazon_linux_ap_southeast_4.id
  my_public_ip   = var.my_public_ip
}

module "vpn_ap_southeast_5" {
  instance_count = contains(keys(var.regions), "ap-southeast-5") ? var.regions["ap-southeast-5"].count : 0
  source         = "./modules/vpn"
  providers      = { aws = aws.ap-southeast-5 }
  region         = "ap-southeast-5"
  ami            = data.aws_ami.amazon_linux_ap_southeast_5.id
  my_public_ip   = var.my_public_ip
}

module "vpn_ap_southeast_7" {
  instance_count = contains(keys(var.regions), "ap-southeast-7") ? var.regions["ap-southeast-7"].count : 0
  source         = "./modules/vpn"
  providers      = { aws = aws.ap-southeast-7 }
  region         = "ap-southeast-7"
  ami            = data.aws_ami.amazon_linux_ap_southeast_7.id
  my_public_ip   = var.my_public_ip
}

module "vpn_ap_east_1" {
  instance_count = contains(keys(var.regions), "ap-east-1") ? var.regions["ap-east-1"].count : 0
  source         = "./modules/vpn"
  providers      = { aws = aws.ap-east-1 }
  region         = "ap-east-1"
  ami            = data.aws_ami.amazon_linux_ap_east_1.id
  my_public_ip   = var.my_public_ip
}

module "vpn_ap_northeast_1" {
  instance_count = contains(keys(var.regions), "ap-northeast-1") ? var.regions["ap-northeast-1"].count : 0
  source         = "./modules/vpn"
  providers      = { aws = aws.ap-northeast-1 }
  region         = "ap-northeast-1"
  ami            = data.aws_ami.amazon_linux_ap_northeast_1.id
  my_public_ip   = var.my_public_ip
}

module "vpn_ap_northeast_2" {
  instance_count = contains(keys(var.regions), "ap-northeast-2") ? var.regions["ap-northeast-2"].count : 0
  source         = "./modules/vpn"
  providers      = { aws = aws.ap-northeast-2 }
  region         = "ap-northeast-2"
  ami            = data.aws_ami.amazon_linux_ap_northeast_2.id
  my_public_ip   = var.my_public_ip
}

module "vpn_ap_northeast_3" {
  instance_count = contains(keys(var.regions), "ap-northeast-3") ? var.regions["ap-northeast-3"].count : 0
  source         = "./modules/vpn"
  providers      = { aws = aws.ap-northeast-3 }
  region         = "ap-northeast-3"
  ami            = data.aws_ami.amazon_linux_ap_northeast_3.id
  my_public_ip   = var.my_public_ip
}