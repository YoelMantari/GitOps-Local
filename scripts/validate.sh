#!/usr/bin/env bash

modulos=("terraform/servicio_a" "terraform/servicio_b")

for modulo in "${modulos[@]}"
do
    servicio="$(basename modulo)"

    echo "Ejecutando: terraform fmt en $servicio"
    terraform -chdir=$modulo fmt --recursive --check

    if [ $? -ne 0 ]; then
        echo "Formato incorrecto en archivos de Terraform."
        exit 1
    else
        echo "Formato adecuado."
    fi

    echo "Ejecutando: terraform validate"
    terraform -chdir=$modulo validate

    if [ $? -ne 0 ]; then
        echo "Validacion fallida"
        exit 1
    fi

    echo "Detectando cambios en archivos '.tf'"
    cambios=$(git status --porcelain *.tf)
    if [ -n "$cambios" ]; then
        echo "Hay cambios pendientes por confirmar"
        exit 1
    else
        echo "No hay cambios por confirmar. Todo ok"
    fi
done