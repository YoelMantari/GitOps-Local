#!/usr/bin/bash

TAG=$1
LRED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

if [ $# -ne 1 ]; then
    echo "Debe ingresar un tag"
    exit 1
fi

git show $TAG #>> /tmp/rollback.log 2>&1
if [ $? -ne 0 ]; then
    echo -e "${LRED}El tag '$TAG' no existe${NC}"
    exit 1
fi

echo "El tag '$TAG' existe"
DIR_TR="terraform"
MODULOS=("servicio_a" "servicio_c" "servicio_b" "servicio_d")
DIR_TAG=$(echo "$TAG" | sed 's/\./_/g')
DIR_BACKUPS="backups/$DIR_TAG"

for modulo in ${MODULOS[@]}; do
    cp -p "$DIR_BACKUPS/$modulo/tfstate_$TAG.tfstate" "terraform/$modulo/terraform.tfstate"
done

echo -e "${GREEN}Restaurando a version ${TAG}${NC}"
echo ""
./scripts/deploy_all.sh