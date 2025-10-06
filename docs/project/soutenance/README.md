# Dossier Soutenance P9 - Guide d'Utilisation

**Objectif :** Ce dossier contient tous les documents nécessaires pour préparer et réaliser la soutenance du projet P9

**Date de création :** 6 janvier 2025
**Statut :** ✅ Phase A complète (70%) | ⏳ Phase B en attente exécution AWS (30%)

---

## 📁 Structure du Dossier

```
docs/project/soutenance/
├── README.md                      ← Vous êtes ici
├── outline.md                     ← Structure détaillée des 20 slides
├── notes-presentation.md          ← Script complet de présentation
├── questions-reponses.md          ← FAQ jury (23 Q&R)
├── metriques.md                   ← Métriques du projet (avec placeholders AWS)
├── guide-powerpoint.md            ← Instructions création PowerPoint
├── instructions-diagrammes.md     ← Spécifications diagrammes Draw.io
├── checklist-aws.md               ← Checklist captures pendant AWS
├── visuels/
│   ├── diagrammes/                ← Diagrammes Draw.io (à créer)
│   └── screenshots/               ← Screenshots AWS (à capturer)
└── presentation.pptx              ← PowerPoint final (à créer)
```

---

## 🎯 Comment Utiliser Ce Dossier

### Phase A : MAINTENANT (sans AWS) - 5h

**Objectif :** Créer 70% de la présentation

#### Étape 1 : Créer les diagrammes (1h)

1. Lire `instructions-diagrammes.md`
2. Ouvrir Draw.io : https://app.diagrams.net
3. Créer les 2 diagrammes :
   - `architecture-big-data.png` (Slide 4)
   - `pipeline-pyspark.png` (Slide 10)
4. Exporter en PNG 300 DPI
5. Sauvegarder dans `visuels/diagrammes/`

**Temps :** 30 min par diagramme

---

#### Étape 2 : Créer le PowerPoint (3h)

1. Lire `guide-powerpoint.md`
2. Créer le fichier `presentation.pptx`
3. Configurer template (couleurs, typographie)
4. Créer les 20 slides selon les instructions
5. Insérer les diagrammes créés à l'étape 1
6. Marquer les placeholders AWS en ROUGE :
   - Slide 6 : Screenshot Console EMR
   - Slide 9 : Tableau coûts
   - Slide 14 : Graphique variance PCA
   - Slide 16 : 3 screenshots
   - Slide 17 : Métriques

**Temps :** 3-4h

**Résultat :** Présentation à 70% complète

---

#### Étape 3 : Préparer la soutenance (1h)

1. Lire `notes-presentation.md` (script slide par slide)
2. Lire `questions-reponses.md` (23 questions anticipées)
3. S'entraîner oralement (répéter avec timer 20 min)
4. Prendre des notes personnelles si nécessaire

**Temps :** 1h de lecture + répétitions

---

### Phase B : APRÈS AWS (Feature 4) - 1h30

**Objectif :** Finaliser la présentation avec les éléments AWS

#### Étape 1 : Capturer pendant l'exécution AWS (20 min)

1. **AVANT de lancer le cluster :** Ouvrir `checklist-aws.md`
2. **PENDANT l'exécution :** Capturer les 6 screenshots
   - Console AWS - Cluster EMR
   - JupyterHub - Notebook
   - JupyterHub - Cellule PCA
   - S3 - Dataset
   - S3 - Résultats
3. **PENDANT l'exécution :** Mesurer les métriques
   - Temps de chargement
   - Temps d'extraction features
   - Variance PCA (CRITIQUE)
   - Temps total
4. **PENDANT l'exécution :** Générer graphique variance PCA
5. Sauvegarder tout dans `visuels/screenshots/`

**Temps :** 15-20 min répartis pendant l'exécution

---

#### Étape 2 : Collecter coûts AWS (24-48h après)

1. Console AWS → Billing → Bills
2. Relever coûts détaillés (EMR, S3, Transfer)
3. Remplir tableau dans `metriques.md`
4. Calculer économie vs budget 10€

**Temps :** 15 min

---

#### Étape 3 : Finaliser PowerPoint (30 min)

1. Ouvrir `presentation.pptx`
2. Remplacer tous les placeholders ROUGES :
   - Slide 6 : Insérer screenshot Console EMR
   - Slide 9 : Insérer tableau coûts réels
   - Slide 10 : Insérer temps total
   - Slide 14 : Insérer graphique + variance réelle
   - Slide 16 : Insérer 3 screenshots
   - Slide 17 : Remplir métriques
3. Vérifier cohérence (tous les chiffres identiques)
4. Révision finale

**Temps :** 25-30 min

---

#### Étape 4 : Répétition finale (30 min)

1. Répéter présentation avec timer (20 min max)
2. Vérifier transitions
3. S'entraîner aux questions jury
4. Préparer backup (PDF, screenshots locaux)

**Temps :** 30 min

---

## 📄 Description des Fichiers

### 1. outline.md (400+ lignes)

**Contenu :**
- Structure détaillée des 20 slides
- Contenu complet pour chaque slide
- Timing par slide et par section
- Checklist des visuels par slide
- Notes sur éléments manquants (AWS)

**Quand l'utiliser :**
- Lors de la création du PowerPoint (référence pour chaque slide)
- Pour vérifier la cohérence du contenu

---

### 2. notes-presentation.md (500+ lignes)

**Contenu :**
- Script complet slide par slide
- Ce qu'il faut dire pour chaque slide (mot à mot ou paraphrasé)
- Timing précis
- Conseils de présentation
- Gestion du stress et des questions

**Quand l'utiliser :**
- Pendant la préparation orale
- Juste avant la soutenance (relecture)
- En mode Présentateur PowerPoint (notes)

---

### 3. questions-reponses.md (400+ lignes)

**Contenu :**
- 23 questions anticipées du jury
- Réponses détaillées (1-2 min chacune)
- 7 catégories :
  1. Architecture Big Data
  2. Améliorations techniques
  3. Cloud et coûts
  4. Conformité RGPD
  5. Mise en œuvre technique
  6. Perspectives
  7. Questions pièges

**Quand l'utiliser :**
- Pendant la préparation (apprendre les réponses)
- Phase discussion (5 min après présentation)

---

### 4. metriques.md (400+ lignes)

**Contenu :**
- Toutes les métriques du projet
- Métriques dataset (87k images, 131 catégories, etc.)
- Métriques pipeline (temps, variance PCA, etc.)
- Métriques cluster EMR
- Métriques coûts AWS
- Codes Python pour mesurer chaque métrique
- Checklist de collecte

**Quand l'utiliser :**
- PENDANT l'exécution AWS (pour mesurer métriques)
- APRÈS AWS (pour remplir placeholders)
- Référence pour slides 9, 10, 14, 17

---

### 5. guide-powerpoint.md (500+ lignes)

**Contenu :**
- Instructions configuration initiale (template, couleurs, typo)
- Instructions slide par slide (20 slides)
- Contenu exact à insérer
- Conseils de design
- Checklist finalisation
- Instructions mise à jour après AWS

**Quand l'utiliser :**
- Phase A : Création du PowerPoint
- Phase B : Mise à jour avec éléments AWS

---

### 6. instructions-diagrammes.md (300+ lignes)

**Contenu :**
- Spécifications pour 2 diagrammes Draw.io
- Diagramme 1 : Architecture Big Data (Slide 4)
- Diagramme 2 : Pipeline PySpark (Slide 10)
- Instructions étape par étape
- Palette de couleurs
- Alternatives à Draw.io

**Quand l'utiliser :**
- Phase A : Création des diagrammes
- Avant de créer les slides 4 et 10

---

### 7. checklist-aws.md (400+ lignes)

**Contenu :**
- Checklist complète pour Feature 4
- 6 screenshots à capturer (avec instructions précises)
- 9 métriques à mesurer (avec codes Python)
- 1 graphique à générer (variance PCA)
- 1 tableau coûts à remplir
- Timeline : pendant / après / 24-48h après

**Quand l'utiliser :**
- **CRITIQUE :** Ouvrir AVANT de lancer Feature 4
- Suivre pendant toute l'exécution AWS
- Cocher au fur et à mesure

---

## ⚠️ Points Critiques

### 🔴 Ne PAS oublier

1. **Ouvrir `checklist-aws.md` AVANT Feature 4**
   - Risque : oublier de capturer screenshots
   - Conséquence : impossible à récupérer après terminaison cluster

2. **Mesurer variance PCA pendant exécution**
   - Métrique CRITIQUE pour slides 14 et 17
   - Génération graphique variance

3. **Relever coûts AWS 24-48h après**
   - Facturation différée
   - Nécessaire pour slide 9

---

## 📊 État d'Avancement Actuel

### ✅ Phase A : Complète (70%)

- [x] Structure dossier créée
- [x] Documentation complète (7 fichiers)
- [x] Instructions diagrammes rédigées
- [x] Instructions PowerPoint rédigées
- [x] Script présentation rédigé
- [x] Questions-réponses préparées

### ⏳ Phase B : En attente (30%)

- [ ] Diagrammes Draw.io à créer (1h)
- [ ] PowerPoint à créer (3h)
- [ ] Feature 4 AWS à exécuter
- [ ] Screenshots à capturer
- [ ] Métriques à mesurer
- [ ] Graphique PCA à générer
- [ ] Coûts AWS à relever
- [ ] PowerPoint à finaliser

---

## 🎯 Checklist Globale

### Avant Feature 4

- [ ] Créer diagrammes Draw.io (2)
- [ ] Créer PowerPoint (20 slides avec placeholders)
- [ ] Lire script présentation
- [ ] Lire questions-réponses
- [ ] S'entraîner oralement (répétition 20 min)
- [ ] Préparer checklist AWS imprimée

### Pendant Feature 4

- [ ] Capturer 6 screenshots
- [ ] Mesurer 9 métriques
- [ ] Générer graphique variance PCA
- [ ] Télécharger graphique depuis JupyterHub

### 24-48h après Feature 4

- [ ] Relever coûts AWS (facture)
- [ ] Remplir tableau coûts

### Finalisation

- [ ] Mettre à jour PowerPoint (placeholders → valeurs réelles)
- [ ] Vérifier cohérence métriques
- [ ] Révision finale présentation
- [ ] Répétition finale (20 min chrono)
- [ ] Export PDF (backup)

---

## 💡 Conseils

### Pour gagner du temps

1. **Créer les diagrammes en premier**
   - Vous en avez besoin pour slides 4 et 10
   - 1h de travail focalisé

2. **Utiliser les templates PowerPoint**
   - Dupliquer slides similaires (ex: slides 11-15)
   - Gagner 30-45 min

3. **Préparer checklist AWS imprimée**
   - Format papier plus pratique pendant exécution
   - Ne pas risquer d'oublier

### Pour la qualité

1. **Vérifier cohérence des chiffres**
   - Même variance PCA partout
   - Même temps total partout
   - Même coûts partout

2. **Tester lisibilité screenshots**
   - Zoomer dans PowerPoint
   - Si illisible, refaire (mieux avant terminaison cluster)

3. **Répéter avec timer**
   - 20 min MAX
   - Réduire slides 7, 12 si dépassement

---

## 📞 Support

**Si problème technique :**
→ Voir `docs/project/guides/aws-setup-guide.md` section Troubleshooting

**Si doute sur contenu :**
→ Relire `outline.md` et `notes-presentation.md`

**Si question non anticipée :**
→ Structure réponse : Direct → Justification → Exemple → Ouverture (1-2 min max)

---

## 🎓 Résumé du Parcours

| Phase | Tâches | Durée | Fichiers utilisés |
|-------|--------|-------|-------------------|
| **A - Maintenant** | Créer diagrammes + PowerPoint | 4h | guide-powerpoint.md, instructions-diagrammes.md |
| | Préparer soutenance | 1h | notes-presentation.md, questions-reponses.md |
| **B - Pendant AWS** | Capturer screenshots + métriques | 20 min | checklist-aws.md, metriques.md |
| **B - Après AWS** | Relever coûts | 15 min | checklist-aws.md |
| | Finaliser PowerPoint | 30 min | guide-powerpoint.md |
| | Répétition finale | 30 min | notes-presentation.md |
| **TOTAL** | | **~7h** | |

---

**Bonne préparation et bonne soutenance ! 🎓🚀**
