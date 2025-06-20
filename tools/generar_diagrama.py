import json
from pathlib import Path
import re

raiz_terraform = Path("terraform")
arch_dot = Path("infra.dot")


def buscar_archivos_estado(raiz_tf: Path) -> list[Path]:
    """
    Busca recursivamente en la carpeta terraform
    archivos con extension .tfstate y los retorna
    en una lista
    """
    return list(raiz_tf.rglob("*.tfstate"))


def extraer_recursos_dependencias(
    ruta_estado: Path
) -> tuple[list[str], list[tuple[str, str]]]:
    """
    Lee un archivo .tfstate y extrae los nombres y tipo de recursos y
    sus dependencias, y
    retorna una lista de nodos y aristas
    """

    datos = json.loads(ruta_estado.read_text())
    nodos: list[str] = []
    aristas: list[tuple[str, str]] = []

    for recurso in datos.get("resources", []):
        if recurso["type"] not in ("null_resource", "local_file"):
            continue

        # nombre del nodo
        if recurso["type"] == "local_file":
            dst = f"{recurso['type']}.{recurso['name']}"
        else:
            dst = f"{recurso['type']} {recurso['name']}"
        nodos.append(dst)

        # dependencias
        for instancia in recurso.get("instances", []):
            for dep in instancia.get("dependencies", []):
                partes = dep.split(".")

                # solo tomamos caminos con 0 o 1 aparición de module
                if len(partes) < 2 or partes[-2] not in ("null_resource", "local_file"):
                    continue

                src_type, src_name = partes[-2], partes[-1]
                if src_type == "local_file":
                    src = f"{src_type}.{src_name}"
                else:
                    src = f"{src_type} {src_name}"

                aristas.append((src, dst))

    return nodos, aristas


def detectar_drift_en_log(log_file: Path) -> list[str]:
    drift = []
    conte = log_file.read_text()
    patron = re.compile(r'^[~\-\+]\s+resource\s+"(null_resource|local_file)"\s+"([^"]+)"')
    if "Terraform will perform the following actions:" in conte:
        acciones = conte.split("Terraform will perform the following actions:")[-1]
        for linea in acciones.splitlines():
            m = patron.search(linea.strip())
            if m:
                t, name = m.group(1), m.group(2)
                drift.append(f"{t}.{name}" if t == "local_file" else f"{t} {name}")
    return sorted(set(drift))


def generar_dot(
    nodos: list[str],
    aristas: list[tuple[str, str]]
) -> str:

    """
    Genera el texto para el grafo dot a partir de una lista de nodos
    y retorna un string para el contenido del archivo .dot
    """

    lineas = ["digraph Infra {", "  graph [rankdir=LR];"]

    for nodo in dict.fromkeys(nodos):
        if "servicio_c" in nodo:
            shape = "cylinder"
        elif "servicio_d" in nodo:
            shape = "trapezium"
        else:
            shape = "box"
        lineas.append(f'  "{nodo}" [shape={shape}];')

    for ini, dest in dict.fromkeys(aristas):
        lineas.append(f'  "{ini}" -> "{dest}";')

    lineas.append("}")
    return "\n".join(lineas)


def main():
    # se busca los archivos .tfstate en la carpeta terraform
    estados_tf = buscar_archivos_estado(raiz_terraform)
    if not estados_tf:
        raise RuntimeError(
            f"No se encontro ningun .tfstate en la carpeta {raiz_terraform}"
            )

    nodos_total: list[str] = []
    aristas_total: list[tuple[str, str]] = []

    # se extrae los recursos de cada archivo
    # .tfstate y agregarlos a la lista de nodos
    for estado in estados_tf:
        nodos, aristas = extraer_recursos_dependencias(estado)
        nodos_total.extend(nodos)
        aristas_total.extend(aristas)

    # se genera el grafo dot y se escribe el archivo
    dot = generar_dot(nodos_total, aristas_total)
    arch_dot.write_text(dot)


if __name__ == "__main__":
    main()
