# Stack Technique - Projet P9 Fruits! Classification

## Vue d'ensemble

**Projet :** Développement d'une architecture Big Data pour la classification d'images de fruits
**Contexte :** Start-up AgriTech "Fruits!" - Application mobile de reconnaissance de fruits
**Objectif :** Mise en place d'une chaîne de traitement PySpark scalable avec EMR AWS

## Stack Principal

### Python & Environnement

**Gestion des dépendances :**

- **Poetry** : Gestion des dépendances et environnements virtuels
- **Python 3.9+** : Version recommandée pour compatibilité PySpark
- **Virtual Environment** : `.venv` pour isolation des packages

**Packages principaux :**

```toml
[tool.poetry.dependencies]
python = "^3.9"
pyspark = "^3.4.0"
tensorflow = "^2.5.0"
numpy = "^1.24.0"
pandas = "^2.0.0"
scikit-learn = "^1.3.0"
matplotlib = "^3.7.0"
seaborn = "^0.12.0"
pillow = "^10.0.0"
boto3 = "^1.28.0"
```

### Cloud & Big Data

**AWS Services :**

- **Amazon EMR** : Cluster de calcul distribué pour PySpark
- **Amazon S3** : Stockage des données et résultats (région eu-west-1)
- **AWS IAM** : Gestion des permissions et sécurité
- **EC2** : Instances pour le cluster EMR

**Big Data :**

- **Apache Spark** : Moteur de calcul distribué
- **PySpark** : API Python pour Spark
- **JupyterHub** : Interface de développement sur EMR

### Machine Learning & Deep Learning

**Frameworks :**

- **TensorFlow/Keras** : Deep learning et transfer learning
- **MobileNetV2** : Architecture de réseau pré-entraîné
- **scikit-learn** : Machine learning classique (PCA, etc.)

**Techniques :**

- **Transfer Learning** : Réutilisation de modèles pré-entraînés
- **Feature Extraction** : Extraction de features avec CNN
- **PCA** : Réduction de dimension en PySpark

### Données & Stockage

**Dataset :**

- **Fruits-360** : 87 000+ images de fruits classifiées
- **Format** : JPG, résolution 100x100 pixels
- **Structure** : Training/Test avec labels par classe

**Stockage :**

- **Local** : Développement et tests
- **S3** : Stockage cloud avec conformité RGPD
- **Formats** : CSV pour matrices PCA, Parquet pour optimisations

## Outils de Développement

### Qualité de Code

**Python :**

- **Ruff** : Linting et formatage rapide
- **Black** : Formatage de code (alternative)
- **Pylint** : Analyse statique de code

**Configuration Poetry :**

```toml
[tool.poetry.group.dev.dependencies]
ruff = "^0.1.0"
pytest = "^7.4.0"
jupyter = "^1.0.0"
ipykernel = "^6.25.0"
```

### Documentation & Présentation

**Documentation :**

- **Markdown** : Documentation technique
- **Jupyter Notebooks** : Documentation interactive
- **Mermaid** : Diagrammes d'architecture

**Présentation :**

- **PowerPoint** : Support de soutenance
- **Markdown** : Structure des slides
- **Captures d'écran** : Démonstrations AWS

## Architecture Technique

### Pipeline de Traitement

1. **Ingestion** : Chargement des images depuis S3
2. **Preprocessing** : Normalisation et préparation des données
3. **Feature Extraction** : Extraction avec MobileNetV2
4. **Broadcast** : Diffusion des poids du modèle sur les workers
5. **PCA** : Réduction de dimension en PySpark
6. **Sauvegarde** : Stockage des résultats sur S3

### Workflow de Développement

**Local :**

```bash
# Installation avec Poetry
poetry install

# Activation de l'environnement
poetry shell

# Exécution des tests
poetry run pytest

# Linting
poetry run ruff check .
poetry run ruff format .
```

**Cloud :**

- Développement local avec Spark local
- Tests sur cluster EMR temporaire
- Déploiement et exécution sur EMR
- Résiliation pour optimiser les coûts

## Conformité & Sécurité

### RGPD

**Conformité :**

- **Région AWS** : eu-west-1 (Europe)
- **Stockage** : Données sur serveurs européens
- **Traitement** : Calculs sur instances européennes
- **Documentation** : Traçabilité des données

### Sécurité

**AWS :**

- **IAM** : Permissions minimales nécessaires
- **VPC** : Réseau privé pour le cluster
- **SSH** : Accès sécurisé au cluster EMR
- **Encryption** : Chiffrement des données en transit et au repos

## Performance & Optimisation

### Optimisations

**Spark :**

- **Partitioning** : Optimisation des partitions
- **Caching** : Mise en cache des DataFrames
- **Broadcast** : Variables broadcast pour les modèles
- **Serialization** : Kryo pour la sérialisation

**Optimisation des Coûts (CRITIQUE) :**

- **Instances Spot** : Réduction jusqu'à 90% des coûts (PRIORITÉ ABSOLUE)
- **Instances Graviton2** : Réduction de 35% des coûts + 15% de performance
- **Auto-scaling intelligent** : Ajustement automatique selon la charge réelle
- **Résiliation immédiate** : Arrêt automatique après traitement
- **S3 comme stockage principal** : Séparation stockage/calcul
- **Formats optimisés** : Parquet/ORC pour réduire les coûts de traitement
- **Budget total estimé : 1.69€** (83% d'économie par rapport au budget de 10€)

## Monitoring & Logs

### Surveillance

**AWS :**

- **CloudWatch** : Monitoring des performances
- **EMR Console** : Suivi des jobs Spark
- **S3 Metrics** : Surveillance du stockage

**Spark :**

- **Spark UI** : Interface de monitoring
- **History Server** : Historique des applications
- **Logs** : Centralisation des logs

## Déploiement

### Environnements

**Développement :**

- Environnement local avec Poetry
- Spark local pour les tests
- Jupyter Notebook pour l'exploration

**Production :**

- Cluster EMR temporaire
- Exécution des jobs PySpark
- Sauvegarde des résultats sur S3

### Livrables

**Code :**

- Notebook PySpark exécutable
- Scripts de déploiement
- Documentation technique

**Données :**

- Dataset traité sur S3
- Matrices PCA en CSV
- Métriques de performance

**Présentation :**

- Support PowerPoint
- Démonstration en direct
- Documentation des choix techniques

---

**Dernière mise à jour :** [Date]
**Responsable :** Data Scientist
**Statut :** En cours de développement
