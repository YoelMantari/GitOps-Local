#!/usr/bin/bash

TAG=$1

if [[ $# -ne 1 ]]; then
    echo "Debe ingresar el nombre del tag. Debe tener este formato vX.Y.Z"
    exit 1
fi

read -p "Ingresa el mensaje del tag $TAG: " mensaje
MODULOS=("servicio_a" "servicio_b" "servicio_c" "servicio_d")
DIR_TR=terraform
DIR_TAG=$(echo "$TAG" | sed 's/\./_/g')
DIR_BACKUPS="backups/$DIR_TAG"
mkdir -p $DIR_BACKUPS
echo ""
echo "Copiando los archivos tfstate hacia el directorio $DIR_BACKUPS"

for modulo in ${MODULOS[@]}; do
    mkdir -p "$DIR_BACKUPS/$modulo"
    cp "$DIR_TR/$modulo/terraform.tfstate" "$DIR_BACKUPS/$modulo/tfstate_$TAG.tfstate"
    echo "El archivo 'terraform.tfstate' de $modulo se ha copiado a '$DIR_BACKUPS/$modulo'"
done
echo ""
echo "Se creará el tag $TAG con el mensaje: '$mensaje'"
git tag -a $TAG -m "$mensaje"
echo ""
if [[ $? -eq 0 ]]; then
    echo "Se ha creado el tag exitosamente"
else
    echo "Error al crear el tag"
    exit 1
fi

