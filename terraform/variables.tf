variable "regions" {
  type = map(object({
    count          = number
    instance_type  = string
  }))

  default = {}
}