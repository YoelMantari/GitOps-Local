import json
import socket
import time
import sys
from pathlib import Path


raiz_proyecto = Path(__file__).parents[1]
raiz_tf = raiz_proyecto / "terraform"
estado = list(raiz_tf.rglob("*.tfstate"))
reporte_archivo = raiz_proyecto / "reporte_validacion.json"
servicio_dir = raiz_proyecto / "servicios_simulados"
cola_host = "127.0.0.1"
cola_port = 1234


