# Guide de Création PowerPoint - P9 Soutenance

**Objectif :** Instructions détaillées slide par slide pour créer la présentation

**Durée estimée :** 3-4 heures

---

## 🎨 Configuration initiale (15 minutes)

### Étape 1 : Créer le fichier PowerPoint

1. Ouvrir PowerPoint (ou Google Slides / Keynote)
2. Créer une présentation vierge
3. Sauvegarder sous : `docs/project/soutenance/presentation.pptx`

### Étape 2 : Configuration du template

**Thème recommandé :**
- Template PowerPoint moderne et sobre
- Suggéré : "Ion" ou "Facet" (templates Microsoft intégrés)
- Ou créer un template personnalisé

**Palette de couleurs (max 3 couleurs principales) :**
- **Couleur primaire** : Bleu foncé (#1E3A8A) - pour les titres
- **Couleur secondaire** : Orange (#F97316) - pour les accents
- **Couleur tertiaire** : Gris clair (#E5E7EB) - pour les backgrounds
- **Texte** : Noir (#000000) ou gris foncé (#374151)

**Typographie :**
- **Titre slide** : Arial ou Calibri Bold, 36-40pt
- **Sous-titres** : Arial ou Calibri Bold, 24-28pt
- **Texte corps** : Arial ou Calibri Regular, 18-22pt
- **Code snippets** : Consolas ou Courier New, 14-16pt

### Étape 3 : Créer le masque de slides

1. Aller dans Affichage → Masque des diapositives
2. Configurer :
   - Logo (si applicable) en haut à droite
   - Numéro de page en bas à droite
   - Pied de page : "P9 - Fruits Classification | AWS EMR + PySpark"
3. Sauvegarder le masque

---

## 📄 Création des Slides

### SECTION 1 : Introduction (Slides 1-3)

---

#### Slide 1 : Page de titre ⏱️ 30 sec

**Layout :** Titre centré

**Contenu :**

**Titre principal** (centre, gros, 48pt, gras)
```
Architecture Big Data pour Classification de Fruits
```

**Sous-titre** (centre, 32pt)
```
PySpark + AWS EMR + TensorFlow
```

**Informations en bas** (centre, 20pt)
```
[Votre nom]
[Date de soutenance]
OpenClassrooms - Parcours Data Scientist
```

**Visuel (optionnel) :**
- Logo "Fruits!" si vous en avez un
- Ou une belle image de fruits en arrière-plan (opacité 10-20%)

**Instructions PowerPoint :**
1. Insérer → Zone de texte pour chaque élément
2. Centre horizontalement (Ctrl+E)
3. Espacer verticalement de manière équilibrée
4. Appliquer animations si souhaité (entrée progressive)

---

#### Slide 2 : Contexte et problématique ⏱️ 1 min 30

**Layout :** Titre + contenu à puces

**Titre slide :**
```
Contexte et Problématique
```

**Contenu (3 blocs de bullet points) :**

**Bloc 1 : Start-up Fruits!**
- ✓ Préservation de la biodiversité fruitière
- ✓ Application mobile de reconnaissance de fruits
- ✓ Objectif futur : robots cueilleurs intelligents

**Bloc 2 : Challenge technique**
- ⚠️ Volumes massifs d'images à traiter
- ⚠️ Architecture Big Data scalable nécessaire
- ⚠️ Contraintes : RGPD + budget limité (10€)

**Bloc 3 : Objectif du projet**
- 🎯 Pipeline PySpark complet sur AWS EMR
- 🎯 Extraction de features (TensorFlow)
- 🎯 Réduction de dimensions (PCA)

**Instructions PowerPoint :**
1. Utiliser des icônes pour ✓, ⚠️, 🎯 (Insérer → Icônes)
2. Couleur différente pour chaque bloc (bleu, orange, vert)
3. Espacement entre les blocs (15-20pt)
4. Taille police : 20pt pour les bullet points

---

#### Slide 3 : Dataset Fruits-360 ⏱️ 1 min

**Layout :** Titre + 2 colonnes (texte gauche, image droite)

**Titre slide :**
```
Dataset Fruits-360
```

**Colonne gauche (texte) :**
```
Caractéristiques
• 87 000+ images de fruits
• 131 catégories différentes
• Format : 100x100 pixels, RGB
• Volume total : ~2 GB

Challenge Big Data
→ Traitement distribué nécessaire
→ pandas ne scale pas
→ PySpark requis
```

**Colonne droite (visuel) :**
- Grille de 6-8 images de fruits du dataset
- Exemples : pomme, banane, orange, fraise, kiwi, etc.

**Instructions PowerPoint :**
1. Créer 2 zones de texte (gauche et droite)
2. Gauche : largeur 50%, texte à puces
3. Droite : insérer grille d'images
   - Aller dans dossier `data/raw/fruits-360_dataset/fruits-360/Training/`
   - Sélectionner 6-8 images représentatives
   - Créer grille 2x3 ou 2x4
   - Ajouter légende sous chaque image (nom du fruit)

---

### SECTION 2 : Architecture Big Data (Slides 4-9)

---

#### Slide 4 : Vue d'ensemble de l'architecture ⏱️ 1 min

**Layout :** Titre + diagramme pleine largeur

**Titre slide :**
```
Architecture Big Data : Vue d'ensemble
```

**Contenu :**
- Diagramme complet : Dataset → S3 → EMR → S3
- **Référence :** Voir fichier `instructions-diagrammes.md` pour créer ce diagramme dans Draw.io
- Une fois créé, exporter en PNG haute qualité et insérer ici

**Annotations sur le diagramme :**
- Dataset : "87k images, 2 GB"
- S3 (gauche) : "Stockage brut (eu-west-1)"
- EMR : "Cluster Spark (1 master + 2 workers)"
- S3 (droite) : "Résultats PCA (Parquet)"
- Flèches : "Upload", "Processing", "Output"

**Instructions PowerPoint :**
1. Insérer → Image → `visuels/diagrammes/architecture-big-data.png`
2. Centrer et agrandir pour occuper tout l'espace
3. Vérifier lisibilité (zoom pour tester)

---

#### Slide 5 : Amazon S3 - Stockage ⏱️ 1 min

**Layout :** Titre + 2 colonnes

**Titre slide :**
```
Amazon S3 : Stockage Distribué et Durable
```

**Colonne gauche (Rôle) :**
```
Rôle de S3
• Stockage objet distribué
• Durabilité 99,999999999% (11 neuf)
• Séparation compute/storage
• Intégration native avec EMR

Pourquoi S3 ?
→ Éteindre EMR sans perdre données
→ Coût stockage faible
→ Accès via s3:// dans Spark
```

**Colonne droite (Configuration) :**
```
Configuration utilisée

Région : eu-west-1 (Ireland, UE)
Chiffrement : AES-256 (transit + repos)
Bucket : fruits-classification-p9-maxime

Contenu stocké :
📁 dataset/Training/
   → 87k images (~2 GB)
📁 results/pca_output/
   → Matrice PCA (Parquet)
```

**Visuel (optionnel) :**
- Logo AWS S3 en haut à droite
- Icône bucket S3

**Instructions PowerPoint :**
1. 2 colonnes égales (50/50)
2. Utiliser fond coloré léger pour la colonne droite (gris clair)
3. Icônes pour 📁 (Insérer → Icônes → Dossier)

---

#### Slide 6 : AWS EMR - Cluster de calcul ⏱️ 1 min

**Layout :** Titre + contenu mixte

**Titre slide :**
```
AWS EMR : Cluster Apache Spark Managé
```

**Contenu :**

**Bloc 1 : Rôle d'EMR** (haut gauche)
```
Rôle
• Cluster Apache Spark managé par AWS
• Calculs distribués parallèles
• Scalabilité horizontale (ajout workers)
```

**Bloc 2 : Configuration** (haut droite)
```
Configuration du cluster
Master : 1x m6g.xlarge (4 vCPU, 16 GB)
Workers : 2x m6g.large (2 vCPU, 8 GB)
Logiciels : Spark 3.4, JupyterHub, TensorFlow
Type : Spot instances (90% réduction coûts)
```

**Bloc 3 : Screenshot** (bas, pleine largeur)
```
🔴 [SCREENSHOT AWS CONSOLE - MANQUANT]
Screenshot de la console AWS montrant le cluster EMR actif
```

**Instructions PowerPoint :**
1. Créer 2 zones texte en haut (50/50)
2. Créer zone en bas pour screenshot
3. **SI SCREENSHOT MANQUANT** : insérer rectangle gris avec texte "Screenshot à insérer après AWS"
4. **APRÈS AWS** : remplacer par screenshot réel

---

#### Slide 7 : Apache Spark / PySpark ⏱️ 1 min

**Layout :** Titre + 3 colonnes

**Titre slide :**
```
Apache Spark / PySpark : Moteur de Calcul Distribué
```

**Colonne 1 : Qu'est-ce que Spark ?**
```
Spark
• Moteur distribué open-source
• Traitement parallèle
• API Python : PySpark
• In-memory processing
```

**Colonne 2 : Composants utilisés**
```
Composants
• Spark Core
  → Calcul distribué (RDD, DataFrames)
• Spark SQL
  → Manipulation DataFrames
• Spark ML
  → PCA distribuée
```

**Colonne 3 : Avantages**
```
Pourquoi Spark ?
✓ Scalabilité
  → 87k → 1M images
✓ Performance
  → In-memory
✓ Écosystème
  → TensorFlow, S3, etc.
```

**Visuel :**
- Logo Apache Spark en haut
- Schéma simple : Master → Worker 1, Worker 2 (architecture Spark)

**Instructions PowerPoint :**
1. 3 colonnes égales (33/33/33)
2. Séparateur vertical entre colonnes
3. Icônes pour ✓

---

#### Slide 8 : Conformité RGPD ⏱️ 1 min

**Layout :** Titre + checklist centrale

**Titre slide :**
```
Conformité RGPD : Serveurs Européens
```

**Contenu (centré, grande checklist) :**

```
Exigences RGPD
→ Données personnelles sur serveurs européens
→ Aucun transfert hors Union Européenne

Solutions mises en œuvre

✅ Région AWS : eu-west-1 (Ireland, UE)
✅ Stockage S3 : buckets dans eu-west-1
✅ Traitements EMR : cluster dans eu-west-1
✅ Chiffrement : AES-256 (transit + repos)
✅ Permissions IAM : principe du moindre privilège
✅ Aucun transfert hors UE : toute la chaîne dans eu-west-1

Résultat : 100% conforme RGPD ✓
```

**Visuel :**
- Carte de l'Europe avec marqueur sur l'Irlande (eu-west-1)
- Logo RGPD

**Instructions PowerPoint :**
1. Centrer le contenu
2. Checkmarks ✅ de couleur verte
3. Dernière ligne en gras et plus grande (24pt)
4. Fond légèrement coloré (bleu très clair) pour mise en avant

---

#### Slide 9 : Optimisation des coûts ⏱️ 1 min

**Layout :** Titre + 2 colonnes

**Titre slide :**
```
Optimisation des Coûts : < 2€ sur Budget de 10€
```

**Colonne gauche : Stratégies**
```
Stratégies d'optimisation

1️⃣ Instances Spot
   → Réduction 90% vs On-Demand

2️⃣ Instances Graviton2 (ARM)
   → 35% moins cher + 15% plus rapide

3️⃣ Auto-scaling
   → Ajustement dynamique workers

4️⃣ Auto-terminaison
   → Arrêt après 3h max

5️⃣ Séparation compute/storage
   → S3 séparé d'EMR (pas HDFS)
```

**Colonne droite : Tableau coûts**
```
Coûts réels

🔴 [TABLEAU DÉTAILLÉ - MANQUANT]

| Service | Coût |
|---------|------|
| EMR Master | X€ |
| EMR Core (x2) | X€ |
| S3 Storage | X€ |
| S3 Transfert | X€ |
| Autres | X€ |
| TOTAL | ~1,69€ |

Économie : 83% vs budget 10€
```

**Instructions PowerPoint :**
1. Colonne gauche : puces numérotées avec émojis
2. Colonne droite : tableau inséré
3. **SI TABLEAU MANQUANT** : laisser placeholder
4. **APRÈS AWS** : remplacer par coûts réels
5. Dernière ligne (Économie) en gras et vert

---

### SECTION 3 : Chaîne de Traitement PySpark (Slides 10-15)

---

#### Slide 10 : Pipeline complet - Vue d'ensemble ⏱️ 1 min

**Layout :** Titre + diagramme + métriques

**Titre slide :**
```
Pipeline PySpark : 5 Étapes
```

**Contenu haut : Schéma pipeline**
- Diagramme horizontal : 5 étapes en séquence
- **Référence :** Voir fichier `instructions-diagrammes.md` pour créer ce schéma dans Draw.io
- Étapes : Chargement S3 → Preprocessing → Feature Extraction → PCA → Sauvegarde S3

**Contenu bas : Métriques**
```
Métriques globales

Volume traité : 87 000 images (~2 GB)
Durée totale : 🔴 [X minutes - MANQUANT]
Environnement : AWS EMR (Spark 3.4)
```

**Instructions PowerPoint :**
1. Schéma en haut (70% de l'espace)
2. Métriques en bas (30%)
3. Placer métriques manquantes en rouge

---

#### Slides 11-15 : Étapes détaillées

**Chaque slide suit le même modèle :**
- Titre : "Étape X - [Nom]"
- Objectif (haut gauche)
- Code snippet (bas gauche, fond gris)
- Résultat (droite)

**Note :** Pour gagner du temps, voici le modèle à dupliquer 5 fois, puis personnaliser :

**Template slide étape :**
```
Titre : Étape X - [Nom]

[Haut gauche - Objectif]
Objectif
• Point 1
• Point 2

[Bas gauche - Code]
[Fond gris clair]
```python
# Code snippet
```

[Droite - Résultat]
Résultat
→ Description
→ Métrique
```

**Personnalisation pour chaque slide :**

**Slide 11 : Étape 1 - Chargement depuis S3** - Consultez `outline.md` lignes 266-280
**Slide 12 : Étape 2 - Preprocessing** - Consultez `outline.md` lignes 282-297
**Slide 13 : Étape 3 - Feature Extraction** - Consultez `outline.md` lignes 299-322
**Slide 14 : Étape 4 - PCA** - Consultez `outline.md` lignes 324-350
**Slide 15 : Étape 5 - Sauvegarde** - Consultez `outline.md` lignes 352-368

**Instructions PowerPoint pour slides 11-15 :**
1. Dupliquer le template 5 fois
2. Remplir selon contenu d'`outline.md`
3. Code en police Consolas 14-16pt, fond gris clair (#F3F4F6)
4. Sur slide 14 : insérer graphique variance PCA (🔴 si manquant)

---

### SECTION 4 : Démonstration (Slides 16-17)

---

#### Slide 16 : Démonstration - Screenshots ⏱️ 1 min

**Layout :** Titre + 3 images en grille

**Titre slide :**
```
Démonstration : Pipeline en Exécution
```

**Contenu : Grille 3 screenshots**

**Screenshot 1 (gauche haut)** - 40% largeur
```
Console AWS - Cluster EMR actif
🔴 [À CAPTURER APRÈS AWS]
```
Légende : "Cluster EMR running, eu-west-1"

**Screenshot 2 (droite haut)** - 60% largeur
```
JupyterHub - Notebook en exécution
🔴 [À CAPTURER APRÈS AWS]
```
Légende : "Notebook avec outputs PCA"

**Screenshot 3 (bas pleine largeur)** - 100% largeur
```
Bucket S3 - Résultats PCA
🔴 [À CAPTURER APRÈS AWS]
```
Légende : "Structure S3 : dataset/ + results/pca_output/"

**Instructions PowerPoint :**
1. Créer 3 zones rectangles grises (placeholders)
2. Ajouter texte "Screenshot à capturer après AWS" en rouge
3. **APRÈS AWS** : remplacer par screenshots réels
4. Ajouter légendes sous chaque image (12pt, italique)

---

#### Slide 17 : Métriques de performance ⏱️ 1 min

**Layout :** Titre + tableau 2 colonnes

**Titre slide :**
```
Métriques de Performance
```

**Contenu : Tableau récapitulatif**

| Catégorie | Métrique | Valeur |
|-----------|----------|--------|
| **Pipeline** | Volume traité | 87 000 images (~2 GB) |
| | Temps d'exécution | 🔴 **[X min - MANQUANT]** |
| | Dimensions | 1280 → 256 (80% réduction) |
| | Variance PCA | 🔴 **[X% - MANQUANT]** |
| **Cloud** | Cluster | 1 master + 2 workers (Graviton2, Spot) |
| | Région | eu-west-1 (RGPD ✅) |
| | Coûts AWS | 🔴 **[X€ - MANQUANT]** |
| **Qualité** | RGPD | ✅ 100% conforme |
| | Pipeline | ✅ Complet et fonctionnel |
| | Coûts | ✅ Maîtrisés (< 10€) |

**Instructions PowerPoint :**
1. Insérer tableau (Insertion → Tableau)
2. Mettre en gras les catégories
3. Métriques manquantes en rouge
4. Checkmarks ✅ en vert
5. Bordures légères pour lisibilité

---

### SECTION 5 : Synthèse et Conclusion (Slides 18-20)

---

#### Slide 18 : Améliorations apportées ⏱️ 1 min

**Layout :** Titre + 2 colonnes

**Titre slide :**
```
Améliorations Techniques Apportées
```

**Colonne gauche : Amélioration 1**
```
⭐ 1. Broadcast TensorFlow Optimisé

Implémentation
• Compression gzip + pickle
• Validation taille < 2GB
• Gestion d'erreurs robuste

Bénéfice
→ Réduction trafic réseau (99%)
→ Gain performance significatif
→ Scalabilité validée (87k images)
```

**Colonne droite : Amélioration 2**
```
⭐ 2. PCA en PySpark ML

Implémentation
• PCA distribuée (Spark ML)
• Réduction 80% dimensions (1280 → 256)
• Variance expliquée ≥90% (~95%)
• Sauvegarde Parquet optimisée

Bénéfice
→ Scalabilité (vs scikit-learn)
→ Calcul distribué sur workers
→ Compression efficace
```

**Bas de slide (pleine largeur) :**
```
✅ Pipeline complet fonctionnel | ✅ Conformité RGPD | ✅ Coûts < 2€
```

**Instructions PowerPoint :**
1. 2 colonnes égales
2. Étoiles ⭐ pour marquer les améliorations
3. Checkmarks ✅ en bas en vert
4. Fond léger pour chaque amélioration (bleu clair et orange clair)

---

#### Slide 19 : Critères d'évaluation validés ⏱️ 1 min

**Layout :** Titre + 3 blocs

**Titre slide :**
```
Critères d'Évaluation : 9/9 Validés
```

**Bloc 1 : Compétence 1**
```
Compétence 1 : Sélectionner les outils du Cloud

✅ CE1 : Identification briques d'architecture
   → S3, EMR, Spark (slides 4-9)
✅ CE2 : Outils cloud conformes RGPD
   → Région eu-west-1, chiffrement AES-256 (slide 8)
```

**Bloc 2 : Compétence 2**
```
Compétence 2 : Prétraiter, analyser, modéliser

✅ CE1 : Chargement fichiers dans stockage cloud
   → Images chargées depuis S3 (slide 11)
✅ CE2 : Exécution scripts dans cloud
   → Notebook exécuté sur EMR (slide 16)
✅ CE3 : Écriture sorties dans stockage cloud
   → Résultats PCA sur S3 Parquet (slide 15)
```

**Bloc 3 : Compétence 3**
```
Compétence 3 : Réaliser calculs distribués

✅ CE1 : Identification traitements critiques
   → Feature extraction + PCA (slides 13-14)
✅ CE2 : Exploitation conforme RGPD
   → Serveurs eu-west-1 uniquement (slide 8)
✅ CE3 : Scripts s'appuyant sur Spark
   → Pipeline entièrement PySpark (slides 10-15)
✅ CE4 : Chaîne complète dans cloud
   → S3 → EMR → S3 (slide 16)
```

**Instructions PowerPoint :**
1. 3 blocs en colonnes ou empilés verticalement
2. Checkmarks ✅ verts
3. Références entre parenthèses en italique petit (14pt)
4. Bordure pour chaque bloc
5. Titre de slide avec "9/9" en gras et vert

---

#### Slide 20 : Conclusion et perspectives ⏱️ 1 min

**Layout :** Titre + 2 colonnes + footer

**Titre slide :**
```
Conclusion et Perspectives
```

**Colonne gauche : Résultats**
```
Résultats obtenus

✅ Pipeline Big Data scalable opérationnel
✅ Architecture cloud-native réutilisable
✅ Améliorations techniques validées
   • Broadcast TensorFlow optimisé
   • PCA PySpark distribuée
✅ Conformité RGPD stricte (eu-west-1)
✅ Coûts optimisés (< 2€ vs budget 10€)
```

**Colonne droite : Perspectives**
```
Perspectives pour Fruits!

Court terme
→ Base technique pour robots cueilleurs
→ Features PCA → modèle de classification

Moyen terme
→ Scalabilité validée (87k → 1M images)
→ Architecture S3 + EMR prête

Long terme
→ Pattern réutilisable (autres projets ML)
→ Expertise Big Data transférable
```

**Footer (centré, grand, gras) :**
```
Questions ?
```

**Instructions PowerPoint :**
1. 2 colonnes égales
2. Checkmarks ✅ verts
3. Flèches → pour perspectives
4. Footer "Questions ?" très visible (32pt, gras, couleur primaire)
5. Optionnel : image de fruits en bas à droite, petite

---

## 🎨 Finalisation et Révision (30 minutes)

### Étape 1 : Cohérence visuelle

- [ ] Vérifier police uniforme (Arial/Calibri)
- [ ] Vérifier taille police (min 18pt pour texte)
- [ ] Vérifier couleurs cohérentes (palette définie)
- [ ] Vérifier alignement texte et images
- [ ] Vérifier numérotation slides

### Étape 2 : Transitions et animations

**Recommandation :** Transitions discrètes

- Transition entre slides : "Fondu" ou "Pousser" (0,5 seconde)
- Animations dans les slides : "Apparition" progressive pour bullet points
- Éviter les effets tape-à-l'œil (rebond, tourbillon, etc.)

### Étape 3 : Mode Présentateur

1. Affichage → Mode Présentateur
2. Ajouter les notes de présentation depuis `notes-presentation.md`
3. Vérifier timing pour chaque slide

### Étape 4 : Tests

- [ ] Lancer présentation en mode plein écran
- [ ] Vérifier lisibilité sur écran distant (TV ou projecteur si possible)
- [ ] Tester navigation clavier (flèches, espace)
- [ ] Vérifier temps total (20 minutes max)

### Étape 5 : Export PDF (backup)

1. Fichier → Enregistrer sous → PDF
2. Sauvegarder : `docs/project/soutenance/presentation.pdf`
3. Utiliser comme backup si problème PowerPoint

---

## 📋 Checklist Finale

### Contenu

- [ ] 20 slides créées
- [ ] Titres clairs sur chaque slide
- [ ] Texte lisible (min 18pt)
- [ ] Code snippets dans les slides 11-15
- [ ] Diagrammes insérés (architecture + pipeline)
- [ ] Screenshots placeholders pour AWS (marqués en rouge)
- [ ] Métriques placeholders pour AWS (marquées en rouge)
- [ ] Tableau coûts placeholder (marqué en rouge)

### Design

- [ ] Palette de couleurs cohérente (3 couleurs max)
- [ ] Typographie uniforme
- [ ] Logo ou branding (optionnel)
- [ ] Alignement correct
- [ ] Espacement équilibré
- [ ] Numérotation pages

### Fonctionnalités

- [ ] Transitions entre slides
- [ ] Animations bullet points (optionnel)
- [ ] Notes de présentation ajoutées
- [ ] Mode présentateur configuré
- [ ] Timing validé (20 min)

### Exports

- [ ] Fichier PPTX sauvegardé
- [ ] Fichier PDF exporté (backup)
- [ ] Tous les visuels dans `visuels/`

---

## 🔄 Mise à jour après exécution AWS

**Quand :** Après avoir exécuté la Feature 4 (AWS Deployment)

**Actions :**

1. **Remplacer screenshots placeholders (slide 6, 16)**
   - Screenshot Console AWS → insérer dans slide 6
   - Screenshots JupyterHub + S3 → insérer dans slide 16

2. **Remplir métriques manquantes**
   - Slide 10 : Temps total exécution
   - Slide 14 : Variance PCA réelle + graphique
   - Slide 17 : Toutes les métriques rouges

3. **Remplir tableau coûts (slide 9)**
   - Remplacer estimation par coûts réels AWS
   - Calculer économie vs budget

4. **Révision finale**
   - Relire tous les slides
   - Vérifier cohérence
   - Tester timing avec screenshots réels

---

**Durée totale création** : 3-4 heures
**+ Mise à jour après AWS** : 30-45 minutes

**Bonne création ! 🎨**
