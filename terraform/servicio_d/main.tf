variable "python_exec" {
  description = "Ruta al ejecutable de Python."
  type = string
  default = "/home/dirac/Documents/DS/GitOps-Local/.venv/bin/python3.12"
}


resource "null_resource" "servicio_dummy_d" {
  
  provisioner "local-exec" {
    command = "nohup ${var.python_exec} /home/dirac/Documents/DS/GitOps-Local/scripts/cola_dummy.py > /tmp/cola_dummy.log 2>&1 &" 
  }
}