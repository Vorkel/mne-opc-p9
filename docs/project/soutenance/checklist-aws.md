# Checklist Captures et Métriques AWS - Feature 4

**Objectif :** S'assurer de capturer tous les screenshots et métriques nécessaires pour finaliser la présentation

**Quand :** Pendant et après l'exécution de la Feature 4 (Déploiement AWS)

---

## 📸 PHASE 1 : Screenshots à capturer PENDANT l'exécution

### 1.1 Console AWS - Cluster EMR actif

**Quand :** Juste après la création du cluster (Phase 2 du guide AWS)

**Où :** Console AWS → EMR → Clusters → [votre cluster]

**Ce qui doit être visible :**
- [ ] Nom du cluster
- [ ] Status : "Running" (vert)
- [ ] Master instance : m6g.xlarge
- [ ] Core instances : 2x m6g.large
- [ ] Applications : Spark, JupyterHub, TensorFlow
- [ ] Région : eu-west-1
- [ ] Timeline avec date/heure de création

**Comment capturer :**
- Mac : Cmd + Shift + 4 → sélectionner zone
- Windows : Outil Capture d'écran

**Sauvegarder sous :**
```
docs/project/soutenance/visuels/screenshots/aws-emr-console.png
```

**Utilisation :** Slide 6 de la présentation

---

### 1.2 Console AWS - Configuration du cluster

**Quand :** Juste après création cluster (optionnel, pour backup)

**Où :** Console AWS → EMR → Clusters → [cluster] → Onglet "Hardware"

**Ce qui doit être visible :**
- [ ] Liste des instances (master + 2 workers)
- [ ] Type d'instances (m6g.xlarge, m6g.large)
- [ ] Market type : Spot
- [ ] Availability Zone (eu-west-1a, eu-west-1b, etc.)

**Sauvegarder sous :**
```
docs/project/soutenance/visuels/screenshots/aws-emr-hardware.png
```

**Utilisation :** Backup, questions jury

---

### 1.3 JupyterHub - Notebook ouvert

**Quand :** Après connexion à JupyterHub (Phase 3 du guide AWS)

**Où :** JupyterHub EMR → Notebook ouvert

**Ce qui doit être visible :**
- [ ] Nom du notebook : "P8_Notebook_Linux_EMR_PySpark_V1.0.ipynb"
- [ ] Liste des cellules visibles
- [ ] Au moins une cellule exécutée (kernel actif)
- [ ] Barre d'adresse JupyterHub visible (montre URL EMR)

**Sauvegarder sous :**
```
docs/project/soutenance/visuels/screenshots/jupyterhub-notebook.png
```

**Utilisation :** Slide 16

---

### 1.4 JupyterHub - Cellule PCA exécutée

**Quand :** Pendant l'exécution du notebook, après la cellule PCA

**Où :** JupyterHub → Cellule de code PCA avec output

**Ce qui doit être visible :**
- [ ] Code de la PCA visible (pca.fit(), pca.transform())
- [ ] Output de la cellule montrant :
  - Variance expliquée (ex: "Variance expliquée : 95.2%")
  - Nombre de composantes (256)
  - Confirmation succès
- [ ] Numéro de cellule visible (ex: In [14])

**Sauvegarder sous :**
```
docs/project/soutenance/visuels/screenshots/jupyterhub-pca-output.png
```

**Utilisation :** Slide 14, démonstration variance PCA

---

### 1.5 Bucket S3 - Dataset uploadé

**Quand :** Après upload du dataset (Phase 1 du guide AWS)

**Où :** Console AWS → S3 → Buckets → fruits-classification-p9-maxime → Test/

**Ce qui doit être visible :**
- [ ] Structure du bucket :
  - dataset/
    - Training/
      - Apple/ (folders de fruits)
      - Banana/
      - Orange/
      - etc.
- [ ] Nombre de dossiers (131 catégories)
- [ ] Taille totale approximative (~2 GB)

**Sauvegarder sous :**
```
docs/project/soutenance/visuels/screenshots/s3-bucket-dataset.png
```

**Utilisation :** Slide 16

---

### 1.6 Bucket S3 - Résultats PCA générés

**Quand :** Après exécution complète du notebook (Phase 5 du guide AWS)

**Où :** Console AWS → S3 → Buckets → fruits-classification-p9-maxime → Results/pca_output/

**Ce qui doit être visible :**
- [ ] Dossier `Results/pca_output/`
- [ ] Fichiers Parquet listés (part-00000.parquet, part-00001.parquet, etc.)
- [ ] Taille des fichiers (en MB)
- [ ] Date de dernière modification (prouve que c'est récent)
- [ ] Nombre de fichiers

**Sauvegarder sous :**
```
docs/project/soutenance/visuels/screenshots/s3-bucket-results-pca.png
```

**Utilisation :** Slide 16

---

## 📊 PHASE 2 : Métriques à collecter PENDANT l'exécution

### 2.1 Métriques du pipeline (dans le notebook)

**Où :** Ajouter des cellules de code dans le notebook pour mesurer

#### Temps de chargement S3

**Code à ajouter après chargement :**
```python
import time

start_time = time.time()
df_images = spark.read.format("image") \
    .option("dropInvalid", True) \
    .load("s3://fruits-classification-p9-maxime/Test/")
df_images.cache()
count = df_images.count()
load_time = time.time() - start_time

print(f"✅ Images chargées : {count}")
print(f"⏱️ Temps de chargement : {load_time:.2f} secondes ({load_time/60:.2f} minutes)")

# NOTER CES VALEURS IMMÉDIATEMENT
```

**Valeurs à noter :**
- [ ] Nombre d'images chargées : ___________
- [ ] Temps de chargement : ___________ minutes

---

#### Temps d'extraction de features

**Code à ajouter après extraction :**
```python
start_time = time.time()
df_features = extract_features(df_preprocessed, model_broadcast)
df_features.cache()
count = df_features.count()
extraction_time = time.time() - start_time

print(f"✅ Features extraites : {count}")
print(f"⏱️ Temps d'extraction : {extraction_time:.2f} secondes ({extraction_time/60:.2f} minutes)")
```

**Valeurs à noter :**
- [ ] Nombre de features extraites : ___________
- [ ] Temps d'extraction : ___________ minutes

---

#### Variance PCA (CRITIQUE)

**Code à ajouter après PCA :**
```python
from pyspark.ml.feature import PCA

pca = PCA(k=256, inputCol="features_vector", outputCol="features_pca")

# Fit
start_fit = time.time()
pca_model = pca.fit(df_vectorized)
fit_time = time.time() - start_fit

# Variance expliquée
variance_expliquee = sum(pca_model.explainedVariance[:256])

print(f"✅ Variance expliquée : {variance_expliquee:.2%}")
print(f"⏱️ Temps de fit PCA : {fit_time:.2f} secondes ({fit_time/60:.2f} minutes)")

# Transform
start_transform = time.time()
df_pca = pca_model.transform(df_vectorized)
df_pca.cache()
count = df_pca.count()
transform_time = time.time() - start_transform

print(f"✅ Vecteurs PCA générés : {count}")
print(f"⏱️ Temps de transform : {transform_time:.2f} secondes ({transform_time/60:.2f} minutes)")
```

**Valeurs à noter :**
- [ ] Variance expliquée : ___________ %
- [ ] Temps de fit : ___________ minutes
- [ ] Temps de transform : ___________ minutes
- [ ] Vecteurs PCA générés : ___________

---

#### Temps de sauvegarde S3

**Code à ajouter après sauvegarde :**
```python
start_time = time.time()
df_pca.select("path", "label", "features_pca") \
    .write \
    .mode("overwrite") \
    .parquet("s3://fruits-classification-p9-maxime/Results/pca_output/")
write_time = time.time() - start_time

print(f"✅ Résultats sauvegardés")
print(f"⏱️ Temps d'écriture : {write_time:.2f} secondes ({write_time/60:.2f} minutes)")
```

**Valeurs à noter :**
- [ ] Temps d'écriture : ___________ minutes

---

#### Temps total du pipeline

**Code à ajouter à la fin du notebook :**
```python
total_time = load_time + extraction_time + fit_time + transform_time + write_time

print(f"\n{'='*60}")
print(f"⏱️ TEMPS TOTAL DU PIPELINE")
print(f"{'='*60}")
print(f"Chargement S3       : {load_time/60:>6.2f} min")
print(f"Extraction features : {extraction_time/60:>6.2f} min")
print(f"PCA fit             : {fit_time/60:>6.2f} min")
print(f"PCA transform       : {transform_time/60:>6.2f} min")
print(f"Sauvegarde S3       : {write_time/60:>6.2f} min")
print(f"{'='*60}")
print(f"TOTAL               : {total_time/60:>6.2f} min")
print(f"{'='*60}")
print(f"\n✅ Pipeline complet exécuté avec succès !")
```

**Valeur à noter :**
- [ ] Temps total : ___________ minutes

---

### 2.2 Graphique variance PCA (CRITIQUE)

**Code à ajouter dans une nouvelle cellule après PCA :**

```python
import matplotlib.pyplot as plt

# Récupérer variance
variance = pca_model.explainedVariance
cumulative_variance = []
total = 0
for v in variance:
    total += v
    cumulative_variance.append(total)

# Créer graphique
plt.figure(figsize=(12, 7))
plt.plot(range(1, len(cumulative_variance)+1), cumulative_variance,
         linewidth=2, color='#1E3A8A', label='Variance cumulative')
plt.axhline(y=0.9, color='red', linestyle='--', linewidth=2,
            label='Seuil 90%')
plt.xlabel('Nombre de composantes principales', fontsize=14, fontweight='bold')
plt.ylabel('Variance expliquée cumulative', fontsize=14, fontweight='bold')
plt.title('Variance Expliquée par PCA - Fruits Classification',
          fontsize=16, fontweight='bold')
plt.legend(fontsize=12, loc='lower right')
plt.grid(True, alpha=0.3)
plt.tight_layout()

# Sauvegarder localement dans JupyterHub
plt.savefig('variance_pca.png', dpi=300, bbox_inches='tight')
plt.show()

print(f"✅ Graphique sauvegardé : variance_pca.png")
print(f"📊 Variance à 256 composantes : {cumulative_variance[255]:.2%}")
```

**Actions après exécution :**
- [ ] Vérifier que le graphique s'affiche correctement
- [ ] Noter la variance à 256 composantes : ___________ %
- [ ] Télécharger le fichier `variance_pca.png` depuis JupyterHub :
  - Clic droit sur fichier → Download
  - Sauvegarder dans `docs/project/soutenance/visuels/`

**Utilisation :** Slide 14

---

## 💰 PHASE 3 : Coûts AWS (24-48h APRÈS l'exécution)

### 3.1 Relever la durée du cluster

**Quand :** Après terminaison du cluster

**Où :** Console AWS → EMR → Clusters → [cluster] → Timeline

**Ce qui doit être visible :**
- [ ] Heure de création
- [ ] Heure de terminaison
- [ ] Durée totale (heures:minutes)

**Valeur à noter :**
- [ ] Durée de vie du cluster : ___________ heures

---

### 3.2 Consulter la facture AWS

**Quand :** 24-48h après terminaison du cluster

**Où :** Console AWS → Billing → Bills → Mois en cours

**Actions :**
1. Aller sur AWS Billing Dashboard
2. Sélectionner le mois en cours
3. Rechercher :
   - Amazon EMR
   - Amazon S3
   - AWS Data Transfer
4. Noter les coûts détaillés

**Tableau à remplir :**

| Service | Détail | Durée | Coût unitaire | Coût total |
|---------|--------|-------|---------------|------------|
| EMR Master | m6g.xlarge Spot | _____ h | _____ €/h | _____ € |
| EMR Core (x2) | m6g.large Spot | _____ h | _____ €/h | _____ € |
| EMR Service Fee | 10% instances | - | - | _____ € |
| S3 Storage | _____ GB | 1 mois | _____ €/GB | _____ € |
| S3 Requests | _____ requêtes | - | - | _____ € |
| S3 Transfer | _____ GB | - | - | _____ € |
| CloudWatch Logs | _____ GB | - | - | _____ € |
| Autres | _____ | - | - | _____ € |
| **TOTAL** | | | | **_____ €** |

**Actions après collecte :**
- [ ] Remplir le tableau dans `metriques.md`
- [ ] Calculer économie : (10€ - coût réel) / 10€ × 100 = _____ %
- [ ] Mettre à jour slide 9 de la présentation

---

### 3.3 Créer tableau coûts pour la présentation

**Où :** PowerPoint, Slide 9

**Contenu :**
Copier les valeurs du tableau ci-dessus dans un tableau PowerPoint formaté.

**Instructions :**
1. Insérer → Tableau dans slide 9
2. Remplir avec valeurs réelles
3. Mettre en gras la ligne TOTAL
4. Ajouter note en bas : "Économie : X% vs budget 10€"

---

## 📋 PHASE 4 : Finalisation de la présentation

### 4.1 Remplacer tous les placeholders

**Fichiers à mettre à jour :**

1. **metriques.md**
   - [ ] Remplir tous les champs marqués 🔴 [MANQUANT]
   - [ ] Vérifier cohérence des données

2. **PowerPoint (presentation.pptx)**
   - [ ] Slide 6 : Insérer screenshot Console EMR
   - [ ] Slide 9 : Insérer tableau coûts réels
   - [ ] Slide 10 : Insérer temps total exécution
   - [ ] Slide 14 : Insérer graphique variance PCA + variance réelle
   - [ ] Slide 16 : Insérer 3 screenshots (Console, JupyterHub, S3)
   - [ ] Slide 17 : Remplir toutes les métriques

3. **Vérifier cohérence**
   - [ ] Tous les chiffres sont identiques dans tous les fichiers
   - [ ] Aucun placeholder rouge ne reste
   - [ ] Screenshots en haute qualité (lisibles)

---

### 4.2 Tests finaux

- [ ] Relire présentation slide par slide
- [ ] Vérifier lisibilité screenshots (zoom pour tester)
- [ ] Tester timing : répétition chronomètre en main
- [ ] Vérifier notes de présentation

---

## 🎯 Checklist Récapitulative Globale

### Screenshots (6)

- [ ] **1. Console AWS - Cluster EMR actif** → Slide 6
- [ ] **2. Console AWS - Hardware cluster** (backup)
- [ ] **3. JupyterHub - Notebook ouvert** → Slide 16
- [ ] **4. JupyterHub - Cellule PCA output** → Slide 14
- [ ] **5. S3 - Dataset uploadé** → Slide 16
- [ ] **6. S3 - Résultats PCA** → Slide 16

### Métriques (9)

- [ ] **1. Temps chargement S3**
- [ ] **2. Temps extraction features**
- [ ] **3. Variance PCA** (CRITIQUE) → Slides 14, 17
- [ ] **4. Temps fit PCA**
- [ ] **5. Temps transform PCA**
- [ ] **6. Temps sauvegarde S3**
- [ ] **7. Temps total pipeline** → Slides 10, 17
- [ ] **8. Durée cluster**
- [ ] **9. Coûts AWS réels** → Slides 9, 17

### Visuels (1)

- [ ] **Graphique variance PCA** → Slide 14

### Tableau (1)

- [ ] **Tableau coûts AWS détaillé** → Slide 9

---

## 💡 Conseils Pratiques

### Pendant l'exécution

1. **Prendre les screenshots au fur et à mesure**
   - Ne pas attendre la fin pour tout capturer
   - Risque : cluster terminé = plus de screenshots possibles

2. **Noter les métriques immédiatement**
   - Créer un fichier texte temporaire
   - Copier/coller les outputs du notebook

3. **Sauvegarder régulièrement**
   - Screenshots dans le bon dossier immédiatement
   - Backup sur cloud (Drive, Dropbox) recommandé

### Si quelque chose échoue

**Si cluster s'arrête avant screenshots :**
→ Les logs EMR restent disponibles pendant 7 jours
→ Consulter CloudWatch Logs pour récupérer certaines métriques

**Si screenshot raté :**
→ Possibilité de relancer cluster brièvement juste pour screenshots
→ Coût minimal (~0,10€ pour 15 min)

**Si métrique non mesurée :**
→ Estimer en extrapolant depuis tests locaux
→ Mentionner que c'est une estimation dans la présentation

---

## 📞 Support

**Si problème pendant exécution :**
1. Consulter `docs/project/guides/aws-setup-guide.md` section Troubleshooting
2. Vérifier logs CloudWatch
3. Vérifier Spark UI (port 8088 sur master)

**Si doute sur métrique :**
→ Consultez `metriques.md` qui contient les codes Python pour mesurer

---

**Temps total estimé pour collecte :** 15-20 minutes pendant exécution + 15 min après
**Bonne exécution AWS ! 🚀**
