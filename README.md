# GitOps-Local

## Sprint 2

### Estructura del proyecto

```text
├── CHANGELOG.md
├── infra.dot
├── infra.png
├── README.md
├── requirements.txt
├── scripts
│   ├── deploy_all.sh
│   └── validate.sh
├── terraform
│   ├── servicio_a
│   │   └── main.tf
│   ├── servicio_b
│   │   └── main.tf
│   ├── servicio_c
│   │   ├── main.tf
│   └── servicio_d
│       └── main.tf
└── tools
    └── generar_diagrama.py
```


### Paso 1
Estando el el directorio raíz `/GitOps-Local`

```sh
$ ./scripts/deploy_all.sh 
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

