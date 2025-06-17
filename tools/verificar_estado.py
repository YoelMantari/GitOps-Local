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


def validar_servicio_a() -> str:
    f = servicio_dir / "servicio_dummy_A.service"
    return "ok" if f.exists() else f"No existe {f}"

def validar_servicio_b() -> str:

    f = servicio_dir / "servicio_dummy_B.service"

    return "ok" if f.exists() else f"No existe {f}"


def validar_servicio_c() -> str:

    f = raiz_proyecto / "terraform" / "servicio_c" / "servicios" / "db_dummy.txt"
    return "ok" if f.exists() else f"No existe {f}"


def validar_servicio_d() -> str:
    try:
        with socket.create_connection((cola_host, cola_port), timeout=1):
            return "ok"
    except Exception as e:
        return f"La cola no responde en {cola_host}:{cola_port} ({e})"