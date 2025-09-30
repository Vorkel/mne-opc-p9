# PRD Brief - Projet P9 Fruits! Classification

## 1. Présentation / Description du Projet

**Projet :** Développement d'une architecture Big Data pour la classification d'images de fruits
**Contexte :** Start-up AgriTech "Fruits!" - Application mobile de reconnaissance de fruits
**Objectif :** Mise en place d'une chaîne de traitement PySpark scalable avec EMR AWS

### Vision du Projet

La start-up "Fruits!" développe des solutions innovantes pour la récolte des fruits en préservant la biodiversité. Dans un premier temps, l'entreprise souhaite créer une application mobile permettant aux utilisateurs de photographier un fruit et d'obtenir des informations détaillées sur celui-ci.

Cette application servira à :

- Sensibiliser le grand public à la biodiversité des fruits
- Développer une première version du moteur de classification d'images
- Construire l'architecture Big Data nécessaire pour les futurs robots cueilleurs intelligents

### Défi Technique

Le projet consiste à reprendre et améliorer un notebook PySpark existant (3302 lignes) développé par un alternant, en ajoutant :

- La diffusion des poids du modèle TensorFlow sur les clusters (broadcast)
- Une étape de réduction de dimension PCA en PySpark
- La migration vers un environnement cloud AWS EMR avec conformité RGPD

## 2. Public Cible

### Public Principal

- **Utilisateurs finaux :** Grand public utilisant l'application mobile de reconnaissance de fruits
- **Développeurs :** Équipe technique de la start-up pour le développement des robots cueilleurs

### Public Secondaire

- **Évaluateurs :** Jury de soutenance pour validation des compétences Big Data
- **Investisseurs :** Démonstration de la capacité technique de l'entreprise

## 3. Principaux Avantages / Fonctionnalités

### Fonctionnalités Core

**Pipeline de Traitement d'Images :**

- Ingestion de 87 000+ images du dataset Fruits-360
- Preprocessing et normalisation des images
- Extraction de features avec MobileNetV2 (transfer learning)
- Réduction de dimension PCA pour optimiser les performances
- Sauvegarde des résultats sur stockage cloud

**Architecture Big Data Scalable :**

- Traitement distribué avec Apache Spark/PySpark
- Cluster EMR AWS pour calculs parallèles
- Stockage S3 pour données et résultats
- Conformité RGPD (serveurs européens eu-west-1)

**Optimisations de Performance :**

- Broadcast des modèles TensorFlow sur tous les workers
- Partitioning intelligent des données
- Mise en cache des DataFrames fréquemment utilisés
- Auto-scaling du cluster selon la charge

### Avantages Concurrentiels

**Technique :**

- Architecture cloud-native scalable
- Pipeline de ML optimisé pour le Big Data
- Conformité réglementaire européenne
- Coûts maîtrisés avec instances spot et résiliation rapide

**Business :**

- Première version du moteur de classification
- Base technique pour les futurs robots cueilleurs
- Sensibilisation du public à la biodiversité
- Démonstration de capacité technique pour levée de fonds
- **Coûts maîtrisés** : Optimisation maximale des dépenses AWS (budget max : 10€)

## 4. Technologies / Architecture Utilisées

### Stack Principal

**Big Data & Cloud :**

- **Apache Spark 3.4** : Moteur de calcul distribué
- **PySpark** : API Python pour Spark
- **AWS EMR** : Cluster de calcul distribué
- **Amazon S3** : Stockage des données (région eu-west-1)
- **AWS IAM** : Gestion des permissions et sécurité

**Machine Learning :**

- **TensorFlow/Keras** : Deep learning et transfer learning
- **MobileNetV2** : Architecture CNN pré-entraînée
- **scikit-learn** : Machine learning classique (PCA)
- **NumPy/Pandas** : Manipulation des données

**Développement :**

- **Python 3.9+** : Langage principal
- **Poetry** : Gestion des dépendances
- **JupyterHub** : Interface de développement sur EMR
- **Ruff** : Linting et formatage

### Architecture Technique

**Pipeline de Traitement :**

1. **Ingestion** : Chargement des images depuis S3
2. **Preprocessing** : Normalisation et préparation
3. **Feature Extraction** : MobileNetV2 avec broadcast
4. **PCA** : Réduction de dimension en PySpark
5. **Sauvegarde** : Stockage des résultats sur S3

**Sécurité & Conformité :**

- **RGPD** : Données traitées sur serveurs européens (eu-west-1)
- **Chiffrement** : AES-256 en transit et au repos
- **IAM** : Permissions minimales nécessaires
- **VPC** : Réseau privé pour le cluster

**Optimisations de Coûts (CRITIQUE) :**

- **Instances Spot** : Réduction des coûts jusqu'à 90% (priorité absolue)
- **Instances Graviton2** : Réduction de 35% des coûts + 15% de performance
- **Auto-scaling** : Ajustement dynamique des workers selon la charge
- **Résiliation immédiate** : Arrêt automatique après traitement
- **S3 comme stockage principal** : Séparation stockage/calcul pour flexibilité
- **Formats optimisés** : Parquet/ORC pour réduire les coûts de traitement
- **Monitoring strict** : Alertes budget et surveillance continue des coûts

### Livrables

**Technique :**

- Notebook PySpark exécutable sur EMR
- Dataset traité et matrices PCA sur S3
- Scripts de déploiement automatisé
- Documentation technique complète

**Présentation :**

- Support PowerPoint pour soutenance (20 min)
- Démonstration en direct du pipeline
- Documentation des choix architecturaux
- Métriques de performance et coûts

---

**Statut :** En cours de développement
**Responsable :** Data Scientist
**Durée estimée :** 10 jours de développement + 2 jours de buffer
