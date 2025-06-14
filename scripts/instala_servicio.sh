APP_NAME=$1
INSTALL_PATH=$2

echo "Instalando $APP_NAME ..."
echo "$APP_NAME se esta instalando en $INSTALL_PATH"

for  in {1..5}; do
    echo "Instalando dependencia $i"
done

echo "Ha finalizado la instalacion"