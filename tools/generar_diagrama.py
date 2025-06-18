import json
from pathlib import Path

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
    Lee un archivo .tfstate y extrae los nombres de recursos y
    sus dependencias, y
    retorna una lista de nodos y aristas
    """

    datos = json.loads(ruta_estado.read_text())
    nodos: list[str] = []
    aristas: list[tuple[str, str]] = []

    for recurso in datos.get("resources", []):
        if recurso["type"] != "null_resource":
            continue

        dst = f"{recurso['type']} {recurso['name']}"
        nodos.append(dst)

        for instancia in recurso.get("instances", []):
            for dep in instancia.get("dependencies", []):
                partes = dep.split(".")

                # solo tomamos caminos con 0 o 1 aparición de module
                if partes[-2] != "null_resource":
                    continue
                if partes[:-2].count("module") > 1:
                    continue 

                src = f"{partes[-2]} {partes[-1]}"
                if (src, dst) not in aristas:
                    aristas.append((src, dst))

    return nodos, aristas


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
