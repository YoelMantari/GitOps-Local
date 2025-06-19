#!/usr/bin/bash

#set -e

TAG=$1
LRED='\033[0;31m'
NC='\033[0m'

if [ $# -ne 1 ]; then
    echo "Debe ingresar un tag"
    exit 1
fi

git show $TAG >> /tmp/rollback.log 2>&1
if [ $? -ne 0 ]; then
    echo -e "${LRED}El tag '$TAG' no existe${NC}"
    exit 1
fi

echo "El tag '$TAG' existe"
TIMESTAMP=$(date +%Y-%m-%d_%H-%M-%S)
git checkout $TAG >> /tmp/rollback_$TIMESTAMP.log 2>&1

if [ $? -ne 0 ]; then 
    echo -e "${LRED}Hay cambios sin confirmar. Confirma o guarda tus cambios (stash)${NC}"
    exit 1
fi

echo "Restaurando a version $TAG"
./scripts/hola.sh


# Añadir **funcionalidad avanzada** de rollback local:
 #* Script `rollback.sh` que, dado un tag Git (p. ej., `v-0`), 
 # restaure el estado de `terraform.tfstate` correspondiente y 
 # ejecute `terraform apply` para volver al despliegue previo.
 #* El script debe:
	#* Validar que el tag existe.
	#* Copiar el backup de estado en `backups/tfstate_vX.tfstate`.
	#* Forzar el estado local y aplicar el plan.