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

# Tests de validation PCA
echo "Tests de validation PCA..."
python scripts/pca_validation.py

# Tests d'optimisation broadcast
echo "Tests d'optimisation broadcast..."
python scripts/test_broadcast_optimization.py

# Tests du pipeline complet
echo "Tests du pipeline complet..."
python scripts/test_pipeline_complet.py

# Tests de validation des résultats
echo "Tests de validation des résultats..."
python scripts/validate_pipeline_results.py

echo "✅ Tous les tests sont passés!"
