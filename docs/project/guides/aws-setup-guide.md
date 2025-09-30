# Guide AWS - Configuration S3 et Déploiement EMR

**Version :** 1.0
**Date :** 30 septembre 2024
**Objectif :** Guide pas-à-pas pour configurer l'infrastructure AWS et exécuter le notebook sur EMR

---

## Vue d'ensemble

Ce guide vous accompagne dans :
1. Configuration d'un bucket S3 (région eu-west-1, RGPD)
2. Upload du dataset Fruits-360
3. Création d'un cluster EMR optimisé coûts
4. Exécution du notebook sur JupyterHub EMR
5. Validation des résultats et terminaison

**Durée estimée :** 6 heures
**Coûts estimés :** 1.69€ (budget max : 10€)

---

## Prérequis

### Compte AWS

- [ ] Compte AWS créé
- [ ] Carte bancaire enregistrée
- [ ] Région configurée : **eu-west-1** (Irlande - RGPD)

### Outils Locaux

- [ ] AWS CLI installé : `aws --version`
- [ ] SSH client disponible
- [ ] Navigateur web (Chrome/Firefox recommandé)

### Fichiers Nécessaires

- [ ] Dataset Fruits-360 téléchargé (~2GB)
- [ ] Notebook PySpark modifié (avec broadcast + PCA)

---

## Phase 1 : Configuration Sécurité et Budget (30 minutes)

### 1.1 Configuration Région

1. **Connexion à AWS Console** : https://console.aws.amazon.com
2. **Sélection région** : Haut à droite → **EU (Ireland) eu-west-1**
3. **Vérification** : Toutes les actions suivantes dans eu-west-1

### 1.2 Configuration AWS Budgets

**Service :** AWS Budgets
**Navigation :** Console → Services → AWS Cost Management → Budgets

**Créer un budget :**

```yaml
Nom: P9-Fruits-Classification-Budget
Type: Cost budget
Montant: 10 EUR
Période: Mensuel
```

**Alertes à configurer :**

| Seuil | Montant | Action |
|-------|---------|--------|
| Alerte 1 | 5 EUR (50%) | Email notification |
| Alerte 2 | 8 EUR (80%) | Email notification |
| Alerte 3 | 10 EUR (100%) | Email notification URGENT |

**Email de notification :** Votre adresse email

### 1.3 Configuration IAM (Permissions)

**Service :** IAM (Identity and Access Management)
**Navigation :** Console → Services → IAM

**Créer un rôle pour EMR :**

1. **IAM → Roles → Create role**
2. **Service :** EMR
3. **Use case :** EMR
4. **Permissions (policies à attacher) :**
   - `AmazonEMRServicePolicy_v2`
   - `AmazonS3FullAccess` (pour accès S3)
5. **Nom du rôle :** `EMR_DefaultRole_P9`

**Créer un rôle pour EC2 (instances EMR) :**

1. **IAM → Roles → Create role**
2. **Service :** EC2
3. **Permissions :**
   - `AmazonS3FullAccess`
   - `AmazonEMRServicePolicy_v2`
4. **Nom du rôle :** `EMR_EC2_DefaultRole_P9`

---

## Phase 2 : Configuration S3 (1 heure)

### 2.1 Création du Bucket S3

**Service :** S3 (Simple Storage Service)
**Navigation :** Console → Services → S3 → Create bucket

**Configuration du bucket :**

```yaml
Nom du bucket: fruits-classification-p9-[votre-nom]
# Exemple: fruits-classification-p9-maxime
# IMPORTANT: Le nom doit être unique globalement

Région: EU (Ireland) eu-west-1

Object Ownership: ACLs disabled (recommandé)

Block Public Access:
  - ✅ Block all public access (cocher tout)

Bucket Versioning: Disabled (économie de coûts)

Encryption:
  - Type: Server-side encryption with Amazon S3 managed keys (SSE-S3)

Object Lock: Disabled
```

**Créer le bucket** → Cliquer sur "Create bucket"

### 2.2 Structure de Dossiers S3

Créer la structure suivante dans le bucket :

```
fruits-classification-p9-maxime/
├── dataset/               # Dataset Fruits-360
│   ├── Training/         # Images d'entraînement
│   └── Test/             # Images de test
├── notebooks/            # Notebooks Jupyter
└── results/              # Résultats PCA
    └── pca_output/       # Sortie PCA Parquet
```

**Création des dossiers :**
1. Dans le bucket → **Create folder**
2. Créer : `dataset`, `notebooks`, `results`, `results/pca_output`

### 2.3 Upload du Dataset

**Option A : Via AWS Console (Interface graphique)**

1. Aller dans `dataset/`
2. **Upload** → **Add files** ou **Add folder**
3. Sélectionner le dossier `fruits-360_dataset/`
4. **Upload** (durée : 1-2 heures pour ~2GB)

**Option B : Via AWS CLI (Plus rapide, recommandé)**

```bash
# Installation AWS CLI (si pas déjà fait)
brew install awscli  # macOS
# ou: pip install awscli

# Configuration AWS CLI
aws configure
# AWS Access Key ID: [Votre clé]
# AWS Secret Access Key: [Votre clé secrète]
# Default region name: eu-west-1
# Default output format: json

# Upload du dataset
aws s3 sync ./data/raw/fruits-360_dataset/ \
  s3://fruits-classification-p9-maxime/dataset/ \
  --region eu-west-1

# Vérification
aws s3 ls s3://fruits-classification-p9-maxime/dataset/ --recursive | wc -l
# Devrait afficher ~87000 (nombre d'images)
```

**Durée upload :**
- Via Console : 1-2 heures
- Via CLI : 30-60 minutes (plus rapide)

### 2.4 Vérification S3

- [ ] Bucket créé dans eu-west-1
- [ ] Structure de dossiers créée
- [ ] Dataset uploadé (~87k fichiers)
- [ ] Permissions correctes (accès EMR)

---

## Phase 3 : Création Cluster EMR (2 heures)

### 3.1 Lancement du Wizard EMR

**Service :** EMR (Elastic MapReduce)
**Navigation :** Console → Services → EMR → Create cluster

### 3.2 Configuration du Cluster

#### Étape 1 : General Configuration

```yaml
Nom du cluster: Fruits-Classification-P9-Cluster
Region: eu-west-1
```

#### Étape 2 : Software Configuration

**Version EMR :** `emr-6.15.0` (ou dernière version stable)

**Applications à installer :**
- ✅ Spark 3.4.1
- ✅ JupyterHub 1.5.0
- ✅ Hadoop 3.3.3
- ✅ Livy 0.7.1 (optionnel, pour API REST)

**Cocher : "Use for Spark table metadata"** → Disabled (économie)

#### Étape 3 : Hardware Configuration

**Instances Master :**
```yaml
Instance type: m6g.xlarge
  - vCPU: 4
  - RAM: 16 GB
  - Architecture: ARM64 (Graviton2)
  - Prix: ~0.17€/heure (Spot)
Count: 1
Market: Spot (économie 70-90%)
```

**Instances Core (Workers) :**
```yaml
Instance type: m6g.large
  - vCPU: 2
  - RAM: 8 GB
  - Architecture: ARM64 (Graviton2)
  - Prix: ~0.10€/heure (Spot)
Count: 2
Market: Spot
```

**Auto-scaling (optionnel, recommandé) :**
```yaml
Minimum instances: 2
Maximum instances: 4
Scale-up policy:
  - Trigger: YARNMemoryAvailablePercentage < 15%
  - Add: 1 instance
Scale-down policy:
  - Trigger: YARNMemoryAvailablePercentage > 75% for 5 minutes
  - Remove: 1 instance
```

**Total coûts estimés (3 heures) :**
- Master (m6g.xlarge) : 0.51€
- Core 2x (m6g.large) : 0.60€
- **Total : 1.11€**

#### Étape 4 : Networking

```yaml
VPC: (Default VPC - eu-west-1)
Subnet: Select any subnet in eu-west-1 (a, b, ou c)
EC2 Security Groups:
  - Master: Create new (ElasticMapReduce-master)
  - Core & Task: Create new (ElasticMapReduce-slave)
```

**Configuration groupe de sécurité Master (pour JupyterHub) :**

Après création du cluster, modifier le groupe de sécurité :

1. **EC2 → Security Groups → ElasticMapReduce-master**
2. **Inbound Rules → Edit inbound rules**
3. **Add rule :**
   - Type : Custom TCP
   - Port : 9443 (JupyterHub)
   - Source : My IP (votre IP publique)
   - Description : JupyterHub access
4. **Save rules**

#### Étape 5 : Security and Access

```yaml
EC2 key pair:
  - Créer une nouvelle paire de clés SSH
  - Nom: emr-p9-keypair
  - Télécharger le fichier .pem
  - Sauvegarder dans ~/.ssh/emr-p9-keypair.pem

Permissions:
  - EMR role: EMR_DefaultRole_P9
  - EC2 instance profile: EMR_EC2_DefaultRole_P9
```

**Changer permissions du fichier .pem (macOS/Linux) :**
```bash
chmod 400 ~/.ssh/emr-p9-keypair.pem
```

#### Étape 6 : Cluster Termination

**IMPORTANT : Configuration auto-terminaison**

```yaml
Termination protection: Disabled (permet terminaison manuelle)

Auto-termination:
  ✅ Enable auto-termination
  Idle time: 3 hours
  (Termine automatiquement après 3h d'inactivité)
```

### 3.3 Lancement du Cluster

1. **Revoir la configuration** (Summary)
2. **Create cluster**
3. **Attendre démarrage** : 10-15 minutes
4. **Statut** : "Waiting" = prêt

**Vérifications :**
- [ ] Cluster status : "Waiting"
- [ ] Master public DNS disponible
- [ ] Security groups configurés
- [ ] Auto-terminaison activée

---

## Phase 4 : Connexion JupyterHub (30 minutes)

### 4.1 Récupération DNS Master

**EMR Console → Clusters → [Votre cluster]**

**Informations importantes :**
- Master public DNS : `ec2-XXX-XXX-XXX-XXX.eu-west-1.compute.amazonaws.com`
- Master security group : `sg-XXXXXXXXX`

### 4.2 Configuration Tunnel SSH (Optionnel, recommandé)

**Option A : Port forwarding SSH**

```bash
# Créer un tunnel SSH pour JupyterHub
ssh -i ~/.ssh/emr-p9-keypair.pem \
  -L 9443:localhost:9443 \
  hadoop@ec2-XXX-XXX-XXX-XXX.eu-west-1.compute.amazonaws.com

# Laisser cette fenêtre terminal ouverte
```

**Option B : Accès direct (si security group configuré)**

Utiliser directement l'URL : `https://ec2-XXX-XXX-XXX-XXX.eu-west-1.compute.amazonaws.com:9443`

### 4.3 Connexion à JupyterHub

1. **Ouvrir navigateur** : `https://localhost:9443` (avec tunnel)
   ou `https://[master-public-dns]:9443` (direct)

2. **Warning certificat SSL** :
   - Normal, certificat auto-signé
   - Cliquer "Advanced" → "Proceed" (Chrome)
   - ou "Accept Risk" (Firefox)

3. **Login JupyterHub** :
   - Username : `jovyan` (par défaut EMR)
   - Password : `jupyter` (par défaut EMR)

4. **Vérification** :
   - Jupyter notebook interface doit s'afficher
   - Kernel disponibles : Python 3, PySpark

### 4.4 Configuration PySpark Kernel

Dans JupyterHub, créer un nouveau notebook et vérifier :

```python
# Vérifier Spark
import pyspark
print(f"PySpark version: {pyspark.__version__}")

# Vérifier TensorFlow
import tensorflow as tf
print(f"TensorFlow version: {tf.__version__}")

# Vérifier accès S3
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("P9-Test").getOrCreate()
df = spark.read.format("image").load("s3://fruits-classification-p9-maxime/dataset/Training/Apple*/")
print(f"Images chargées: {df.count()}")
```

**Résultats attendus :**
- PySpark : 3.4.x
- TensorFlow : 2.13.0
- Accès S3 : OK (images chargées)

---

## Phase 5 : Exécution du Notebook (2 heures)

### 5.1 Upload du Notebook

**Dans JupyterHub :**
1. **Upload** (bouton haut à droite)
2. Sélectionner : `P8_Notebook_Linux_EMR_PySpark_V1.0.ipynb`
3. **Upload** → Notebook apparaît dans la liste

### 5.2 Configuration des Chemins S3

**Ouvrir le notebook et modifier les chemins :**

```python
# Remplacer les chemins locaux par S3
BUCKET_NAME = "fruits-classification-p9-maxime"
DATASET_PATH = f"s3://{BUCKET_NAME}/dataset/Training/"
OUTPUT_PATH = f"s3://{BUCKET_NAME}/results/pca_output/"

# Exemple de lecture
df_images = spark.read.format("image").load(DATASET_PATH)
```

### 5.3 Exécution du Pipeline

**Ordre d'exécution (cellules importantes) :**

1. **Cellule 1 : Imports**
   - Vérifier tous les imports (gzip, pickle, PySpark ML)

2. **Cellule 2 : Configuration Spark**
   - Ajuster mémoire si nécessaire :
     ```python
     spark.conf.set("spark.driver.memory", "4g")
     spark.conf.set("spark.executor.memory", "2g")
     ```

3. **Cellule 3 : Chargement Dataset**
   - Charger depuis S3
   - Vérifier nombre d'images

4. **Cellule 4 : Preprocessing**
   - Normalisation images

5. **Cellule 5 : Feature Extraction avec Broadcast**
   - Broadcast optimisé des poids
   - Extraction features MobileNetV2

6. **Cellule 6 : PCA PySpark**
   - Réduction de dimension (1280 → 256)
   - Affichage variance expliquée

7. **Cellule 7 : Sauvegarde S3**
   - Écriture résultats format Parquet
   - Vérification écriture réussie

**Temps d'exécution estimé :** 30-60 minutes (selon taille dataset)

### 5.4 Capture Screenshots

**Pendant l'exécution, capturer :**
1. **Console AWS EMR** : Cluster en cours
2. **JupyterHub** : Notebook en exécution
3. **Cellule PCA** : Variance expliquée affichée
4. **Console S3** : Résultats PCA dans `results/pca_output/`

**Outils capture :**
- macOS : Cmd+Shift+4
- Windows : Snipping Tool
- Linux : Screenshot tool

---

## Phase 6 : Validation et Terminaison (1 heure)

### 6.1 Validation des Résultats

**Vérifier sur S3 :**

```bash
# Lister les fichiers de résultats
aws s3 ls s3://fruits-classification-p9-maxime/results/pca_output/ --recursive

# Télécharger un échantillon pour validation
aws s3 cp s3://fruits-classification-p9-maxime/results/pca_output/part-00000.parquet \
  ./local_results/sample.parquet

# Lire avec pandas (vérification locale)
import pandas as pd
df = pd.read_parquet('./local_results/sample.parquet')
print(df.head())
print(f"Colonnes: {df.columns.tolist()}")
print(f"Shape: {df.shape}")
```

**Critères de validation :**
- [ ] Fichiers Parquet créés dans S3
- [ ] Colonnes : path, label, features_pca
- [ ] Features PCA : 256 dimensions
- [ ] Variance expliquée ≥ 90%
- [ ] Nombre d'échantillons cohérent

### 6.2 Vérification des Coûts

**AWS Cost Explorer :**
1. Console → AWS Cost Management → Cost Explorer
2. Filters :
   - Service : EMR, S3
   - Date range : Today
3. Vérifier coûts cumulés < 10€

**Facturation prévue :**
- EMR (3h) : ~1.11€
- S3 storage (20GB) : ~0.46€
- Transferts S3 : ~0.12€
- **Total estimé : ~1.69€**

### 6.3 Terminaison du Cluster EMR

**IMPORTANT : NE PAS OUBLIER CETTE ÉTAPE**

**EMR Console → Clusters → [Votre cluster]**

1. **Terminate** (bouton rouge)
2. **Confirm termination**
3. **Attendre** : Status → "Terminating" → "Terminated"

**Durée terminaison :** 5-10 minutes

**Vérifications finales :**
- [ ] Cluster status : "Terminated"
- [ ] Aucun autre cluster en cours
- [ ] Coûts finaux vérifiés
- [ ] Résultats sauvegardés sur S3

### 6.4 Nettoyage (Optionnel, après soutenance)

**Après la soutenance, pour économiser :**

```bash
# Supprimer le bucket S3 (ATTENTION : supprime toutes les données)
aws s3 rb s3://fruits-classification-p9-maxime --force

# Ou garder seulement les résultats finaux
aws s3 rm s3://fruits-classification-p9-maxime/dataset/ --recursive
# Garder results/ pour référence
```

---

## Troubleshooting

### Problème : Cluster ne démarre pas

**Cause possible :** Capacité Spot insuffisante

**Solution :**
1. Retenter avec instances On-Demand (plus cher)
2. Ou changer type d'instance (m5.xlarge au lieu de m6g.xlarge)

### Problème : Connexion JupyterHub échoue

**Cause possible :** Security group mal configuré

**Solution :**
1. Vérifier security group Master
2. Ajouter règle inbound : Port 9443, Source = My IP
3. Vérifier DNS Master correct

### Problème : Accès S3 refusé depuis EMR

**Cause possible :** Permissions IAM insuffisantes

**Solution :**
1. Vérifier rôle EMR_EC2_DefaultRole_P9
2. Ajouter policy `AmazonS3FullAccess`
3. Redémarrer cluster si nécessaire

### Problème : Dépassement coûts

**Cause possible :** Cluster non terminé, instances trop grosses

**Solution immédiate :**
1. **Terminer IMMÉDIATEMENT** le cluster EMR
2. Vérifier aucun autre service en cours
3. Configurer alertes CloudWatch si pas fait

---

## Checklist Complète

### Avant de Commencer
- [ ] Compte AWS créé et configuré
- [ ] Région eu-west-1 sélectionnée
- [ ] Budget et alertes configurés
- [ ] Dataset téléchargé localement
- [ ] Notebook modifié (broadcast + PCA)

### Phase S3
- [ ] Bucket S3 créé (eu-west-1)
- [ ] Structure de dossiers créée
- [ ] Dataset uploadé (~87k images)
- [ ] Permissions vérifiées

### Phase EMR
- [ ] Rôles IAM créés (EMR + EC2)
- [ ] Cluster EMR créé (Spark + JupyterHub)
- [ ] Instances Spot configurées
- [ ] Security groups configurés
- [ ] Auto-terminaison activée
- [ ] Cluster démarré (status : Waiting)

### Phase Exécution
- [ ] JupyterHub accessible
- [ ] Notebook uploadé
- [ ] Chemins S3 configurés
- [ ] Pipeline exécuté avec succès
- [ ] Screenshots capturés

### Phase Validation
- [ ] Résultats PCA sur S3
- [ ] Variance ≥ 90% validée
- [ ] Coûts vérifiés (< 10€)
- [ ] Cluster terminé
- [ ] Rapport final rédigé

---

## Ressources Complémentaires

### Documentation AWS
- [EMR Getting Started](https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-gs.html)
- [S3 User Guide](https://docs.aws.amazon.com/s3/index.html)
- [EMR Pricing](https://aws.amazon.com/emr/pricing/)

### Commandes AWS CLI Utiles

```bash
# Lister clusters EMR
aws emr list-clusters --region eu-west-1

# Décrire cluster
aws emr describe-cluster --cluster-id j-XXXXXXXXXXXXX --region eu-west-1

# Terminer cluster
aws emr terminate-clusters --cluster-ids j-XXXXXXXXXXXXX --region eu-west-1

# Vérifier coûts
aws ce get-cost-and-usage \
  --time-period Start=2024-09-01,End=2024-09-30 \
  --granularity MONTHLY \
  --metrics BlendedCost \
  --region eu-west-1
```

---

**Version :** 1.0
**Dernière mise à jour :** 30 septembre 2024
**Auteur :** Guide P9 Fruits Classification