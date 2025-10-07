# Guide Création Cluster EMR - Interface 2025 (v2.0)

**Date :** 7 octobre 2025
**Compatible avec :** EMR 7.10.0 (nouvelle interface AWS)
**Public :** Utilisateur ayant déjà complété Phase 0 et Phase 1 du guide principal

---

## Configuration Cluster EMR - Étape par Étape

### ✅ Prérequis

- Région eu-west-1 sélectionnée ⚠️
- Bucket S3 créé avec dataset uploadé
- Rôles IAM créés (EMR_DefaultRole_P9, EMR_EC2_DefaultRole_P9)

---

## SECTION 1 : Nom et Applications

### **Nom**
```
Fruits-Classification-P9-Cluster
```

### **Version Amazon EMR**
- Sélectionner : **emr-7.10.0** (dernière version stable)
- ✅ Compatible avec Spark 3.5.5 et TensorFlow 2.18.0

### **Offre d'applications**

**Cliquer sur les cartes suivantes :**
- ✅ **Spark Interactive** (carte avec logo Spark)
- ✅ **Core Hadoop** (carte avec logo Hadoop)

**Applications incluses automatiquement :**
- Spark 3.5.5
- Hadoop 3.4.1
- JupyterEnterpriseGateway 2.6.0
- JupyterHub 1.5.0
- TensorFlow 2.18.0
- Hive 3.1.3
- Livy 0.8.0

**NE PAS COCHER :** Flink, HBase, Presto, Trino (non nécessaires pour ce projet)

### **Paramètres du catalogue de données AWS Glue**
- ❌ **DÉCOCHER** "Utiliser pour les métadonnées de table Hive"
- ❌ **DÉCOCHER** "Utiliser pour les métadonnées de table Spark"

### **Options du système d'exploitation**
- ✅ **COCHER** "Appliquez automatiquement les dernières mises à jour Amazon Linux"

---

## SECTION 2 : Configuration de Cluster

### **Méthode de configuration**
- Laisser sélectionné : **Groupes d'instances uniformes** ✅

### **Groupes d'instances uniformes**

#### **A. Primaire (Master Node)**

1. **Cliquer sur le bouton "Actions"** dans la carte "Primaire"
2. **Sélectionner "Modifier le type d'instance"**
3. **Choisir le type d'instance :**
   - Dans la barre de recherche, taper : `m6g.xlarge`
   - Sélectionner : **m6g.xlarge**
   - Caractéristiques :
     - 4 vCore
     - 15.25 GiB mémoire
     - Prix Spot le plus bas : ~0.081 USD/h

4. **Configuration de nœud (section facultatif) :**
   - Laisser les valeurs par défaut pour le volume racine EBS :
     - Taille : 15 GiB
     - IOPS : 3000
     - Débit : 125 MiB/s

#### **B. Unité principale (Core Nodes)**

1. **Cliquer sur le bouton "Actions"** dans la carte "Unité principale"
2. **Sélectionner "Modifier le type d'instance"**
3. **Choisir le type d'instance :**
   - Taper : `m6g.xlarge`
   - Sélectionner : **m6g.xlarge**

4. **Configuration de nœud :** Laisser par défaut

#### **C. Tâche - 1 (Task Nodes)**

**IMPORTANT :** Supprimer ce groupe d'instances

1. **Cliquer sur "Retirer le groupe d'instances"** (bouton en haut à droite de la carte "Tâche - 1")
2. Confirmer la suppression

**Pourquoi ?** Pour ce projet, nous n'avons besoin que de 1 Master + 1 Core pour optimiser les coûts.

---

## SECTION 3 : Dimensionnement et Mise en Service du Cluster

### **Choisir une option**
- Sélectionner : **Définir manuellement la taille du cluster** ✅

### **Configuration de mise en service**

**Tableau de configuration :**

| Nom | Type d'instance | Taille de l'instance(s) | Utiliser l'option d'achat Spot |
|-----|-----------------|-------------------------|-------------------------------|
| Unité principale | m6g.xlarge | **1** | ✅ **COCHER** |
| Tâche - 1 | m6g.xlarge | **0** (supprimer cette ligne si présente) | - |

**Actions :**
1. Dans la colonne "Taille de l'instance(s)" pour "Unité principale" : Taper **1**
2. **IMPORTANT : Cocher la case "Utiliser l'option d'achat Spot"** pour "Unité principale"
3. Si la ligne "Tâche - 1" existe, la supprimer

**💰 Estimation des coûts :**
- Master (Primaire) : ~0.081 USD/h (Spot)
- Core (Unité principale) : ~0.081 USD/h (Spot)
- **Total : ~0.16 USD/h** (au lieu de 0.344 USD/h en On-Demand)
- Pour 3 heures : **~0.48 USD** (~0.45€)

---

## SECTION 4 : Réseaux

### **Cloud privé virtuel (VPC)**
- Laisser le VPC par défaut : `vpc-0a73c5d3a4e316e91` (ou votre VPC par défaut)
- ⚠️ Ne rien modifier ici

### **Sous-réseau**
- Laisser le sous-réseau par défaut : `subnet-059488f62e587aa8c` (ou votre subnet par défaut)
- ⚠️ Doit être dans eu-west-1a, eu-west-1b ou eu-west-1c

### **Groupes de sécurité EC2 (pare-feu)**
- Laisser les valeurs par défaut (AWS créera automatiquement les security groups)
- ⚠️ Nous les configurerons APRÈS la création du cluster

---

## SECTION 5 : Résiliation du Cluster et Remplacement des Nœuds

### **Résiliation du cluster**
- ✅ **COCHER** "Résilier le cluster après le temps d'inactivité"
- **Temps d'inactivité :** Modifier de `1 heure` à **`3 heures`**

**Pourquoi 3 heures ?**
- Exécution du notebook : 1h30-2h
- Marge de sécurité : 1h-1h30
- Évite terminaison accidentelle pendant l'exécution

---

## SECTION 6 : Actions d'Amorçage

- ⚠️ **Laisser vide** (0 actions)
- Pas d'actions d'amorçage nécessaires pour ce projet

---

## SECTION 7 : Journaux de Cluster

### **Emplacement Amazon S3**
- ✅ **RECOMMANDÉ :** Activer les logs pour diagnostic

1. Cliquer dans le champ "Emplacement Amazon S3"
2. Taper : `s3://fruits-classification-p9-mne/logs/`
3. AWS créera automatiquement ce dossier

**Alternative :** Laisser vide si vous voulez économiser quelques centimes

---

## SECTION 8 : Identifications (Tags)

- ⚠️ **Optionnel** - Laisser vide
- Ou ajouter un tag si vous voulez :
  - **Clé :** `Project`
  - **Valeur :** `P9-Fruits-Classification`

---

## SECTION 9 : Paramètres du Logiciel

- ⚠️ **Laisser vide** (pas de configuration personnalisée nécessaire)

---

## SECTION 10 : Configuration de Sécurité et Paire de Clés EC2

### **Configuration de sécurité**
- Laisser : **"Choisir une configuration de sécurité"** (vide)
- Pas de configuration de sécurité personnalisée nécessaire

### **Paire de clés Amazon EC2 pour SSH**

**Option 1 : Créer une nouvelle clé (RECOMMANDÉ)**

1. **Cliquer sur "Créer une paire de clés"** (bouton bleu)
2. **Une nouvelle fenêtre s'ouvre** (console EC2)
3. **Remplir :**
   - **Nom :** `emr-p9-keypair`
   - **Type de paire de clés :** RSA
   - **Format de fichier de clé privée :** .pem
4. **Cliquer sur "Créer une paire de clés"**
5. **Le fichier `emr-p9-keypair.pem` se télécharge**
6. **IMPORTANT - Sauvegarder la clé immédiatement :**
   ```bash
   # Dans Terminal Mac :
   mv ~/Downloads/emr-p9-keypair.pem ~/.ssh/
   chmod 400 ~/.ssh/emr-p9-keypair.pem
   ```
7. **Retourner dans l'onglet "Créer un cluster"**
8. **Cliquer sur "Parcourir"** à côté du champ "Paire de clés"
9. **Sélectionner :** `emr-p9-keypair`

**Option 2 : Utiliser une clé existante**

1. Cliquer sur "Parcourir"
2. Sélectionner votre clé existante dans la liste

---

## SECTION 11 : Rôle Identity and Access Management (IAM)

### **Fonction du service Amazon EMR**

1. **Choisir une fonction du service existant** (option de gauche sélectionnée)
2. **Fonction du service :**
   - Cliquer dans le champ "Choisir un rôle IAM"
   - Dans la liste déroulante, chercher : `EMR_DefaultRole_P9`
   - Sélectionner : **EMR_DefaultRole_P9**

### **Profil d'instance EC2 pour Amazon EMR**

1. **Choisir un profil d'instance existant** (option de gauche sélectionnée)
2. **Profil d'instance :**
   - Cliquer dans le champ "Choisir un rôle IAM"
   - Dans la liste, chercher : `EMR_EC2_DefaultRole_P9`
   - Sélectionner : **EMR_EC2_DefaultRole_P9**

### **Rôle d'autoscaling personnalisé**
- ⚠️ **Laisser vide** (facultatif - non nécessaire car pas d'autoscaling)

---

## SECTION 12 : Récapitulatif et Création

### **✅ Checklist Finale - Vérifier TOUS ces points :**

**Nom et applications :**
- ✅ Nom : Fruits-Classification-P9-Cluster
- ✅ Version : emr-7.10.0
- ✅ Applications : Spark Interactive + Core Hadoop

**Configuration cluster :**
- ✅ Primaire (Master) : 1x m6g.xlarge
- ✅ Unité principale (Core) : 1x m6g.xlarge, **Spot activé**
- ✅ Pas de nœuds de tâche (Task)

**Dimensionnement :**
- ✅ Taille manuelle
- ✅ Unité principale : 1 instance, Spot coché

**Réseaux :**
- ✅ VPC par défaut
- ✅ Sous-réseau dans eu-west-1

**Résiliation :**
- ✅ Auto-termination : 3 heures

**Sécurité :**
- ✅ Paire de clés : emr-p9-keypair (ou votre clé)

**IAM :**
- ✅ Fonction du service : EMR_DefaultRole_P9
- ✅ Profil d'instance : EMR_EC2_DefaultRole_P9

### **Créer le Cluster**

1. **Descendre en BAS de la page**
2. **Cliquer sur "Créer un cluster"** (bouton orange)

---

## SECTION 13 : Attente et Vérification

### **Status du Cluster**

**✅ VOUS DEVEZ VOIR :**
- Vous êtes redirigé vers la page du cluster
- **Status : "Starting"** (orange)

**Évolution des status :**
```
Starting (5-7 min)
  ↓
Bootstrapping (3-5 min)
  ↓
Running (1-2 min)
  ↓
Waiting ← ✅ CLUSTER PRÊT quand ce status apparaît
```

⏱️ **Temps total d'attente : 10-15 minutes**

### **Pendant l'Attente**

**Vous pouvez :**
- Rafraîchir la page toutes les 2 minutes (icône refresh)
- Prendre un café ☕
- Lire la Phase 3 du guide principal

**Ne pas :**
- Fermer l'onglet AWS
- Créer un autre cluster
- Modifier les paramètres

### **Quand Status = "Waiting"**

**✅ Cluster prêt ! Vous pouvez passer à :**

1. **Récupérer le DNS Master** (voir ci-dessous)
2. **Configurer Security Group** (voir ci-dessous)
3. **Se connecter à JupyterHub** (Phase 3 du guide principal)

---

## SECTION 14 : Post-Création - DNS et Security Group

### **A. Récupérer le DNS Master**

1. **Sur la page du cluster** (status "Waiting")
2. **Onglet "Résumé"** (déjà sélectionné)
3. **Chercher la ligne :** "DNS public du nœud principal" ou "Master public DNS"
4. **Copier l'adresse** (exemple : `ec2-34-245-xxx-xxx.eu-west-1.compute.amazonaws.com`)
5. **Sauvegarder dans un fichier texte** (vous en aurez besoin pour JupyterHub)

### **B. Configurer Security Group (Ouvrir Port JupyterHub)**

1. **Sur la page du cluster, cliquer sur l'onglet "Sécurité et accès"**
2. **Section "Groupes de sécurité" :**
   - Vous voyez : "Groupe de sécurité du nœud principal" : sg-XXXXXXXXX
3. **Cliquer sur le lien sg-XXXXXXXXX** (lien bleu)
   - Une nouvelle page s'ouvre (EC2 Security Groups)
4. **En bas de la page, onglet "Règles entrantes"**
   - Cliquer sur cet onglet
5. **Cliquer sur "Modifier les règles entrantes"** (bouton à droite)
6. **Cliquer sur "Ajouter une règle"** (bouton en bas)
7. **Remplir la nouvelle règle :**
   - **Type :** Custom TCP
   - **Plage de ports :** `9443`
   - **Source :** My IP (AWS détecte automatiquement votre IP)
   - **Description :** `JupyterHub access`
8. **Cliquer sur "Enregistrer les règles"** (bouton orange)

**✅ VOUS DEVEZ VOIR :**
- Message vert : "Les règles du groupe de sécurité ont bien été modifiées"
- Nouvelle règle dans la liste : TCP 9443 avec votre IP

9. **Fermer cet onglet** et retourner sur la page EMR

---

## SECTION 15 : Validation Finale

### **✅ Checklist Post-Création**

- [ ] Cluster status = "Waiting"
- [ ] DNS Master copié et sauvegardé
- [ ] Security Group configuré (port 9443 ouvert)
- [ ] Paire de clés .pem sauvegardée dans ~/.ssh/
- [ ] Région toujours eu-west-1 ⚠️

**Si tout est coché :** Vous pouvez passer à la Phase 3 (Connexion JupyterHub) du guide principal !

---

## 🆘 Problèmes Fréquents

### **Erreur : "Insufficient capacity"**

**Cause :** Capacité Spot insuffisante en eu-west-1 pour m6g.xlarge

**Solutions :**
1. Réessayer dans 10 minutes (capacité Spot fluctue)
2. Utiliser instances **m5.xlarge** au lieu de m6g.xlarge (x86 au lieu de ARM)
3. Passer en **On-Demand** au lieu de Spot (plus cher : ~1€ au lieu de 0.45€)

### **Erreur : "Invalid IAM Role"**

**Cause :** Rôles IAM non créés ou mal nommés

**Solution :**
1. Vérifier dans IAM → Roles que vous avez bien :
   - EMR_DefaultRole_P9
   - EMR_EC2_DefaultRole_P9
2. Si absents, retourner à Phase 0, Étape 0.4 du guide principal

### **Cluster bloqué sur "Starting"**

**Solutions :**
1. Attendre 15 minutes (parfois AWS est lent)
2. Si toujours bloqué après 20 minutes :
   - Terminer le cluster
   - Vérifier que vous êtes bien en eu-west-1
   - Recréer le cluster

---

## 💰 Estimation Coûts Finale

**Configuration optimisée :**
- Master : 1x m6g.xlarge Spot (~0.081 USD/h)
- Core : 1x m6g.xlarge Spot (~0.081 USD/h)
- **Total : ~0.16 USD/h**

**Pour 3 heures d'utilisation :**
- EMR : 0.48 USD (~0.45€)
- S3 stockage : 0.05 USD (~0.05€)
- S3 transferts : 0.03 USD (~0.03€)
- **Total : ~0.53€** (bien en dessous du budget 10€)

**Économie vs On-Demand :** ~60% de réduction

---

**📌 Félicitations !** Votre cluster EMR est prêt. Passez maintenant à la Phase 3 pour vous connecter à JupyterHub.

**Rappel important :** N'oubliez pas de terminer le cluster après utilisation !
