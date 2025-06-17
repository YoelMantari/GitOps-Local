# variable ruta_raiz_proyecto {
#   description = "Ruta del directorio principal del proyecto"
#   type = string
# }

# variable ruta_servicios_simulados {
#   description = "Ruta del directorio donde se guardara todo lo relacionado a los servicios a, b, c y d"
#   type = string
# }

locals {
  ruta_raiz_proyecto       = abspath("${path.module}/../../")
  ruta_servicios_simulados = abspath("${path.module}/../../servicios_simulados")
}

variable "service_name" {
  description = "Nombre del servicio dummy a instalar"
  type        = string
  default     = "servicio_dummy_A.service"
}


resource "null_resource" "servicio_a" {

  # triggers = {
  #   servicio_existe = fileexists("${var.ruta_servicios_simulados}/${var.service_name}") ? "si_existe" : "no_existe"
  # }

  # count = fileexists("${var.ruta_servicios_simulados}/${var.service_name}") ? 0 : 1

  provisioner "local-exec" {
    command = "${local.ruta_raiz_proyecto}/scripts/instala_servicio.sh ${var.service_name} ${local.ruta_servicios_simulados}"
    # command = "if [ ! -f \"${var.ruta_servicios_simulados}/${var.service_name}\" ]; then ${var.ruta_raiz_proyecto}/scripts/instala_servicio.sh ${var.service_name} ${var.ruta_servicios_simulados}; fi"
    # interpreter = ["bash", "-c"]
  }
}

# command = "${var.ruta_raiz_proyecto}/scripts/instala_servicio.sh ${var.service_name} ${var.ruta_servicios_simulados}"