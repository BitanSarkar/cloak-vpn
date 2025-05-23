variable "regions" {
  type = map(object({
    count          = number
  }))

  default = {}
}