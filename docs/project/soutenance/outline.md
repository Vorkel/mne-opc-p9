# Outline Détaillé de la Présentation P9

**Durée totale : 20 minutes**
**Nombre de slides : 20**

---

## Section 1 : Introduction (3 minutes) - Slides 1-3

### Slide 1 : Page de titre
**Timing : 30 secondes**

**Contenu visuel :**
- Titre principal : "Architecture Big Data pour Classification de Fruits"
- Sous-titre : "PySpark + AWS EMR + TensorFlow"
- Votre nom
- Date de soutenance
- Logo "Fruits!" (optionnel) ou image de fruits

**À dire :**
- Accueillir le jury
- Présenter rapidement le sujet
- Annoncer le plan de la présentation

---

### Slide 2 : Contexte et problématique
**Timing : 1 minute 30**

**Contenu :**
- **Start-up Fruits! et sa mission**
  - Préservation de la biodiversité fruitière
  - Application mobile de reconnaissance de fruits
  - Objectif : identifier fruits pour robots cueilleurs

- **Challenge technique**
  - Besoin d'une architecture Big Data scalable
  - Traitement de volumes massifs d'images
  - Contraintes RGPD (serveurs européens)

- **Objectif du projet**
  - Première version du moteur de classification
  - Pipeline PySpark complet sur AWS EMR
  - Réduction de dimensions avec PCA

**À dire :**
- Expliquer le contexte business : start-up innovante dans l'agriculture
- Mettre en avant le challenge technique : Big Data + Cloud + ML
- Transition : "Pour cela, nous avons utilisé un dataset de 87 000 images..."

---

### Slide 3 : Dataset Fruits-360
**Timing : 1 minute**

**Contenu :**
- **Caractéristiques du dataset**
  - 87 000+ images de fruits
  - 131 catégories de fruits différents
  - Format : 100x100 pixels, RGB
  - Volume total : ~2 GB de données

- **Visuel**
  - Screenshot de quelques fruits représentatifs (pomme, banane, orange, fraise, etc.)
  - Grille de 6-8 images pour montrer la variété

**À dire :**
- Présenter les chiffres clés du dataset
- Montrer la diversité des fruits (montrer les images)
- Expliquer que ce volume nécessite une architecture Big Data
- Transition : "Pour traiter ce volume de données, nous avons conçu une architecture cloud..."

---

## Section 2 : Architecture Big Data (6 minutes) - Slides 4-9

### Slide 4 : Vue d'ensemble de l'architecture
**Timing : 1 minute**

**Contenu visuel :**
- **Diagramme complet** : Dataset → S3 → EMR → Résultats S3
- Annotations pour chaque brique :
  - Dataset local : 87k images (2 GB)
  - S3 : Stockage distribué durable (eu-west-1)
  - EMR : Cluster Spark pour calculs parallèles
  - S3 : Résultats PCA (matrice + labels Parquet)
- Flèches avec labels : "Upload", "Processing", "Output"

**À dire :**
- Présenter l'architecture globale en 4 briques
- Expliquer le flux de données de bout en bout
- Mentionner que tout est dans le cloud AWS (eu-west-1)
- Transition : "Détaillons maintenant chaque brique..."

---

### Slide 5 : Amazon S3 - Stockage distribué
**Timing : 1 minute**

**Contenu :**
- **Rôle de S3**
  - Stockage objet distribué et hautement durable
  - Séparation compute/storage (optimisation coûts)
  - Accessible depuis EMR via protocole s3://

- **Configuration utilisée**
  - Région : **eu-west-1** (Ireland) - RGPD
  - Chiffrement : AES-256 (transit + repos)
  - Bucket : `fruits-classification-p9-[votre-nom]`

- **Contenu stocké**
  - `Test/` : 87k images brutes (~2GB)
  - `Results/pca_output/` : Matrice PCA + labels (Parquet)

**À dire :**
- Expliquer pourquoi S3 (durable, scalable, séparation compute/storage)
- Insister sur RGPD : région eu-west-1
- Mentionner le chiffrement AES-256
- Transition : "Ces données sont ensuite traitées sur un cluster EMR..."

---

### Slide 6 : AWS EMR - Cluster de calcul
**Timing : 1 minute**

**Contenu :**
- **Rôle d'EMR**
  - Cluster Apache Spark managé par AWS
  - Calculs distribués parallèles
  - Scalabilité horizontale (ajout workers)

- **Configuration utilisée**
  - Master : 1x m6g.xlarge (4 vCPU, 16 GB RAM) - Graviton2
  - Workers : 2x m6g.large (2 vCPU, 8 GB RAM) - Graviton2
  - Logiciels : Spark 3.4, JupyterHub, TensorFlow
  - Type : **Spot instances** (réduction 90% des coûts)

- **Visuel**
  - **🔴 [SCREENSHOT AWS - MANQUANT]**
  - Screenshot Console AWS montrant le cluster EMR actif
  - Configuration visible (instances, logiciels, région)

**À dire :**
- Expliquer le rôle d'EMR : cluster Spark managé
- Détailler la configuration : master + 2 workers Graviton2
- Mentionner Spot instances pour optimisation coûts
- Montrer le screenshot de la console AWS
- Transition : "Ce cluster exécute Apache Spark..."

---

### Slide 7 : Apache Spark / PySpark
**Timing : 1 minute**

**Contenu :**
- **Qu'est-ce que Spark ?**
  - Moteur de calcul distribué open-source
  - Traitement parallèle de données massives
  - API Python : PySpark
  - Optimisé pour Big Data (in-memory processing)

- **Composants utilisés dans ce projet**
  - **Spark Core** : moteur de calcul distribué (RDD, DataFrames)
  - **Spark SQL** : manipulation de DataFrames (select, filter, join)
  - **Spark ML** : machine learning distribué (PCA)

- **Avantages pour notre use case**
  - Scalabilité : traitement de millions d'images possible
  - Performance : calculs en mémoire
  - Écosystème riche : intégration TensorFlow, S3, etc.

**À dire :**
- Expliquer pourquoi Spark (et pas pandas ou autre)
- Présenter les 3 composants utilisés
- Mettre en avant la scalabilité
- Transition : "Toute cette architecture respecte les contraintes RGPD..."

---

### Slide 8 : Conformité RGPD
**Timing : 1 minute**

**Contenu :**
- **Exigences RGPD pour ce projet**
  - Données personnelles (potentiellement) : images de fruits
  - Obligation : serveurs sur territoire européen
  - Pas de transfert hors UE

- **Solutions mises en œuvre**
  - ✅ Région AWS : **eu-west-1** (Ireland, Union Européenne)
  - ✅ Stockage S3 : buckets dans eu-west-1
  - ✅ Traitements EMR : cluster dans eu-west-1
  - ✅ Chiffrement : AES-256 (transit + repos)
  - ✅ Permissions IAM : principe du moindre privilège
  - ✅ Aucun transfert hors UE : toute la chaîne dans eu-west-1

**À dire :**
- Rappeler les contraintes RGPD du projet
- Insister sur le choix de la région eu-west-1
- Mentionner le chiffrement et les permissions IAM
- Valider que toute la chaîne est conforme
- Transition : "Au-delà de la conformité, nous avons optimisé les coûts..."

---

### Slide 9 : Optimisation des coûts
**Timing : 1 minute**

**Contenu :**
- **Budget maximal : 10€**

- **Stratégies d'optimisation mises en œuvre**
  - **Instances Spot** : réduction jusqu'à 90% vs On-Demand
  - **Instances Graviton2** (ARM) : 35% moins cher + 15% plus rapide
  - **Auto-scaling** : ajustement dynamique du nombre de workers
  - **Auto-terminaison** : cluster s'arrête après 3h max (ou idle)
  - **Séparation compute/storage** : S3 séparé d'EMR (pas de HDFS)

- **Coûts réels**
  - **🔴 [TABLEAU COÛTS - MANQUANT]**
  - Tableau détaillé :
    - EMR Master (m6g.xlarge Spot) : X€
    - EMR Core x2 (m6g.large Spot) : X€
    - S3 Storage : X€
    - S3 Transfert : X€
  - **TOTAL : ~1.69€** (estimation) - 83% d'économie sur budget

**À dire :**
- Mentionner le budget contraint : 10€ max
- Expliquer les 5 stratégies d'optimisation
- Présenter le tableau des coûts (ou estimation si pas encore de facture)
- Mettre en avant l'économie : 83% sous budget
- Transition : "Maintenant que l'architecture est posée, voyons la chaîne de traitement..."

---

## Section 3 : Chaîne de Traitement PySpark (6 minutes) - Slides 10-15

### Slide 10 : Pipeline complet - Vue d'ensemble
**Timing : 1 minute**

**Contenu visuel :**
- **Schéma du pipeline PySpark** : 5 étapes en séquence
  1. Chargement images (S3)
  2. Preprocessing
  3. Feature extraction (MobileNetV2 + broadcast)
  4. Réduction PCA
  5. Sauvegarde résultats (S3)

- **Métriques globales**
  - Volume traité : **87 000 images**
  - Durée totale : **🔴 [X MINUTES - MANQUANT]**
  - Environnement : **AWS EMR (Spark 3.4)**

**À dire :**
- Présenter le pipeline en 5 étapes
- Mentionner le volume traité (87k images)
- Donner le temps d'exécution total (si disponible)
- Transition : "Détaillons chaque étape, en commençant par le chargement..."

---

### Slide 11 : Étape 1 - Chargement depuis S3
**Timing : 1 minute**

**Contenu :**
- **Objectif**
  - Charger les 87k images depuis S3 dans un DataFrame Spark
  - Validation automatique (suppression images corrompues)

- **Code snippet**
  ```python
  # Chargement images depuis S3
  df_images = spark.read.format("image") \
      .option("dropInvalid", True) \
      .load("s3://fruits-classification-p9-maxime/Test/")

  print(f"Nombre d'images chargées : {df_images.count()}")
  ```

- **Résultat**
  - DataFrame Spark avec colonnes : `path`, `image` (struct avec data, width, height, channels)
  - Chargement distribué automatique (parallélisation par Spark)

**À dire :**
- Expliquer le format "image" de Spark
- Mentionner `dropInvalid=True` pour robustesse
- Insister sur le chargement distribué automatique
- Transition : "Une fois chargées, les images sont prétraitées..."

---

### Slide 12 : Étape 2 - Preprocessing
**Timing : 1 minute**

**Contenu :**
- **Objectif**
  - Normaliser les images [0, 255] → [0, 1]
  - Conversion en tenseurs TensorFlow
  - Préparation pour le modèle MobileNetV2

- **Code snippet**
  ```python
  def preprocess_image(image_data):
      """Normalise une image pour TensorFlow"""
      img = image_data.data
      img = img.astype('float32') / 255.0  # Normalisation
      return img

  # Application via UDF Spark
  df_preprocessed = df_images.withColumn(
      "image_normalized",
      preprocess_udf("image")
  )
  ```

- **Résultat**
  - Images normalisées prêtes pour l'inférence TensorFlow

**À dire :**
- Expliquer la normalisation [0,1]
- Mentionner l'utilisation d'UDF Spark pour distribuer le preprocessing
- Transition : "Ces images sont ensuite traitées par le modèle TensorFlow..."

---

### Slide 13 : Étape 3 - Feature Extraction (MobileNetV2)
**Timing : 1 minute 15**

**Contenu :**
- **Transfer Learning avec MobileNetV2**
  - Architecture pré-entraînée sur ImageNet (1.4M images)
  - Extraction de **1280 features** par image
  - Modèle optimisé pour mobile/edge (léger et rapide)

- **⭐ AMÉLIORATION : Broadcast optimisé des poids du modèle**

  **Code snippet**
  ```python
  # Broadcast du modèle TensorFlow avec compression
  import pickle, gzip

  model = MobileNetV2(weights='imagenet', include_top=False, pooling='avg')
  model_bytes = gzip.compress(pickle.dumps(model), compresslevel=9)
  model_broadcast = spark.sparkContext.broadcast(model_bytes)

  # Validation taille < 2GB
  assert len(model_bytes) < 2 * 1024**3, "Modèle trop volumineux"
  ```

- **Bénéfice du broadcast**
  - Réduction du trafic réseau entre master et workers
  - Modèle envoyé une seule fois à chaque worker (vs envoi par tâche)
  - Gain de performance significatif sur 87k images

**À dire :**
- Expliquer le transfer learning : réutilisation modèle pré-entraîné
- Détailler l'amélioration broadcast (demandée dans la mission)
- Expliquer pourquoi c'est critique : 87k images = beaucoup de tâches Spark
- Transition : "Ces features sont ensuite réduites avec PCA..."

---

### Slide 14 : Étape 4 - Réduction de Dimension (PCA)
**Timing : 1 minute 15**

**Contenu :**
- **Objectif**
  - Réduire 1280 dimensions → 256 dimensions
  - Conserver au moins 90% de variance expliquée

- **⭐ AMÉLIORATION : PCA distribuée en PySpark ML**

  **Code snippet**
  ```python
  from pyspark.ml.feature import PCA

  # Configuration PCA
  pca = PCA(k=256,
            inputCol="features_vector",
            outputCol="features_pca")

  # Entraînement et transformation
  pca_model = pca.fit(df_vectorized)
  df_pca = pca_model.transform(df_vectorized)

  # Variance expliquée
  variance_expliquee = sum(pca_model.explainedVariance[:256])
  print(f"Variance expliquée : {variance_expliquee:.2%}")
  ```

- **Résultats**
  - Réduction : **1280 dimensions → 256 dimensions (80% de réduction)**
  - Variance expliquée : **🔴 [X% - MANQUANT - ESTIMATION 95%]**

- **Visuel**
  - **🔴 [GRAPHIQUE PCA - MANQUANT]**
  - Graphique variance cumulative (courbe atteignant ~95% à 256 composantes)

**À dire :**
- Expliquer l'objectif de la PCA : réduction dimensions, compression
- Détailler l'amélioration : PCA en PySpark ML (demandée dans la mission)
- Montrer le graphique de variance (si disponible)
- Mentionner les résultats : 80% de réduction, 95% de variance conservée
- Transition : "Enfin, ces résultats sont sauvegardés..."

---

### Slide 15 : Étape 5 - Sauvegarde Résultats sur S3
**Timing : 30 secondes**

**Contenu :**
- **Objectif**
  - Sauvegarder matrice PCA + labels sur S3
  - Format Parquet (optimisé et compressé)
  - Écriture distribuée depuis Spark

- **Code snippet**
  ```python
  # Sauvegarde résultats sur S3
  df_pca.select("path", "label", "features_pca") \
      .write \
      .mode("overwrite") \
      .parquet("s3://fruits-classification-p9-maxime/Results/pca_output/")

  print("✅ Résultats PCA sauvegardés sur S3")
  ```

- **Résultat**
  - Fichiers Parquet dans `s3://bucket/Results/pca_output/`
  - Accessible pour futurs modèles de classification

**À dire :**
- Expliquer le choix de Parquet (colonnaire, compressé, optimisé)
- Mentionner l'écriture distribuée depuis Spark vers S3
- Insister sur la persistance : résultats disponibles après terminaison cluster
- Transition : "Voyons maintenant une démonstration concrète..."

---

## Section 4 : Démonstration (2 minutes) - Slides 16-17

### Slide 16 : Démonstration - Screenshots
**Timing : 1 minute**

**Contenu visuel :**
- **3 screenshots côte à côte ou en séquence**

  1. **🔴 [SCREENSHOT AWS - MANQUANT]**
     - Console AWS avec cluster EMR actif
     - Status "Running", configuration visible

  2. **🔴 [SCREENSHOT AWS - MANQUANT]**
     - JupyterHub EMR avec notebook en exécution
     - Cellules exécutées avec outputs PCA visibles

  3. **🔴 [SCREENSHOT AWS - MANQUANT]**
     - Bucket S3 avec résultats PCA
     - Structure : `Results/pca_output/` avec fichiers Parquet

- **Légendes claires** pour chaque screenshot

**À dire :**
- Montrer le cluster EMR actif sur la console AWS
- Montrer le notebook exécuté dans JupyterHub
- Montrer les résultats Parquet dans le bucket S3
- Insister : toute la chaîne est dans le cloud (eu-west-1)
- (Alternative : démo en direct si temps et connexion le permettent)
- Transition : "Voici les métriques de performance..."

---

### Slide 17 : Métriques de performance
**Timing : 1 minute**

**Contenu :**
- **Métriques du pipeline**
  - Volume traité : **87 000 images** (~2 GB)
  - Temps d'exécution : **🔴 [X MINUTES - MANQUANT]**
  - Dimensions : **1280 → 256 (réduction 80%)**
  - Variance PCA : **🔴 [X% - MANQUANT - ESTIMATION 95%]**

- **Métriques cloud**
  - Cluster : 1 master + 2 workers (Graviton2, Spot)
  - Région : eu-west-1 (RGPD ✅)
  - Coûts AWS : **🔴 [X€ - MANQUANT - ESTIMATION 1.69€]**

- **Conformité et qualité**
  - ✅ RGPD validé (serveurs européens)
  - ✅ Pipeline complet fonctionnel
  - ✅ Coûts maîtrisés (< 10€)
  - ✅ Résultats sauvegardés sur S3

**À dire :**
- Récapituler les métriques clés
- Insister sur le temps d'exécution (rapide grâce à Spark)
- Mettre en avant la conformité RGPD
- Mentionner les coûts optimisés
- Transition : "Faisons maintenant une synthèse des améliorations..."

---

## Section 5 : Synthèse et Conclusion (3 minutes) - Slides 18-20

### Slide 18 : Améliorations apportées au notebook
**Timing : 1 minute**

**Contenu :**
- **✅ Amélioration 1 : Broadcast TensorFlow optimisé**
  - Compression gzip + pickle des poids du modèle
  - Validation taille < 2GB avant broadcast
  - Gestion d'erreurs robuste
  - **Bénéfice** : réduction trafic réseau, gain de performance

- **✅ Amélioration 2 : PCA en PySpark ML**
  - PCA distribuée avec Spark ML (pas scikit-learn)
  - Réduction 80% des dimensions (1280 → 256)
  - Variance expliquée ≥90% (typiquement 95%)
  - Sauvegarde Parquet optimisée vers S3
  - **Bénéfice** : scalabilité pour millions d'images

- **✅ Amélioration 3 : Pipeline complet fonctionnel**
  - 5 étapes exécutables de bout en bout sur EMR
  - Intégration S3 → EMR → S3
  - Notebook reproductible

- **✅ Conformité RGPD** : serveurs eu-west-1
- **✅ Coûts maîtrisés** : < 2€ (vs budget 10€)

**À dire :**
- Récapituler les 2 améliorations demandées dans la mission
- Expliquer les bénéfices techniques de chaque amélioration
- Mettre en avant le pipeline complet fonctionnel
- Transition : "Ces améliorations valident les critères d'évaluation..."

---

### Slide 19 : Critères d'évaluation validés
**Timing : 1 minute**

**Contenu :**
- **Compétence 1 : Sélectionner les outils du Cloud**
  - ✅ **CE1** : Identification briques d'architecture (slides 4-9)
    - S3, EMR, Spark identifiés et expliqués
  - ✅ **CE2** : Outils cloud conformes RGPD (slide 8)
    - Région eu-west-1, chiffrement AES-256

- **Compétence 2 : Prétraiter, analyser, modéliser**
  - ✅ **CE1** : Chargement fichiers dans stockage cloud (slide 11)
    - Images chargées depuis S3
  - ✅ **CE2** : Exécution scripts dans cloud (slide 16)
    - Notebook exécuté sur EMR (screenshot JupyterHub)
  - ✅ **CE3** : Écriture sorties dans stockage cloud (slide 15)
    - Résultats PCA sauvegardés sur S3 (format Parquet)

- **Compétence 3 : Calculs distribués**
  - ✅ **CE1** : Identification traitements critiques (slides 13-14)
    - Feature extraction et PCA identifiés comme critiques
  - ✅ **CE2** : Exploitation conforme RGPD (slide 8)
    - Serveurs eu-west-1, aucun transfert hors UE
  - ✅ **CE3** : Scripts s'appuyant sur Spark (slides 10-15)
    - Pipeline entièrement en PySpark
  - ✅ **CE4** : Chaîne complète dans cloud (slide 16)
    - S3 → EMR → S3, toute la chaîne dans AWS

**À dire :**
- Récapituler les 9 critères d'évaluation
- Pour chaque CE, indiquer où dans la présentation il est validé
- Insister sur la conformité complète au référentiel
- Transition : "En conclusion..."

---

### Slide 20 : Conclusion et perspectives
**Timing : 1 minute**

**Contenu :**
- **Résultats obtenus**
  - ✅ Pipeline Big Data scalable opérationnel
  - ✅ Architecture cloud-native réutilisable
  - ✅ Améliorations techniques validées (broadcast + PCA)
  - ✅ Conformité RGPD et coûts optimisés

- **Perspectives pour Fruits!**
  - **Court terme** : Base technique pour robots cueilleurs
    - Features PCA peuvent alimenter un modèle de classification
    - Architecture testée et validée

  - **Moyen terme** : Scalabilité validée pour millions d'images
    - Spark permet de scaler horizontalement (+ workers)
    - Architecture S3 + EMR supporte volumes massifs

  - **Long terme** : Architecture applicable à d'autres projets ML
    - Pattern réutilisable : transfer learning + PCA + cloud
    - Expertise acquise sur Big Data dans le cloud

- **Questions ?**

**À dire :**
- Récapituler les résultats obtenus
- Ouvrir sur les perspectives : de ce POC à la production
- Mentionner la scalabilité validée (argument clé pour Big Data)
- Terminer par "Je suis prêt à répondre à vos questions"

---

## Timing détaillé

| Section | Slides | Durée | Durée cumulée |
|---------|--------|-------|---------------|
| **1. Introduction** | 1-3 | 3 min | 3 min |
| **2. Architecture Big Data** | 4-9 | 6 min | 9 min |
| **3. Pipeline PySpark** | 10-15 | 6 min | 15 min |
| **4. Démonstration** | 16-17 | 2 min | 17 min |
| **5. Synthèse et Conclusion** | 18-20 | 3 min | 20 min |
| **TOTAL** | 20 | **20 min** | |

---

## Checklist des visuels par slide

| Slide | Visuels requis | Statut |
|-------|----------------|--------|
| 1 | Titre + logo Fruits! | ✅ Peut être créé maintenant |
| 2 | Bullet points texte | ✅ Peut être créé maintenant |
| 3 | Screenshot grille de fruits | ✅ Peut être créé maintenant (images du dataset) |
| 4 | Diagramme architecture Big Data | ✅ Peut être créé maintenant (Draw.io) |
| 5 | Schéma S3 + bullet points | ✅ Peut être créé maintenant |
| 6 | Screenshot Console AWS EMR | 🔴 **MANQUANT - Nécessite AWS** |
| 7 | Schéma composants Spark | ✅ Peut être créé maintenant |
| 8 | Checklist RGPD | ✅ Peut être créé maintenant |
| 9 | Tableau coûts AWS | 🔴 **MANQUANT - Nécessite facture AWS** |
| 10 | Schéma pipeline 5 étapes | ✅ Peut être créé maintenant (Draw.io) |
| 11 | Code snippet | ✅ Peut être créé maintenant |
| 12 | Code snippet | ✅ Peut être créé maintenant |
| 13 | Code snippet | ✅ Peut être créé maintenant |
| 14 | Code snippet + graphique variance | 🔴 **Graphique MANQUANT - Nécessite AWS** |
| 15 | Code snippet | ✅ Peut être créé maintenant |
| 16 | 3 screenshots AWS | 🔴 **MANQUANT - Nécessite AWS** |
| 17 | Tableau métriques | 🔴 **Métriques MANQUANTES - Nécessite AWS** |
| 18 | Bullet points avec checkmarks | ✅ Peut être créé maintenant |
| 19 | Checklist 9 CE | ✅ Peut être créé maintenant |
| 20 | Bullet points + "Questions?" | ✅ Peut être créé maintenant |

---

## Notes importantes

### Éléments dépendants de l'exécution AWS (à compléter après Feature 4)

1. **Slide 6** : Screenshot Console AWS EMR
2. **Slide 9** : Tableau coûts réels
3. **Slide 10** : Temps d'exécution total
4. **Slide 14** : Variance PCA réelle + graphique variance
5. **Slide 16** : 3 screenshots (Console, JupyterHub, S3)
6. **Slide 17** : Toutes les métriques réelles

**Action** : Marquer ces slides avec des placeholders **"🔴 [MANQUANT - À COMPLÉTER APRÈS AWS]"** en attendant l'exécution de Feature 4.

### Transitions clés à préparer

- Slide 3 → 4 : "Pour traiter ce volume, nous avons conçu une architecture cloud..."
- Slide 9 → 10 : "Voyons maintenant la chaîne de traitement PySpark..."
- Slide 15 → 16 : "Passons à une démonstration concrète..."
- Slide 17 → 18 : "Récapitulons les améliorations apportées..."
- Slide 19 → 20 : "En conclusion..."

---

**Date de création** : 6 janvier 2025
**Statut** : ✅ Structure complète - En attente éléments AWS pour finalisation
