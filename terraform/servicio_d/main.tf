resource "null_resource" "servicio_dummy_d" {
  
  provisioner "local-exec" {
    command = <<-EOT
      echo "Iniciando servicio de cola de mensajes | Puerto 1234"
    EOT
  }

}

// Una cola dummy (un proceso Python que escuche en un puerto local).