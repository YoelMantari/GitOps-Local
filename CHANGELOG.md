# Dia 1

- Se creó el `issue`: `Estructura inicial y validacion automatica`
- Se creó la estructura inicial del proyecto.
  - Directorio Terraform con modulos `servicio_a` y `servicio_b` con archivos `main.tf` vacios.


# Dia 4

- Se eliminaron las ramas personas `feature/terraform-inicial-mitchel` y `feature/terraform-inicial-yoel`.
- Se creo en el repo remoto la rama de trabajo `feature/deploy-pipeline`.


# Dia 5
- Defini el `null_resource` para los servicios servicio_c y servicio_d (commit: `28d9b20`)
- Implemente el script `deploy_all.sh` (commit: `28d9b20`).

# Dia 6
- Se agrega script en python `cola_dummy.py` para iniciar proceso que escuche en un puerto local (`1234`) (commit: `a500b72`).
- Se mejora script en bash `deploy_all.sh` (commit: `76f99b5`) para
  - Capturar la salida al ejecutar comandos terraform y enviarlos a `logs/deploy_<timestamp>.log`
  - Mejorar salida de script.
  - Mejorar presentación de script. Agregar color verde para ultima linea de salida cuando todos los despliegues han sido exitosos.
- Se modifica `main.tf` en modulo `servicio_d` para que `command` ejecute correctamente el script `cola_dummy.py` (commit: `37faf2d`)
- Se modificó hook `commit-msg` para que (alcance) pueda aceptar letras mayusculas.
- Se refactorizo script `validate.sh` para mejor presentación y para que realice validaciones en modulos `servicio_c` y `servicio_d` y color en los mensajes de salida (commit `68c6226`).
- Se refactorizo script `instala_servicio.sh` para que sea el script responsable de iniciar la simulacion de instalación de los servicios dummy `servicio_a` y `servicio_b` (commit `960da79`).