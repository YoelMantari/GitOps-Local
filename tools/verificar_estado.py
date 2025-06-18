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

    f = servicio_dir / "db_dummy.txt"
    return "ok" if f.exists() else f"No existe {f}"


def validar_servicio_d() -> str:
    try:
        # Creamos socket sin conexión
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)  # Timeout de 1 segundo
        
        # Probamos conectividad sin establecer conexión completa
        result = s.connect_ex((cola_host, cola_port))
        s.close()  # Cerramos el socket explícitamente
        
        # connect_ex devuelve 0 si éxito
        return "ok" if result == 0 else f"Puerto {cola_port} no responde (código: {result})"
    except Exception as e:
        return f"Error validando {cola_host}:{cola_port} ({e})"


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

    return 0 if all(v == "ok" for k, v in reporte.items() if k.startswith("servicio")) else 1


if __name__ == "__main__":
    sys.exit(main())