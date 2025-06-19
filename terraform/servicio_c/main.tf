module "servicio_a" {
  source = "../servicio_a"
  #ruta_raiz_proyecto = var.ruta_raiz_proyecto
  #ruta_servicios_simulados = var.ruta_servicios_simulados
}

locals {

  ruta_raiz_proyecto       = abspath("${path.module}/../../")
  ruta_servicios_simulados = abspath("${path.module}/../../servicios_simulados")
  hora_local               = timeadd(timestamp(), "-5h")
}

# variable ruta_raiz_proyecto {
#   description = "Ruta del directorio principal del proyecto"
#   type = string
# }

# variable ruta_servicios_simulados {
#   description = "Ruta del directorio donde se guardara todo lo relacionado a los servicios a, b, c y d"
#   type = string
# }

resource "local_file" "db_dummy" {
  filename = "${local.ruta_servicios_simulados}/db_dummy.txt"
  content  = "Base de datos creada a las ${formatdate("YYYY-MM-DD hh:mm:ss", local.hora_local)}"
}

resource "null_resource" "servicio_c" {

  depends_on = [module.servicio_a]

  provisioner "local-exec" {
    command = <<-EOT
      if [ ! -f "${local.ruta_raiz_proyecto}/servicios_simulados/db_dummy.txt" ]; then
        echo "Instalando servicio de base de datos"
        mkdir -p "${local.ruta_servicios_simulados}"
        echo "Base de datos creada el $(date +%Y-%m-%d) a las $(date +%H:%M:%S)" >> ${local.ruta_servicios_simulados}/db_dummy.txt
      fi
    EOT
  }
}
