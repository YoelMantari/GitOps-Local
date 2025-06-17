#!/bin/bash

set -e
set -u
# set -x

GREEN='\033[0;32m'
NC='\033[0m'

MODULOS=("servicio_a" "servicio_c" "servicio_b" "servicio_d")
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
DIR_LOG="logs"
FILE_LOG="deploy_$TIMESTAMP.log"
mkdir -p $DIR_LOG

echo "Iniciando deploy de modulos"
for modulo in ${MODULOS[@]}; do
    echo ""
    ruta="terraform/$modulo"
    echo "Ejecutando terraform init en $modulo"
    terraform -chdir=$ruta init -no-color >> "$DIR_LOG"/"$FILE_LOG" 2>&1
    if [ $? -ne  0 ]; then
        echo "Error al inicializar el directorio de Terraform para $modulo"
        exit 1
    fi

    echo "Ejecutando terraform apply -auto-approve"
    terraform -chdir=$ruta apply -auto-approve -no-color >> "$DIR_LOG"/"$FILE_LOG" 2>&1
    if [ $? -ne 0 ]; then
        echo "Error al ejecutar terraform apply -auto-approve"
        exit 1
    fi
    echo "Modulo $modulo desplegado con exito ✅"
done

echo ""
printf "${GREEN}Todos los modulos se desplegaron con exito.${NC}\n"

# Implementar en Bash un script deploy_all.sh que:
# Haga terraform init y terraform apply -auto-approve 
# en cada módulo en un orden definido por dependencias 
# locales (ej., servicio_a -> servicio_c -> servicio_b -> servicio_d).
# Capture logs de salida en logs/deploy_<timestamp>.log.