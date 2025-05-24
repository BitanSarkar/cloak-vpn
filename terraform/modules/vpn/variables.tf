variable "region" {}
variable "ami" {}
variable "instance_count" {
    type = number
    default = 0
}
variable "bad_azs" {
  type = map(list(string))
  default = {
    "us-east-1" = ["us-east-1e"]
  }
}
variable "my_public_ip" {
  type = string
  default = "0.0.0.0/0"
}