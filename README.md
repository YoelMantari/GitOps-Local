# GitOps-Local

## Sprint 2

### Estructura del proyecto

```text
GitOps-Local
├── CHANGELOG.md
├── README.md
├── scripts
│   ├── cola_dummy.py
│   ├── deploy_all.sh
│   ├── instala_servicio.sh
│   └── validate.sh
├── terraform
│   ├── main.tf
│   ├── servicio_a
│   │   ├── main.tf
│   ├── servicio_b
│   │   ├── main.tf
│   ├── servicio_c
│   │   ├── main.tf
│   └── servicio_d
│       ├── main.tf
└── tools
    ├── generar_diagrama.py
    └── verificar_estado.py
```

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

La ruta de ejecución de Python, solo si es necesario. Se muestra el valor por defecto:

```python
variable "ruta_raiz_proyecto" {
  description = "Ruta raiz del directorio principal del proyecto"
  type = string
  default = "python3" # Modificar aqui
}
```

### Paso 1
Estando el el directorio raíz `/GitOps-Local`

```sh
GitOps-Local$ ./scripts/deploy_all.sh 
```

### Paso 2
Comprobar que el proceso Python esta escuchando en un puerto local.

```sh
netstat -ltnp | grep 1234
```

- `-l`: solo sockets en **escucha**
- `t` : solo **TCP**.
- `-n`: Muestra IP y puerto
- `-p`: Muestra el programa/proceso que abrió el puerto


Para conectarse, ejecutar en otra terminal:

```sh
nc localhost 1234
```

Luego escribir en el terminal los mensajes necesarios. Al hacer enter despues de ingresar cada mensaje, saldra en la siguiente línea "Se agrego: 'aqui el mensaje' a la cola". Si se desea obtener todos los mensajes de la cola, ingresar: "GET".

**Nota**
Omitir `-p` si hay porblemas con sudo.



Para matar el proceso manualmente:

```sh
kill <PID>
```

### Paso 3
Generar el diagrama.
Estando situado en el directorio raíz del proyecto

```sh
GitOps-Local$ python3 tools/generar_diagrama.py
GiOps-Local$ dot -Tpng infra.dot -o infra.png
```
### Paso 4
Genere reporte en JSON con la validación de cada módulo.

```sh
GitOps-Local$ python3 tools/verificar_estado.py 
```

## Sprint 1

Estructura del proyecto

```text
└── terraform
    ├── servicio_a
    │           └── main.tf
    └── servicio_b
        └── main.tf
├── scripts
│   └── validate.sh
├── CHANGELOG.md
├── README.md
```

Para definir la carpeta que usara Git para lanzar los hooks:

```sh
git config core.hooksPath .git_hooks
```

---

Estando en el directorio raíz del proyecto

```sh
$ cd terraform/servicio_a
$ terraform init
```

Lo mismo para `terraform/servicio_b`

Luego regresar al directorio raíz

```sh
$ cd ../..
# Y se debe encontrar en 
.../GitOps-Local
```
Ejecutar el script `validate.sh`
```sh
./scripts/validate.sh 
```
Este script `validate.sh` tambien se ejecuta durante el hook `pre-commit`


### Generación del diagrama de infraestructura

Se incluye `tools/generar_diagrama.py` que permite generar automáticamente un grafo DOT con los recursos aplicados.

#### Generar `infra.dot`:

```sh
python3 tools/generar_diagrama.py > infra.dot
```

##### Generar `infra.png` a partir de `infra.dot` (requiere Graphviz instalado):

```sh
dot -Tpng infra.dot -o infra.png
```

