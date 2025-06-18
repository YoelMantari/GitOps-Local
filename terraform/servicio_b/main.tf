module "servicio_c" {
  source = "../servicio_c"
  #ruta_raiz_proyecto = var.ruta_raiz_proyecto
  #ruta_servicios_simulados = var.ruta_servicios_simulados
}

locals {

  ruta_raiz_proyecto       = abspath("${path.module}/../../")
  ruta_servicios_simulados = abspath("${path.module}/../../servicios_simulados")

}

# variable ruta_raiz_proyecto {
#   description = "Ruta del directorio principal del proyecto"
#   type = string
# }

# variable ruta_servicios_simulados {
#   description = "Ruta del directorio donde se guardara todo lo relacionado a los servicios a, b, c y d"
#   type = string
# }

variable "service_name" {
  description = "Nombre del servicio dummy a instalar"
  type        = string
  default     = "servicio_dummy_B.service"
}


resource "null_resource" "servicio_b" {

  depends_on = [module.servicio_c]

  provisioner "local-exec" {
    command = "${local.ruta_raiz_proyecto}/scripts/instala_servicio.sh ${var.service_name} ${local.ruta_servicios_simulados}"
  }
}
