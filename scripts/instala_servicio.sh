#!/usr/bin/bash

set -e

SERVICE_NAME=$1
INSTALL_PATH=$2

echo "Instalando $SERVICE_NAME ..."
echo "$SERVICE_NAME se esta instalando en $INSTALL_PATH"
echo "Iniciando la instalacion de '$SERVICE_NAME ..."
if [ ! -d "$INSTALL_PATH" ]; then
    mkdir -p "$INSTALL_PATH"
fi

if [ ! -f "${INSTALL_PATH}/${SERVICE_NAME}" ]; then
    echo "Servicio dummy instalado el $(date +%Y-%m-%d) a las $(date +%H:%M:%S)" >> "$INSTALL_PATH"/"$SERVICE_NAME"
    echo "Realizando configuraciones necesarias..."
    echo "Verificando dependencias"
    echo "Ha finalizado la instalacion exitosamente"
else
    echo "El servicio ${SERVICE_NAME} ya existe"
    exit 0
fi