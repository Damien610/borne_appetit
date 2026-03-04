#!/bin/bash

# Script pour packager le code Lambda

cd "$(dirname "$0")"

# Créer un répertoire temporaire
rm -rf build
mkdir -p build

# Copier le code source
cp -r src/* build/

# Installer les dépendances Python
pip install -t build/ PyJWT boto3 --quiet

# Créer le zip
cd build
zip -r ../lambda.zip . -q
cd ..

# Nettoyer
rm -rf build

echo "✅ Lambda package créé : lambda.zip"
