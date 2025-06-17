variable "python_exec" {
  description = "Ruta al ejecutable de Python."
  type        = string
  default     = "/home/dirac/Documents/DS/GitOps-Local/.venv/bin/python3.12"
}

locals {

  ruta_raiz_proyecto = "/home/dirac/Documents/DS/GitOps-Local"

}


module "servicio_b" {
  source = "../servicio_b"
}

variable "ip_cola_dummy" {
  description = "El numero IP del socket donde se iniciara el proceso de escucha"
  type        = string
  default     = "127.0.0.1"
}

variable "puerto_cola_dummy" {
  description = "El numero de puerto del socket donde se iniciara el proceso de escucha"
  type        = number
  default     = 1234
}


resource "null_resource" "servicio_d" {

  depends_on = [module.servicio_b]

  provisioner "local-exec" {
    command = "nohup ${var.python_exec} ${local.ruta_raiz_proyecto}/scripts/cola_dummy.py ${var.ip_cola_dummy} ${var.puerto_cola_dummy} > /tmp/cola_dummy.log 2>&1 &"
  }
}