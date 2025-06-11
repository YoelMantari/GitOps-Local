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


def extraer_recursos(ruta_estado: Path) -> list[str]:
    """
    Lee un archivo .tfstate y extrae las listas de recursos aplicados
    por cada recurso retorna una cadena con su modulo, tipo y nombre
    """

    datos = json.loads(ruta_estado.read_text())
    nodos: list[str] = []

    for recurso in datos.get("resources", []):
        modulo = recurso.get("module", "")
        tipo = recurso["type"]
        nombre = recurso["name"]
        direccion = (
            f"{modulo} {tipo} {nombre}"
            if modulo else f"{tipo} {nombre}"
            )
        nodos.append(direccion)
    return nodos


def generar_dot(nodos: list[str]) -> str:
    """
    Genera el texto para el grafo dot a partir de una lista de nodos
    y retorna un string para el contenido del archivo .dot
    """

    lineas = ["digraph Infra {", " graph [rankdir=LR];"]
    for nodo in nodos:
        lineas.append(f' "{nodo}" [shape=box];')
    lineas.append("}")
    return "\n".join(lineas)


def main():
    # se busca los archivos .tfstate en la carpeta terraform
    estados_tf = buscar_archivos_estado(raiz_terraform)
    if not estados_tf:
        raise RuntimeError(
            f"No se encontro ningun .tfstate en la carpeta {raiz_terraform}"
            )

    nodos: list[str] = []

    # se extrae los recursos de cada archivo
    # .tfstate y agregarlos a la lista de nodos
    for estado in estados_tf:
        nodos.extend(extraer_recursos(estado))

    # se genera el grafo dot y se escribe el archivo
    dot = generar_dot(nodos)
    arch_dot.write_text(dot)


if __name__ == "__main__":
    main()
