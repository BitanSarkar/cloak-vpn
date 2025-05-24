variable "regions" {
  type = map(object({
    count          = number
  }))

  default = {}
}
variable "my_public_ip" {
  type = string
  default = "0.0.0.0/0"
}