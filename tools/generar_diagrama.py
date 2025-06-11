import json
import sys
from pathlib import Path

raiz_terraform = Path("terraform")
arch_dot = Path("infra.dot")


def buscar_archivos_estado(raiz_tf: Path) -> list[Path]:
    """
    Busca recursivamente en la carpeta terraform
    archivos con extension .tfstate y los devuelve
    en una lista
    """
    return list(raiz_tf.rglob("*.tfstate"))

