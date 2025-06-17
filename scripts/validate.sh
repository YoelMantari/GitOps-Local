#!/usr/bin/env bash

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

modulos=("terraform/servicio_a" "terraform/servicio_b" "terraform/servicio_c" "terraform/servicio_d")

echo "Iniciando validaciones de estilo y sintaxis..."
echo ""
for modulo in "${modulos[@]}"
do
    servicio="$(basename modulo)"

    echo "Ejecutando: terraform fmt en $modulo"
    terraform -chdir=$modulo fmt --recursive --check

    if [ $? -ne 0 ]; then
        echo -e "${RED}Formato incorrecto en archivos de Terraform.${NC}"
        exit 1
    else
        echo "Formato adecuado."
    fi

    echo "Ejecutando: terraform validate"
    terraform -chdir=$modulo validate >/dev/null

    if [ $? -ne 0 ]; then
        echo -e "${RED}Validacion fallida.${NC}"
        exit 1
    else
        echo "Validacion exitosa"
    fi

    echo "Detectando cambios en archivos '.tf' no confirmados"
    git diff --name-only --exit-code "*.tf" >/dev/null
    if [ $? -ne 0 ]; then
        echo -e "${RED}Hay cambios pendientes por confirmar.${NC}"
        exit 1
    else
        echo "No hay cambios por confirmar"
    fi
    echo ""
done

echo ""
echo -e "${GREEN}Todas las valiaciones han sido exitosas."
echo -e "Archivos listos para commitear.${NC}"