# GitOps-Local


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

Aquí te dejo tu **README actualizado** con todo lo que tú ya tienes + lo que has hecho del `generar_diagrama.py`, `infra.dot` e `infra.png`, de manera clara y bien estructurada:

````markdown
# GitOps-Local

## Estructura del proyecto

```text
└── terraform
    ├── servicio_a
    │   ├── main.tf
    │   └── terraform.tfstate
    └── servicio_b
        ├── main.tf
        └── terraform.tfstate
├── scripts
│   └── validate.sh
├── tools
│   └── generar_diagrama.py
├── infra.dot
├── infra.png
├── CHANGELOG.md
├── README.md
````

---

## Configuración de Git hooks

Para definir la carpeta que usará Git para lanzar los hooks personalizados:

```sh
git config core.hooksPath .git_hooks
```

---

## Validación de los módulos Terraform

Estando en el directorio raíz del proyecto:

```sh
cd terraform/servicio_a
terraform init
```

Repetir para:

```sh
cd ../servicio_b
terraform init
```

Luego regresar al directorio raíz:

```sh
cd ../..
# Y se debe encontrar en 
.../GitOps-Local
```

Ejecutar el script `validate.sh` para validar el formato y la sintaxis de los módulos:

```sh
./scripts/validate.sh
```


## Generación del diagrama de infraestructura

Se incluye `tools/generar_diagrama.py` que permite generar automáticamente un grafo DOT con los recursos aplicados.

##### Generar `infra.dot`:

```sh
python3 tools/generar_diagrama.py > infra.dot
```

##### Generar `infra.png` a partir de `infra.dot` (requiere Graphviz instalado):

```sh
dot -Tpng infra.dot -o infra.png
```
