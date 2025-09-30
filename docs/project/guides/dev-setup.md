# Guide de Configuration de l'Environnement de Développement

## Vue d'ensemble

Ce guide vous accompagne dans la mise en place de l'environnement de développement pour le projet P9 - Fruits! Classification. L'environnement est optimisé pour le développement Big Data avec PySpark, TensorFlow et AWS EMR.

## Prérequis Système

### Système d'Exploitation

**Recommandé :**

- **macOS** 12+ (Monterey ou plus récent)
- **Linux** Ubuntu 20.04+ ou CentOS 8+
- **Windows** 10/11 avec WSL2

**Spécifications minimales :**

- **RAM :** 8 GB (16 GB recommandé)
- **Stockage :** 20 GB d'espace libre
- **CPU :** 4 cores (8 cores recommandé)

### Outils Système

**Obligatoires :**

```bash
# Git
git --version  # >= 2.30

# Python
python3 --version  # >= 3.9

# Java (requis pour Spark)
java -version  # >= 11
```

**Recommandés :**

```bash
# Node.js (pour outils de développement)
node --version  # >= 16

# Docker (pour tests d'intégration)
docker --version  # >= 20.10
```

## Installation de Poetry

### Installation de Poetry

**macOS/Linux :**

```bash
# Installation via curl
curl -sSL https://install.python-poetry.org | python3 -

# Ou via pip
pip3 install poetry

# Vérification
poetry --version
```

**Windows :**

```powershell
# Via PowerShell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -

# Ou via pip
pip install poetry
```

### Configuration Poetry

```bash
# Configuration pour le projet
poetry config virtualenvs.in-project true
poetry config virtualenvs.prefer-active-python true

# Vérification de la configuration
poetry config --list
```

## Configuration du Projet

### Initialisation du Projet

```bash
# Cloner le repository
git clone <repository-url>
cd P9

# Initialiser l'environnement Poetry
poetry install

# Activer l'environnement virtuel
poetry shell
```

### Structure du Projet

```
P9/
├── .venv/                    # Environnement virtuel Poetry
├── data/                     # Données (ignoré par Git)
│   ├── raw/                 # Dataset brut
│   └── processed/           # Données traitées
├── docs/                    # Documentation
│   └── project/            # Documentation projet
├── notebook/                # Notebooks Jupyter
├── src/                     # Code source (à créer)
├── tests/                   # Tests unitaires (à créer)
├── pyproject.toml          # Configuration Poetry
└── README.md               # Documentation principale
```

## Configuration Python

### Création du pyproject.toml

```toml
[tool.poetry]
name = "fruits-classification"
version = "0.1.0"
description = "Big Data pipeline for fruit image classification"
authors = ["Data Scientist <email@example.com>"]
readme = "README.md"

[tool.poetry.dependencies]
python = "^3.9"
pyspark = "^3.4.0"
tensorflow = "^2.13.0"
numpy = "^1.24.0"
pandas = "^2.0.0"
scikit-learn = "^1.3.0"
matplotlib = "^3.7.0"
seaborn = "^0.12.0"
pillow = "^10.0.0"
boto3 = "^1.28.0"
jupyter = "^1.0.0"
ipykernel = "^6.25.0"

[tool.poetry.group.dev.dependencies]
ruff = "^0.1.0"
pytest = "^7.4.0"
pytest-cov = "^4.1.0"
black = "^23.0.0"
mypy = "^1.5.0"
pre-commit = "^3.4.0"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"

[tool.ruff]
line-length = 88
target-version = "py39"

[tool.ruff.lint]
select = ["E", "F", "W", "C90", "I", "N", "UP", "YTT", "S", "BLE", "FBT", "B", "A", "COM", "C4", "DTZ", "T10", "EM", "EXE", "FA", "ISC", "ICN", "G", "INP", "PIE", "T20", "PYI", "PT", "Q", "RSE", "RET", "SLF", "SLOT", "SIM", "TID", "TCH", "INT", "ARG", "PTH", "TD", "FIX", "ERA", "PD", "PGH", "PL", "TRY", "FLY", "NPY", "AIR", "PERF", "FURB", "LOG", "RUF"]
ignore = ["S101", "S104", "S108", "S110", "S112", "S311", "S603", "S607"]

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = "--cov=src --cov-report=html --cov-report=term-missing"
```

### Installation des Dépendances

```bash
# Installation de toutes les dépendances
poetry install

# Installation des dépendances de développement uniquement
poetry install --only dev

# Mise à jour des dépendances
poetry update
```

## Configuration Spark Local

### Installation de Java

**macOS (avec Homebrew) :**

```bash
brew install openjdk@11
export JAVA_HOME=/opt/homebrew/opt/openjdk@11/libexec/openjdk.jdk/Contents/Home
```

**Ubuntu/Debian :**

```bash
sudo apt update
sudo apt install openjdk-11-jdk
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
```

**Windows :**

```powershell
# Télécharger OpenJDK 11 depuis https://adoptium.net/
# Ajouter JAVA_HOME dans les variables d'environnement
```

### Configuration Spark

```bash
# Variables d'environnement Spark
export SPARK_HOME=$HOME/spark
export PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin
export PYTHONPATH=$SPARK_HOME/python:$SPARK_HOME/python/lib/py4j-*-src.zip:$PYTHONPATH

# Ajouter au .bashrc/.zshrc
echo 'export SPARK_HOME=$HOME/spark' >> ~/.bashrc
echo 'export PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin' >> ~/.bashrc
echo 'export PYTHONPATH=$SPARK_HOME/python:$SPARK_HOME/python/lib/py4j-*-src.zip:$PYTHONPATH' >> ~/.bashrc
```

## Configuration Jupyter

### Configuration Jupyter

```bash
# Génération de la configuration
jupyter notebook --generate-config

# Configuration pour le projet
mkdir -p ~/.jupyter
cat > ~/.jupyter/jupyter_notebook_config.py << EOF
c.NotebookApp.notebook_dir = '$(pwd)'
c.NotebookApp.open_browser = False
c.NotebookApp.port = 8888
c.NotebookApp.ip = '127.0.0.1'
EOF
```

### Lancement de Jupyter

```bash
# Dans l'environnement Poetry
poetry shell
jupyter notebook

# Ou directement
poetry run jupyter notebook
```

## Configuration AWS

### Configuration AWS CLI

```bash
# Installation AWS CLI
pip install awscli

# Configuration des credentials
aws configure

# Vérification
aws sts get-caller-identity
```

### Variables d'Environnement

```bash
# Création du fichier .env
cat > .env << EOF
# AWS Configuration
AWS_DEFAULT_REGION=eu-west-1
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key

# S3 Buckets
S3_DATASET_BUCKET=fruits-dataset-bucket
S3_RESULTS_BUCKET=fruits-results-bucket

# EMR Configuration
EMR_CLUSTER_NAME=fruits-classification-cluster
EMR_INSTANCE_TYPE=m5.large
EMR_WORKER_COUNT=2
EOF
```

## Outils de Qualité

### Configuration Ruff

```bash
# Linting
poetry run ruff check .

# Formatage
poetry run ruff format .

# Vérification des types
poetry run mypy src/
```

### Configuration des Tests

```bash
# Exécution des tests
poetry run pytest

# Tests avec couverture
poetry run pytest --cov=src

# Tests en mode verbose
poetry run pytest -v
```

## Scripts d'Automatisation

### Script de Démarrage

```bash
# Création du script setup.sh
cat > setup.sh << 'EOF'
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
EOF

chmod +x setup.sh
```

### Script de Tests

```bash
# Création du script test.sh
cat > test.sh << 'EOF'
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
EOF

chmod +x test.sh
```

## Vérification de l'Installation

### Checklist de Vérification

```bash
# Vérification complète
echo "Vérification de l'installation..."

# Python et Poetry
poetry --version
poetry run python --version

# Dépendances principales
poetry run python -c "import pyspark; print('PySpark OK')"
poetry run python -c "import tensorflow; print('TensorFlow OK')"
poetry run python -c "import pandas; print('Pandas OK')"
poetry run python -c "import numpy; print('NumPy OK')"

# Spark local
poetry run python -c "
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName('test').getOrCreate()
print('Spark Local OK')
spark.stop()
"

# Jupyter
poetry run jupyter --version

echo "Installation complète et fonctionnelle!"
```

## Dépannage

### Problèmes Courants

**Erreur Java :**

```bash
# Vérifier JAVA_HOME
echo $JAVA_HOME
java -version

# Corriger JAVA_HOME si nécessaire
export JAVA_HOME=/path/to/java
```

**Erreur Poetry :**

```bash
# Réinitialiser Poetry
poetry env remove python
poetry install
```

**Erreur Spark :**

```bash
# Vérifier les variables d'environnement
echo $SPARK_HOME
echo $PYTHONPATH

# Redémarrer le terminal
source ~/.bashrc
```

### Support

**Ressources utiles :**

- [Documentation Poetry](https://python-poetry.org/docs/)
- [Documentation PySpark](https://spark.apache.org/docs/latest/api/python/)
- [Documentation TensorFlow](https://www.tensorflow.org/api_docs)
- [Documentation AWS EMR](https://docs.aws.amazon.com/emr/)

---

**Dernière mise à jour :** [Date]
**Responsable :** Data Scientist
**Statut :** Prêt pour le développement
