# Instructions pour Création des Diagrammes

**Objectif :** Créer 2 diagrammes professionnels pour la présentation

**Outil recommandé :** Draw.io (gratuit, https://app.diagrams.net)

**Durée estimée :** 1 heure (30 min par diagramme)

---

## 📐 Diagramme 1 : Architecture Big Data Complète

**Utilisé dans :** Slide 4
**Format de sortie :** PNG, 1920x1080px, haute qualité

### Objectif

Montrer le flux complet de données : Dataset Local → S3 → EMR → S3 Résultats

### Éléments du diagramme

#### 1. Dataset Local (gauche)

**Forme :** Rectangle arrondi, couleur jaune clair (#FEF3C7)
**Contenu :**
```
Dataset Local
Fruits-360
```
**Annotations en dessous :**
- 87 000 images
- ~2 GB
- 131 catégories

**Icône :** Ordinateur ou dossier

---

#### 2. Amazon S3 - Stockage Brut (gauche-centre)

**Forme :** Rectangle arrondi, couleur bleu clair (#DBEAFE)
**Contenu :**
```
Amazon S3
Stockage Distribué
```
**Annotations en dessous :**
- Région: eu-west-1
- Bucket: fruits-classification-p9-maxime
- Test/

**Icône :** Logo AWS S3 (ou icône bucket)

---

#### 3. AWS EMR - Cluster Spark (centre)

**Forme :** Rectangle plus grand, couleur orange clair (#FED7AA)
**Contenu :**
```
AWS EMR
Cluster Apache Spark
```
**Annotations en dessous :**
- Master: m6g.xlarge
- Workers: 2x m6g.large
- Spark 3.4 + TensorFlow

**Sous-éléments (optionnel, à l'intérieur du rectangle EMR) :**
- Petit rectangle "Master" en haut
- Deux petits rectangles "Worker 1" et "Worker 2" en bas

**Icône :** Logo AWS EMR ou Apache Spark

---

#### 4. Amazon S3 - Résultats (droite-centre)

**Forme :** Rectangle arrondi, couleur vert clair (#D1FAE5)
**Contenu :**
```
Amazon S3
Résultats PCA
```
**Annotations en dessous :**
- Format: Parquet
- Results/pca_output/
- Matrice + labels

**Icône :** Logo AWS S3 (ou icône fichier)

---

#### 5. Flèches et flux

**Flèche 1 : Dataset Local → S3 Brut**
- Type : Grosse flèche pleine, couleur bleue
- Label au-dessus : "Upload (aws s3 sync)"
- Label en dessous : "2 GB"

**Flèche 2 : S3 Brut → EMR**
- Type : Grosse flèche pleine, couleur orange
- Label au-dessus : "Chargement (spark.read)"
- Label en dessous : "s3://bucket/Test/"

**Flèche 3 : EMR → S3 Résultats**
- Type : Grosse flèche pleine, couleur verte
- Label au-dessus : "Sauvegarde (.write.parquet)"
- Label en dessous : "s3://bucket/Results/"

---

#### 6. Annotations générales

**En haut du diagramme :**
```
Architecture Big Data - Fruits Classification
```
(titre centré, police 20pt, gras)

**En bas du diagramme :**
```
Toute la chaîne dans eu-west-1 (RGPD ✓)
```
(sous-titre centré, police 14pt, italique)

**Cadre "RGPD" :**
- Rectangle pointillé autour de S3 + EMR + S3
- Label : "Zone eu-west-1 (Union Européenne)"

---

### Instructions Draw.io étape par étape

1. **Ouvrir Draw.io**
   - Aller sur https://app.diagrams.net
   - Créer nouveau diagramme vierge
   - Taille : Custom, 1920x1080px

2. **Créer Dataset Local**
   - Formes → Rectangle arrondi
   - Couleur fond : jaune clair (#FEF3C7)
   - Bordure : 2pt, noir
   - Ajouter texte "Dataset Local\nFruits-360"
   - Ajouter icône ordinateur (bibliothèque Icons)
   - Ajouter annotations en dessous (zone texte)

3. **Créer S3 Brut**
   - Dupliquer rectangle (Ctrl+D)
   - Déplacer à droite du Dataset
   - Changer couleur : bleu clair (#DBEAFE)
   - Modifier texte : "Amazon S3\nStockage Distribué"
   - Ajouter icône S3
   - Annotations en dessous

4. **Créer EMR**
   - Rectangle plus grand au centre
   - Couleur : orange clair (#FED7AA)
   - Texte : "AWS EMR\nCluster Apache Spark"
   - Optionnel : ajouter 3 petits rectangles à l'intérieur (Master + 2 Workers)
   - Annotations en dessous

5. **Créer S3 Résultats**
   - Dupliquer S3 Brut
   - Déplacer à droite d'EMR
   - Changer couleur : vert clair (#D1FAE5)
   - Modifier texte : "Amazon S3\nRésultats PCA"
   - Annotations en dessous

6. **Ajouter flèches**
   - Formes → Flèches → Block Arrow
   - Relier Dataset → S3 : flèche bleue, label "Upload"
   - Relier S3 → EMR : flèche orange, label "Chargement"
   - Relier EMR → S3 : flèche verte, label "Sauvegarde"

7. **Ajouter cadre RGPD**
   - Formes → Rectangle
   - Style bordure : pointillé (dashed)
   - Pas de fond (transparent)
   - Entourer S3 + EMR + S3
   - Label : "Zone eu-west-1"

8. **Ajouter titres**
   - Zone texte en haut : "Architecture Big Data - Fruits Classification"
   - Zone texte en bas : "Toute la chaîne dans eu-west-1 (RGPD ✓)"

9. **Ajustements finaux**
   - Aligner éléments horizontalement (Arrange → Align)
   - Espacer équitablement
   - Vérifier lisibilité

10. **Export**
    - File → Export as → PNG
    - Résolution : 300 DPI
    - Transparent background : Non
    - Sauvegarder : `docs/project/soutenance/visuels/diagrammes/architecture-big-data.png`

---

## 🔄 Diagramme 2 : Pipeline PySpark 5 Étapes

**Utilisé dans :** Slide 10
**Format de sortie :** PNG, 1920x600px (horizontal), haute qualité

### Objectif

Montrer les 5 étapes séquentielles du pipeline PySpark

### Éléments du diagramme

#### Étape 1 : Chargement S3

**Forme :** Rectangle arrondi, couleur bleu clair (#DBEAFE)
**Contenu :**
```
1. Chargement
```
**Icône :** S3 ou téléchargement
**Annotations en dessous :**
- spark.read.format("image")
- S3 → DataFrame

---

#### Étape 2 : Preprocessing

**Forme :** Rectangle arrondi, couleur violet clair (#E9D5FF)
**Contenu :**
```
2. Preprocessing
```
**Icône :** Engrenage ou filtre
**Annotations en dessous :**
- Normalisation [0,1]
- Conversion TensorFlow

---

#### Étape 3 : Feature Extraction

**Forme :** Rectangle arrondi, couleur orange clair (#FED7AA)
**Contenu :**
```
3. Feature Extraction
```
**Icône :** Réseau de neurones ou cerveau
**Annotations en dessous :**
- MobileNetV2 (broadcast)
- 1280 features/image

---

#### Étape 4 : Réduction PCA

**Forme :** Rectangle arrondi, couleur rose clair (#FBCFE8)
**Contenu :**
```
4. Réduction PCA
```
**Icône :** Graphique ou compression
**Annotations en dessous :**
- PySpark ML
- 1280 → 256 dims

---

#### Étape 5 : Sauvegarde S3

**Forme :** Rectangle arrondi, couleur vert clair (#D1FAE5)
**Contenu :**
```
5. Sauvegarde
```
**Icône :** S3 ou disque dur
**Annotations en dessous :**
- .write.parquet()
- S3 Résultats

---

### Flèches entre les étapes

**Entre chaque étape :**
- Grosse flèche simple horizontale
- Couleur : gris foncé (#374151)
- Largeur : 3pt

---

### Annotations générales

**En haut du diagramme :**
```
Pipeline PySpark - 5 Étapes
```
(titre centré, police 18pt, gras)

**En bas du diagramme (global) :**
```
Volume traité : 87 000 images | Environnement : AWS EMR (Spark 3.4)
```
(sous-titre centré, police 12pt)

---

### Instructions Draw.io étape par étape

1. **Ouvrir Draw.io**
   - Créer nouveau diagramme
   - Taille : Custom, 1920x600px (horizontal)

2. **Créer Étape 1**
   - Rectangle arrondi, bleu clair
   - Texte : "1. Chargement"
   - Icône S3 en haut du rectangle
   - Zone texte en dessous : annotations

3. **Dupliquer pour Étapes 2-5**
   - Ctrl+D pour dupliquer
   - Placer horizontalement à droite
   - Changer couleur selon étape
   - Modifier texte et annotations

4. **Ajouter flèches**
   - Flèches simples entre chaque étape
   - Couleur gris foncé, 3pt
   - Aligner au centre des rectangles

5. **Ajouter titre et sous-titre**
   - Zone texte en haut : "Pipeline PySpark - 5 Étapes"
   - Zone texte en bas : métriques globales

6. **Alignement**
   - Sélectionner toutes les étapes
   - Arrange → Align → Center Vertically
   - Arrange → Distribute → Horizontally

7. **Export**
   - File → Export as → PNG
   - Résolution : 300 DPI
   - Sauvegarder : `docs/project/soutenance/visuels/diagrammes/pipeline-pyspark.png`

---

## 🎨 Conseils de Design

### Palette de couleurs utilisée

| Élément | Couleur | Code Hex |
|---------|---------|----------|
| Dataset / Fichiers | Jaune clair | #FEF3C7 |
| S3 Stockage | Bleu clair | #DBEAFE |
| EMR / Spark | Orange clair | #FED7AA |
| Résultats | Vert clair | #D1FAE5 |
| Preprocessing | Violet clair | #E9D5FF |
| PCA | Rose clair | #FBCFE8 |
| Flèches | Gris foncé | #374151 |
| Texte | Noir | #000000 |

### Typographie

- **Titres principaux** : Arial Bold, 18-20pt
- **Noms éléments** : Arial Bold, 14-16pt
- **Annotations** : Arial Regular, 10-12pt

### Icônes

**Où trouver les icônes :**
- Draw.io : bibliothèque "Icons" intégrée
- AWS Architecture Icons : https://aws.amazon.com/architecture/icons/
- Flaticon : https://www.flaticon.com/ (gratuit avec attribution)

**Icônes recommandées :**
- S3 : bucket ou cloud storage
- EMR : cluster ou serveurs
- Spark : éclair ou logo Apache Spark
- MobileNetV2 : réseau de neurones ou cerveau
- PCA : graphique ou compression

---

## ✅ Checklist Finale

### Diagramme 1 : Architecture

- [ ] 4 éléments principaux créés (Dataset, S3, EMR, S3)
- [ ] 3 flèches avec labels
- [ ] Cadre RGPD pointillé
- [ ] Titre et sous-titre
- [ ] Annotations lisibles
- [ ] Icônes ajoutées
- [ ] Couleurs cohérentes
- [ ] Export PNG 300 DPI

### Diagramme 2 : Pipeline

- [ ] 5 étapes créées
- [ ] 4 flèches entre étapes
- [ ] Titre et sous-titre
- [ ] Annotations lisibles
- [ ] Icônes ajoutées
- [ ] Couleurs cohérentes
- [ ] Alignement horizontal
- [ ] Export PNG 300 DPI

---

## 🔄 Alternatives à Draw.io

Si vous préférez d'autres outils :

**Lucidchart** (en ligne, freemium)
- https://www.lucidchart.com
- Templates d'architecture cloud intégrés
- Export haute qualité

**PowerPoint SmartArt** (intégré Office)
- Utiliser SmartArt → Processus ou Cycles
- Personnaliser couleurs et texte
- Avantage : directement dans PowerPoint

**Figma** (en ligne, gratuit)
- https://www.figma.com
- Design professionnel
- Export PNG/SVG

**Canva** (en ligne, freemium)
- https://www.canva.com
- Templates infographies
- Facile à utiliser

---

**Temps total : 1 heure**
**Bonne création ! 🎨**
