#!/usr/bin/env python3
import json
import re
import os
import datetime
from pathlib import Path
from collections import defaultdict, deque

raiz_terraform = Path("terraform")
arch_dot = Path("infra.dot")
drift_report_md = Path("drift_report.md")
logs_dir = Path("logs")

def buscar_archivos_estado(raiz_tf: Path) -> list[Path]:
    return list(raiz_tf.rglob("*.tfstate"))

def extraer_recursos_dependencias(ruta_estado: Path):
    datos = json.loads(ruta_estado.read_text())
    nodos, aristas = [], []
    for recurso in datos.get("resources", []):
        if recurso["type"] not in ("null_resource", "local_file"):
            continue
        # Nombre del nodo
        if recurso["type"] == "local_file":
            dst = f"{recurso['type']}.{recurso['name']}"
        else:
            dst = f"{recurso['type']} {recurso['name']}"
        nodos.append(dst)
        # Dependencias
        for inst in recurso.get("instances", []):
            for dep in inst.get("dependencies", []):
                partes = dep.split(".")
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
    drifted = []
    content = log_file.read_text()
    pattern = re.compile(r'^[~\-\+]\s+resource\s+"(null_resource|local_file)"\s+"([^"]+)"')
    if "Terraform will perform the following actions:" in content:
        acciones = content.split("Terraform will perform the following actions:")[-1]
        for line in acciones.splitlines():
            m = pattern.search(line.strip())
            if m:
                t, name = m.group(1), m.group(2)
                drifted.append(f"{t}.{name}" if t == "local_file" else f"{t} {name}")
    return sorted(set(drifted))

def filtrar_aristas_transitivas(aristas: list[tuple[str, str]]) -> list[tuple[str, str]]:
    grafo = defaultdict(set)
    for src, dst in aristas:
        grafo[src].add(dst)
    def tiene_ruta_alterna(src, dst):
        q = deque([src])
        vistos = {src}
        while q:
            u = q.popleft()
            for v in grafo[u]:
                if u == src and v == dst:
                    continue
                if v == dst:
                    return True
                if v not in vistos:
                    vistos.add(v)
                    q.append(v)
        return False
    resultado = []
    for src, dst in aristas:
        if not tiene_ruta_alterna(src, dst):
            resultado.append((src, dst))
    return resultado

def generar_dot(nodos, aristas, drifted_resources):
    lineas = ["digraph Infra {", "  graph [rankdir=LR];"]
    for nodo in dict.fromkeys(nodos):
        # Forma
        if nodo.startswith("local_file"):
            shape = "trapezium"
        elif nodo.startswith("null_resource servicio_c"):
            shape = "cylinder"
        elif nodo.startswith("null_resource servicio_d"):
            shape = "trapezium"
        else:
            shape = "box"
        # Color y estilo
        if nodo in drifted_resources:
            color, style = "red", "bold"
        else:
            color, style = "black", "solid"
        lineas.append(f'  "{nodo}" [shape={shape}, color="{color}", fontcolor="{color}", style="{style}"];')
    for ini, dest in aristas:
        lineas.append(f'  "{ini}" -> "{dest}";')
    lineas.append("}")
    return "\n".join(lineas)

def generar_drift_report(drifted_resources):
    with drift_report_md.open("w") as f:
        f.write(f"# Reporte de Drift de Terraform\n\n")
        f.write(f"**Fecha y Hora:** {datetime.datetime.now():%Y-%m-%d %H:%M:%S}\n\n")
        if drifted_resources:
            f.write("Se detectaron los siguientes recursos con **drift**:\n\n")
            for r in sorted(drifted_resources):
                f.write(f"- `{r}`\n")
            f.write("\n---\n\n")
            f.write("## Acción Sugerida\n\n")
            f.write("Revisar módulos afectados, ejecutar `terraform plan` y luego `terraform apply`.\n")
        else:
            f.write("🎉 ¡No se detectó ningún drift!\n")
    print(f"[+] Reporte generado en {drift_report_md}")

def main():
    # 1) Leer último log de drift
    logs = sorted(logs_dir.glob("drift_*.log"), key=os.path.getmtime, reverse=True)
    if logs:
        latest = logs[0]
        print(f"Analizando log: {latest}")
        drifted = detectar_drift_en_log(latest)
    else:
        print("No se encontraron logs de drift.")
        drifted = []
    generar_drift_report(drifted)

    # 2) Recolectar estados
    estados = buscar_archivos_estado(raiz_terraform)
    if not estados:
        raise RuntimeError(f"No hay .tfstate en {raiz_terraform}")
    nodos, aristas = [], []
    for e in estados:
        n, a = extraer_recursos_dependencias(e)
        nodos.extend(n)
        aristas.extend(a)

    # 3) Eliminar duplicados y filtrar transitivas
    aristas = list(set(aristas))
    aristas = filtrar_aristas_transitivas(aristas)

    # 4) Generar y escribir el grafo .dot
    dot = generar_dot(nodos, aristas, drifted)
    arch_dot.write_text(dot)
    print(f"[+] Grafo DOT escrito en {arch_dot}")

if __name__ == "__main__":
    main()
