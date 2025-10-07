#!/bin/bash
# Script de build para Vercel
# Copia archivos estáticos a la carpeta public

echo "Copiando archivos estáticos..."

# Crear directorios
mkdir -p public/static/css
mkdir -p public/static/js

# Copiar archivos
cp -r app/static/css/* public/static/css/
cp -r app/static/js/* public/static/js/

echo "Archivos estáticos copiados exitosamente."
