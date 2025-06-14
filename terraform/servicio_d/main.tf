resource "null_resource" "servicio_dummy_d" {
  
  provisioner "local-exec" {
    command = "echo Se instalo 'servicio_dummy_d'"
  }

}