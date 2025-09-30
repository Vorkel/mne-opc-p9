#!/bin/bash
set -e

echo "Configuration de l'environnement P9..."

# Vérification des prérequis
echo "Vérification des prérequis..."
python3 --version || { echo "❌ Python 3.9+ requis"; exit 1; }
java -version || { echo "❌ Java 11+ requis"; exit 1; }

# Installation Poetry si nécessaire
if ! command -v poetry &> /dev/null; then
    echo "Installation de Poetry..."
    curl -sSL https://install.python-poetry.org | python3 -
fi

# Configuration Poetry
echo "Configuration Poetry..."
poetry config virtualenvs.in-project true

# Installation des dépendances
echo "Installation des dépendances..."
poetry install

# Configuration des variables d'environnement
echo "Configuration de l'environnement..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "Veuillez configurer le fichier .env"
fi

echo "Configuration terminée!"
echo "Pour démarrer: poetry shell && jupyter notebook"
