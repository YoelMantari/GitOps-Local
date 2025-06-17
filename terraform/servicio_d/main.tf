variable "python_exec" {
  description = "Ruta al ejecutable de Python."
  type        = string
  default     = "/usr/bin/python3.12"
}

locals {

  ruta_raiz_proyecto = "/home/YoeMant/Documents/CodeSublime/GitOps-Local"

}


module "servicio_b" {
  source = "../servicio_b"
}


resource "null_resource" "servicio_d" {

  depends_on = [module.servicio_b]

  provisioner "local-exec" {
    command = "nohup ${var.python_exec} ${local.ruta_raiz_proyecto}/scripts/cola_dummy.py > /tmp/cola_dummy.log 2>&1 &"
  }
}
