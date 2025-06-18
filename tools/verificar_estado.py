import json
import socket
import time
import sys
from pathlib import Path

# rutas base del proyecto y modulos
raiz_proyecto = Path(__file__).parents[1]
raiz_tf = raiz_proyecto / "terraform"
estados = list(raiz_tf.rglob("*.tfstate"))
reporte_archivo = raiz_proyecto / "reporte_validacion.json"
servicio_dir = raiz_proyecto / "servicios_simulados"
cola_host = "127.0.0.1"
cola_port = 1234


# se verifica si el archivo del servicio A existe
def validar_servicio_a() -> str:
    f = servicio_dir / "servicio_dummy_A.service"
    return "ok" if f.exists() else f"No existe {f}"


# se verifica si el archivo del servicio B existe
def validar_servicio_b() -> str:

    f = servicio_dir / "servicio_dummy_B.service"

    return "ok" if f.exists() else f"No existe {f}"


# se verifica si el archivo db_dummy.txt del servicio C fue creado
def validar_servicio_c() -> str:

    f = raiz_proyecto / "terraform" / "servicio_c" / "servicios" / "db_dummy.txt"
    return "ok" if f.exists() else f"No existe {f}"


# se verifica si el servicio D está escuchando en el puerto especificado
def validar_servicio_d() -> str:
    try:
        with socket.create_connection((cola_host, cola_port), timeout=1):
            return "ok"
    except Exception as e:
        return f"La cola no responde en {cola_host}:{cola_port} ({e})"


# se valida los servicios y genera un reporte en JSON
def main() -> int:
    if not estados:
        print(f"No se encontraron ningun archivo .tfstate en {raiz_tf}")

    reporte = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "servicio_a": validar_servicio_a(),
        "servicio_b": validar_servicio_b(),
        "servicio_c": validar_servicio_c(),
        "servicio_d": validar_servicio_d(),
    }

    reporte_archivo.write_text(json.dumps(reporte, indent=2, ensure_ascii=False))

    return 0 if all(v == "ok" for v in reporte.values()) else 1


if __name__ == "__main__":
    sys.exit(main())