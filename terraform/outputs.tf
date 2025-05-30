# ✅ Region to Public IPs Output
output "vpn_public_ips" {
  value = tomap({
    "us-east-1"      = try(flatten([for m in try(module.vpn_us_east_1.public_ips, []) : m]), [])
    "us-east-2"      = try(flatten([for m in try(module.vpn_us_east_2.public_ips, []) : m]), [])
    "us-west-1"      = try(flatten([for m in try(module.vpn_us_west_1.public_ips, []) : m]), [])
    "us-west-2"      = try(flatten([for m in try(module.vpn_us_west_2.public_ips, []) : m]), [])
    "ca-central-1"   = try(flatten([for m in try(module.vpn_ca_central_1.public_ips, []) : m]), [])
    "sa-east-1"      = try(flatten([for m in try(module.vpn_sa_east_1.public_ips, []) : m]), [])
    "eu-west-1"      = try(flatten([for m in try(module.vpn_eu_west_1.public_ips, []) : m]), [])
    "eu-west-2"      = try(flatten([for m in try(module.vpn_eu_west_2.public_ips, []) : m]), [])
    "eu-west-3"      = try(flatten([for m in try(module.vpn_eu_west_3.public_ips, []) : m]), [])
    "eu-north-1"     = try(flatten([for m in try(module.vpn_eu_north_1.public_ips, []) : m]), [])
    "eu-central-1"   = try(flatten([for m in try(module.vpn_eu_central_1.public_ips, []) : m]), [])
    "eu-central-2"   = try(flatten([for m in try(module.vpn_eu_central_2.public_ips, []) : m]), [])
    "eu-south-1"     = try(flatten([for m in try(module.vpn_eu_south_1.public_ips, []) : m]), [])
    "eu-south-2"     = try(flatten([for m in try(module.vpn_eu_south_2.public_ips, []) : m]), [])
    "me-central-1"   = try(flatten([for m in try(module.vpn_me_central_1.public_ips, []) : m]), [])
    "me-south-1"     = try(flatten([for m in try(module.vpn_me_south_1.public_ips, []) : m]), [])
    "il-central-1"   = try(flatten([for m in try(module.vpn_il_central_1.public_ips, []) : m]), [])
    "af-south-1"     = try(flatten([for m in try(module.vpn_af_south_1.public_ips, []) : m]), [])
    "ap-south-1"     = try(flatten([for m in try(module.vpn_ap_south_1.public_ips, []) : m]), [])
    "ap-south-2"     = try(flatten([for m in try(module.vpn_ap_south_2.public_ips, []) : m]), [])
    "ap-southeast-1" = try(flatten([for m in try(module.vpn_ap_southeast_1.public_ips, []) : m]), [])
    "ap-southeast-2" = try(flatten([for m in try(module.vpn_ap_southeast_2.public_ips, []) : m]), [])
    "ap-southeast-3" = try(flatten([for m in try(module.vpn_ap_southeast_3.public_ips, []) : m]), [])
    "ap-southeast-4" = try(flatten([for m in try(module.vpn_ap_southeast_4.public_ips, []) : m]), [])
    "ap-southeast-5" = try(flatten([for m in try(module.vpn_ap_southeast_5.public_ips, []) : m]), [])
    "ap-southeast-7" = try(flatten([for m in try(module.vpn_ap_southeast_7.public_ips, []) : m]), [])
    "ap-east-1"      = try(flatten([for m in try(module.vpn_ap_east_1.public_ips, []) : m]), [])
    "ap-northeast-1" = try(flatten([for m in try(module.vpn_ap_northeast_1.public_ips, []) : m]), [])
    "ap-northeast-2" = try(flatten([for m in try(module.vpn_ap_northeast_2.public_ips, []) : m]), [])
    "ap-northeast-3" = try(flatten([for m in try(module.vpn_ap_northeast_3.public_ips, []) : m]), [])
  })
}