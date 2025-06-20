# Sprint 1

## Dia 1

**Yoel Mantari**
- Se creó el repositorio y el tablero Kanban
- Se creó el `issue`: `Estructura inicial y validacion automatica`

**Mitchel Soto**
- Se creó la estructura inicial del proyecto.
  - Directorio Terraform con modulos `servicio_a` y `servicio_b` con archivos `main.tf` vacios.

## Dia 2

**Yoel Mantari**
- Se implementó el script en Python para:
  - Buscar recursivamente archivos `.tfstate` en la carpeta `terraform`.
  - Extraer los recursos definidos de cada archivo `.tfstate`.
  - Representar los recursos como nodos con formato `<modulo> <tipo> <nombre>`.
- Se desarrolló la función `buscar_archivos_estado()` para localizar los estados.
- Se desarrolló la función `extraer_recursos()` para interpretar los archivos `.tfstate`.

**Mitchel Soto**
- Se agrega script `validate.sh` que valida el formato usando `terraform apply` y la sintaxis usando `terraform validate`

## Dia 3

**Yoel Mantari**
- Se desarrolló la función `generar_dot()` para convertir los recursos extraídos en un grafo en formato DOT.
- Se implementó la función `main()` para integrar todo el flujo:
  - Buscar estados.
  - Extraer recursos.
  - Generar y guardar el archivo `infra.dot`.
- Se escribió el archivo `infra.dot` con los nodos encontrados.

**Mitchel Soto**
- Se mejora el script `validate.sh`
- Se crea el hook de `pre-commit` que ejecutara el script `validate.sh`
- Se crea el hook `message-commit` que validará el formato del mensaje de los commits

## Dia 4
- 

## Dia 5

**Yoel Mantari**
- Se realizó el Pull Request desde la rama `feature/terraform-inicial` hacia la rama `main`
- Se creó el tag `v0.0.1.0-alpha` correspondiente a la primera versión del proyecto.
- Se eliminaron las ramas personales `feature/terraform-inicial-mitchel` y `feature/terraform-inicial-yoel`.
- Se creo en el repositorio remoto la rama de trabajo `feature/deploy-pipeline`.

# Sprint 2

## Dia 6

**Mitchel Soto**
- Se definio el `null_resource` para los servicios servicio_c y servicio_d (commit: `28d9b20`)
- Implemente el script `deploy_all.sh` (commit: `28d9b20`).

## Dia 7

**Mitchel Soto**
- Se agrega script en python `cola_dummy.py` para iniciar proceso que escuche en un puerto local (`1234`) (commit: `a500b72`).
- Se mejora script en bash `deploy_all.sh` (commit: `76f99b5`) para
  - Capturar la salida al ejecutar comandos terraform y enviarlos a `logs/deploy_<timestamp>.log`
  - Mejorar salida de script.
  - Mejorar presentación de script. Agregar color verde para ultima linea de salida cuando todos los despliegues han sido exitosos.
- Se modifica `main.tf` en modulo `servicio_d` para que `command` ejecute correctamente el script `cola_dummy.py` (commit: `37faf2d`)
- Se modificó hook `commit-msg` para que (alcance) pueda aceptar letras mayusculas.
- Se refactorizo script `validate.sh` para mejor presentación y para que realice validaciones en modulos `servicio_c` y `servicio_d` y color en los mensajes de salida (commit `68c6226`).
- Se refactorizo script `instala_servicio.sh` para que sea el script responsable de iniciar la simulacion de instalación de los servicios dummy `servicio_a` y `servicio_b` (commit `960da79`).


# Dia 8

**Mitchel Soto**
- Se mejoro script `cola_dummy.py` para que reciba una conexión mediante el comando `nc <IP> <Puerto>` y guarde los mensajes ingresados en una cola.
- Se modifico los archivos `main.tf` de los modulos de servicio para evitar *harcodeo* de parametros como la ruta absoluta del proyecto o la ruta donde se almacenaran los servicios.
- Se modifico el archivo `main.tf` principal en la carpeta `terraform` para que se gestione desde alli la inicialización del directorio terraform y los *apply* para cada servicio.
- Se implementó el script `verificar_estado.py` para validar el estado de los servicios desplegados.
  - Verifica la existencia de los archivos `.service` de `servicio_a` y `servicio_b`.
  - Comprueba la existencia del archivo `db_dummy.txt` generado por `servicio_c`.


## Día 9
**Yoel Mantari**
- Verifica que el proceso `servicio_d` esté escuchando correctamente en el puerto `1234`.
- Se implementa validación de cada servicio `ok` o descripción del error.
- Se genera automáticamente el archivo `reporte_validacion.json`.


# Sprint

# Dia 10
- Se crea el script `rollaback` para que restaure el estado de `terraform.tfstate` dado un tag
- Adicionalmente se incluyo un script `guarda_tag_state.sh` para automatizar la creación de un tag y copiar el estado actual de terraform (`terraform.tfstate`) hacia el directorio `backups`

**Yoel Mantari**
- Se creo el script Bash simular_drift.sh con el objetivo de simular un drift en la infraestructura local, lo cual:
  - Modifica manualmente usando sed uno de los archivos de configuración .tf para alterar el nombre de un recurso.
  - Ejecuta terraform plan para detectar el drift provocado.
  - Registra la salida completa del plan en el archivo.
  - Incluye una recomendación para ejecutar terraform plan y terraform apply como acciones correctivas.

## Día 11

**Yoel Mantari**
- Se refactorizo el script generar_diagrama.py para integrarlo completamente con la lógica de drift:
  - Se implemento la función detectar_drift_en_log() .
  - Esta función analiza el log generado por terraform plan y extrae los recursos que presentan drift, según su tipo y nombre.
  - Se agregó la función generar_drift_report() que:
  - Genera un archivo drift_report.md con una lista clara de los recursos afectados por drift.
  - Lee automáticamente el ultimo log generado por simular_drift.sh.
  - Detecta los recursos modificados y los resalta en rojo dentro del grafo generado.
  - Elimina aristas transitivas para simplificar la visualización de dependencias.
