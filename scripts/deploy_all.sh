#!/bin/bash

set -e
set -u
# set -x

modulos=("servicio_a" "servicio_b" "servicio_c" "servicio_d")

for modulo in ${modulos[@]}; do
    
    ruta="terraform/$modulo"
    
    echo "Ejecutando terraform init en $modulo"
    terraform -chdir=$ruta init
    if [ $? -ne  0 ]; then
        echo "Error al inicializar el directorio de Terraform para $modulo"
        exit 1
    fi

    echo "Ejecutando terraform apply -auto-approve"
    terraform -chdir=$ruta apply -auto-approve
    if [ $? -ne 0 ]; then
        echo "Error al ejecutar terraform apply -auto-approve"
        exit 1
    fi
    echo "Modulo $modulo desplegado con exito ✅"
done

echo "Todos los modulos se desplegaron con exito."

# Implementar en Bash un script deploy_all.sh que:
# Haga terraform init y terraform apply -auto-approve 
# en cada módulo en un orden definido por dependencias 
# locales (ej., servicio_a -> servicio_c -> servicio_b -> servicio_d).
# Capture logs de salida en logs/deploy_<timestamp>.log.