#!/usr/bin/env bash
# scripts/simular_drift.sh

set -e
set -u

MODULO="servicio_a"
RUTA_TF="terraform/$MODULO/main.tf"
LOG_DIR="logs"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
LOG_FILE="$LOG_DIR/drift_$TIMESTAMP.log"

ORIGINAL="servicio_dummy_A.service"
DRIFTED="servicio_drift_A.service"

# crear carpeta de logs si no existe
mkdir -p "$LOG_DIR"

echo "Simulando drift en módulo: $MODULO"
echo "Reemplazando '$ORIGINAL' por '$DRIFTED' en $RUTA_TF"

# hacemos una copia de respaldo del archivo original
cp "$RUTA_TF" "$RUTA_TF.bak"

# modificamos el archivo con sed
sed -i "s/$ORIGINAL/$DRIFTED/g" "$RUTA_TF"

echo "Ejecutando terraform plan..."
terraform -chdir="terraform/$MODULO" plan -no-color | tee "$LOG_FILE"

echo "Resultado guardado en $LOG_FILE"