#!/usr/bin/env bash

path="terraform/servicio_a"

echo "Iniciando modulo 'servicio_a'"
terraform -chdir=$path init

echo "Ejecutando: terraform fmt"
terraform -chdir=$path fmt

echo "Ejecutando: terraform validate"
terraform -chdir=$path validate

if [ $? -ne 0 ]; then
    echo "Validacion fallida"
    exit 1

else
    echo "Validacion exitosa"
    exit 0
fi