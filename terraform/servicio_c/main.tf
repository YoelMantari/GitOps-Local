module "servicio_a" {
  source = "../servicio_a"
}

locals {

  ruta_raiz_proyecto = "/home/YoeMant/Documents/CodeSublime/GitOps-Local"

  ruta_servicios_simulados = "${local.ruta_raiz_proyecto}/servicios_simulados"

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
