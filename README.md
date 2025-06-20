# GitOps-Local

### Estructura del proyecto

text
├── CHANGELOG.md
├── infra.dot
├── infra.png
├── logs
│   ├── deploy_2025(varios)
├── README.md
├── reporte_validacion.json
├── scripts
│   ├── cola_dummy.py
│   ├── deploy_all.sh
│   ├── guarda_tag_state.sh
│   ├── instala_servicio.sh
│   ├── rollback.sh
│   ├── simular_drift.sh
│   └── validate.sh
├── servicios_simulados
│   ├── db_dummy.txt
│   ├── servicio_dummy_A.service
│   └── servicio_dummy_B.service
├── terraform
│   ├── main.tf
│   ├── servicio_a
│   │   ├── main.tf
│   │   └── terraform.tfstate
│   ├── servicio_b
│   │   ├── main.tf
│   │   └── terraform.tfstate
│   ├── servicio_c
│   │   ├── main.tf
│   │   └── terraform.tfstate
│   └── servicio_d
│       ├── main.tf
│       └── terraform.tfstate
└── tools
    ├── generar_diagrama.py
    └── verificar_estado.py



### Paso 0

Para definir la carpeta que usara Git para lanzar los hooks:

```sh
git config core.hooksPath .git_hooks
```

Asignar los permisos necesarios a los scripts

```sh
GitOps-Local$ chmod +x scripts/deploy_all.sh
GitOps-Local$ chmod +x scripts/instala_servicio.sh
GitOps-Local$ chmod +x scripts/validate.sh
```

Modificar variables:

Modificar la ruta de ejecución de Python en el archivo main.tf del modulo servicio_d

```python
variable "python_exec" {
  description = "Ruta al ejecutable de Python."
  type        = string
  default     = "python3" # Modifica aqui
}
```

### Paso 1
Estando el el directorio raíz /GitOps-Local

```sh
GitOps-Local$ ./scripts/deploy_all.sh 
```

### Paso 2
Comprobar que el proceso Python esta escuchando en un puerto local.

```sh
netstat -ltnp | grep 1234
```

- `-l`: solo sockets en *escucha*
- `-t` : solo *TCP*.
- `-n`: Muestra IP y puerto
- `-p`: Muestra el programa/proceso que abrió el puerto


Para conectarse, ejecutar en otra terminal:

```sh
nc localhost 1234
```

Luego escribir en el terminal los mensajes necesarios. Al hacer enter despues de ingresar cada mensaje, saldra en la siguiente línea "Se agrego: 'aqui el mensaje' a la cola". Si se desea obtener todos los mensajes de la cola, ingresar: "GET".

*Nota*
Omitir `-p` si hay porblemas con sudo.



Para matar el proceso manualmente:

```sh
kill <PID>
```

### Paso 3

Simular drift

```sh
GitOps-Local$ ./scripts/simular_drift.sh
```


### Paso 4
Generar el diagrama y reporte del drift.
Estando situado en el directorio raíz del proyecto

```sh
GitOps-Local$ python3 tools/generar_diagrama.py
GiOps-Local$ dot -Tpng infra.dot -o infra.png
```

### Paso 5
Genere reporte en JSON con la validación de cada módulo.

```sh
GitOps-Local$ python3 tools/verificar_estado.py 
```

### Paso 6
Realizar un rollback. Para ello se debe ingresar un tag. La convención de tags utilizada en este proyecto es `vX.Y.Z`

```sh
./scripts/rollback.sh
```

Para crear un tag y guardar los estados `tfstate` en el directorio `backups` de los modulos `servicio_a`,`servicio_b`, `servicio_c` y `servicio_d`

```sh
./guarda_tag_state.sh
```

