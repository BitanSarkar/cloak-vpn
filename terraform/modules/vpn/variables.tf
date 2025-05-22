variable "region" {}
variable "ami" {}
variable "instance_type" {}
variable "instance_count" {
    type = number
    default = 0
}