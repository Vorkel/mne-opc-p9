#!/bin/bash
set -e

echo "Exécution des tests..."

# Linting
echo "Linting..."
poetry run ruff check .

# Formatage
echo "Formatage..."
poetry run ruff format .

# Tests unitaires
echo "Tests unitaires..."
poetry run pytest

echo "✅ Tous les tests sont passés!"
