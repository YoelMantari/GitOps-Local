resource "null_resource" "servicio_c_db" {
  provisioner "local-exec" {
    command = <<-EOT
      echo "Instalando servicio de base de datos"
      mkdir -p ${path.root}/servicios/db_dummy.txt
    EOT
  }
}