locals {

  ruta_raiz_proyecto = "/home/YoeMant/Documents/CodeSublime/GitOps-Local"

  ruta_servicios_simulados = "${local.ruta_raiz_proyecto}/servicios_simulados"

}

variable "service_name" {
  description = "Nombre del servicio dummy a instalar"
  type        = string
  default     = "servicio_dummy_A.service"
}


resource "null_resource" "servicio_a" {
  provisioner "local-exec" {
    command = "${local.ruta_raiz_proyecto}/scripts/instala_servicio.sh ${var.service_name} ${local.ruta_servicios_simulados}"
  }
}
