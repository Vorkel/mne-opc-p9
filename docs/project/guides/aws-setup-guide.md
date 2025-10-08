# Guide AWS - Configuration S3 et Déploiement EMR (Débutant)

**Version :** 2.0 - Guide Ultra-Détaillé pour Débutant AWS
**Date :** 6 octobre 2025
**Objectif :** Guide pas-à-pas ULTRA-PRÉCIS pour configurer AWS et exécuter le notebook EMR
**Public :** Débutant AWS n'ayant jamais utilisé AWS auparavant

---

## Important à Savoir AVANT de Commencer

### WARNINGS CRITIQUES

1. **NE PAS OUBLIER DE TERMINER LE CLUSTER EMR** à la fin → Sinon coûts continuent !
2. **TOUJOURS vérifier que vous êtes en région eu-west-1** (coin haut droit AWS Console)
3. **Configurer les alertes budget** AVANT de créer quoi que ce soit
4. **Sauvegarder le fichier .pem** (clé SSH) dans un endroit sûr (`~/.ssh/`)

### Budget et Coûts

- **Budget maximum :** 10€
- **Coûts estimés réels :** ~1.69€
- **Marge de sécurité :** 8.31€ (83%)

### Temps Estimé Total : ~6 heures

| Phase | Durée | Travail Actif | Attente | Quand faire |
|-------|-------|---------------|---------|-------------|
| Phase 0 : Config initiale | 30 min | 30 min | 0 | Maintenant |
| Phase 1 : S3 + Upload | 2h | 30 min | 1h30 | Lancer upload et faire autre chose |
| Phase 2 : EMR | 1h | 45 min | 15 min | Attendre démarrage cluster |
| Phase 3 : JupyterHub | 15 min | 15 min | 0 | Connexion rapide |
| Phase 4 : Exécution | 2h | 15 min | 1h45 | Lancer pipeline et faire autre chose |
| Phase 5 : Validation | 30 min | 30 min | 0 | Vérifier et TERMINER cluster |
| **TOTAL** | **~6h** | **~3h** | **~3h** | **Peut être fait sur 1-2 jours** |

💡 **Astuce :** Vous pouvez faire autre chose pendant l'upload dataset et l'exécution du notebook

---

## Prérequis - Vérification

### Compte AWS

- [ ] Compte AWS créé sur https://aws.amazon.com
- [ ] Email de confirmation AWS reçu
- [ ] Carte bancaire enregistrée et validée
- [ ] Vous pouvez vous connecter à https://console.aws.amazon.com

### ✅ Environnement Local

- [ ] macOS (vous utilisez un Mac)
- [ ] Terminal accessible : Applications → Utilitaires → Terminal
- [ ] Navigateur : Chrome ou Firefox (recommandé)

### ✅ Fichiers du Projet

- [ ] Dataset Fruits-360 dans `/Users/maximenejad/Developer/OPC/P9/data/raw/fruits-360_dataset/`
- [ ] Notebook PySpark dans `/Users/maximenejad/Developer/OPC/P9/notebook/P8_Notebook_Linux_EMR_PySpark_V1.0.ipynb`

---

## PHASE 0 : Configuration Initiale AWS (30 minutes)

### Étape 0.1 : Première Connexion à AWS Console

**📍 CE QUE VOUS ALLEZ FAIRE :** Se connecter à AWS et sélectionner la bonne région

1. **Ouvrir votre navigateur** (Chrome ou Firefox)
2. **Aller sur :** https://console.aws.amazon.com
3. **Se connecter avec :**
   - Email de votre compte AWS
   - Mot de passe

**✅ VOUS DEVEZ VOIR :** Page d'accueil AWS Console avec :
- Barre noire en haut
- Votre nom en haut à droite
- Barre de recherche au centre
- Plein de carrés avec des icônes (services AWS)

---

### Étape 0.2 : Sélection Région eu-west-1 (RGPD - OBLIGATOIRE)

**📍 ULTRA IMPORTANT - À VÉRIFIER À CHAQUE CONNEXION AWS**

1. **Regarder en HAUT À DROITE** de la page (à côté de votre nom)
2. **Vous voyez un nom de région** avec un drapeau
   - Exemples possibles : "N. Virginia", "Paris", "Ohio", etc.
3. **Cliquer sur ce nom de région**
4. **Une liste déroulante apparaît** avec toutes les régions AWS
5. **Descendre et CHERCHER :** `Europe (Ireland) eu-west-1`
6. **CLIQUER sur :** `Europe (Ireland) eu-west-1`

**✅ VOUS DEVEZ VOIR :** En haut à droite :
- Drapeau de l'Irlande 🇮🇪
- Texte : "Europe (Ireland) eu-west-1" ou juste "eu-west-1"

⚠️ **CRITIQUE :** Vérifier TOUJOURS que vous êtes en `eu-west-1` avant CHAQUE action AWS !
**Pourquoi ?** RGPD - Données doivent rester en Europe

---

### Étape 0.3 : Créer Alerte Budget (Sécurité Anti-Dépassement)

**📍 CE QUE VOUS ALLEZ FAIRE :** Recevoir des emails quand vous approchez 5€, 8€ ou 10€

#### Partie A : Accéder au service Budgets

1. **Dans la barre de recherche** (en haut, au milieu de l'écran) :
   - Cliquer dans la barre
   - Taper : `Budgets`
   - **Attendre 1 seconde** → Des résultats apparaissent

2. **Dans les résultats** :
   - Chercher la ligne "AWS Budgets" (avec icône de calculatrice)
   - Cliquer dessus

**✅ VOUS DEVEZ VOIR :**
- Page "AWS Budgets"
- Bouton orange "Create budget" en haut à droite

#### Partie B : Créer le budget avec 3 alertes

3. **Cliquer sur "Create budget"** (bouton orange)

4. **Page "Select budget type" :**
   - **Vous voyez plusieurs options** (Cost, Usage, etc.)
   - **Vérifier que "Cost budget" est coché** (normalement oui par défaut)
   - **Cliquer sur "Next"** (bouton orange en bas à droite)

5. **Page "Set budget amount" :**
   Remplir les champs suivants :

   - **Budget name :**
     - Cliquer dans le champ
     - Taper : `P9-Fruits-Budget`

   - **Period :**
     - Cliquer sur le menu déroulant
     - Sélectionner : **"Monthly"**

   - **Budgeting method :**
     - Sélectionner : **"Fixed"**

   - **Enter your budgeted amount ($) :**
     - Cliquer dans le champ
     - Taper : `10`
     - ⚠️ Note : Même si compte en EUR, AWS affiche USD. 10 USD ≈ 10 EUR

   - **Cliquer sur "Next"** (bas de page)

6. **Page "Configure alerts" :**

   **ALERTE 1 - À 5€ (50%) :**
   - Cliquer sur bouton **"Add an alert threshold"**
   - **Threshold :** Taper `5`
   - **Email recipients :** Taper votre adresse email
   - Cliquer à nouveau sur **"Add an alert threshold"** (pour ajouter alerte 2)

   **ALERTE 2 - À 8€ (80%) :**
   - **Threshold :** Taper `8`
   - **Email recipients :** (déjà rempli avec votre email)
   - Cliquer une 3ème fois sur **"Add an alert threshold"**

   **ALERTE 3 - À 10€ (100%) :**
   - **Threshold :** Taper `10`
   - **Email recipients :** (déjà rempli)

   - **Cliquer sur "Next"**

7. **Page "Attach actions" (OPTIONNEL) :**
   - Vous pouvez ignorer cette page
   - **Cliquer sur "Next"**

8. **Page "Review" :**
   - **Vérifier que tout est correct :**
     - Budget name : P9-Fruits-Budget
     - Amount : $10
     - 3 alertes : $5, $8, $10
   - **Cliquer sur "Create budget"** (bouton orange)

**✅ VOUS DEVEZ VOIR :**
- Message vert en haut : "Budget P9-Fruits-Budget created successfully"
- Votre budget apparaît dans la liste

**📧 RÉSULTAT :**
- Vous recevrez 3 emails de confirmation d'AWS
- Vous recevrez ensuite un email chaque fois que vous dépensez 5€, 8€ ou 10€

---

### Étape 0.4 : Créer Rôles IAM (Permissions)

**📍 CE QUE VOUS ALLEZ FAIRE :** Créer 2 "rôles" (= permissions) pour permettre à EMR d'utiliser S3

#### Partie A : Accéder à IAM

1. **Dans la barre de recherche** (en haut), taper : `IAM`
2. **Cliquer sur "IAM"** dans les résultats

**✅ VOUS DEVEZ VOIR :**
- Page "IAM Dashboard"
- Menu à gauche avec plein d'options
- Panneau central avec des statistiques

#### Partie B : Créer le 1er Rôle (Pour le Service EMR)

3. **Dans le menu de GAUCHE**, chercher et cliquer sur **"Roles"**

**✅ VOUS DEVEZ VOIR :**
- Page "Roles"
- Liste de rôles (peut être vide si nouveau compte)
- Bouton orange "Create role" en haut à droite

4. **Cliquer sur "Create role"** (bouton orange)

5. **Page "Select trusted entity" :**

   - **Trusted entity type :**
     - Vérifier que **"AWS service"** est sélectionné (normalement oui)

   - **Use case :**
     - Vous voyez une liste déroulante avec EC2, Lambda, etc.
     - **Chercher dans la liste : "EMR"**
     - **Cliquer sur "EMR"**
     - Puis en dessous, **sélectionner "EMR"** (PAS "EMR Notebooks" ni "EMR Serverless")

   - **Cliquer sur "Next"**

6. **Page "Add permissions" :**

   - Vous voyez une **barre de recherche** et une liste de "policies"

   **Ajouter la 1ère permission :**
   - Dans la barre de recherche, taper : `AmazonEMRServicePolicy_v2`
   - Dans les résultats, **cocher la case** à côté de `AmazonEMRServicePolicy_v2`

   **Ajouter la 2ème permission :**
   - **Effacer** la barre de recherche
   - Taper : `AmazonS3FullAccess`
   - **Cocher la case** à côté de `AmazonS3FullAccess`

   **✅ VÉRIFICATION :** Vous devez avoir 2 policies cochées :
   - AmazonEMRServicePolicy_v2
   - AmazonS3FullAccess

   - **Cliquer sur "Next"**

7. **Page "Name, review, and create" :**

   - **Role name :**
     - Cliquer dans le champ
     - Taper EXACTEMENT : `EMR_DefaultRole_P9`
     - ⚠️ Important : Respecter majuscules/minuscules et underscores

   - **Description (optionnel) :**
     - Taper : `Role for EMR cluster P9 project`

   - **Descendre en bas de la page**
   - **Cliquer sur "Create role"** (bouton orange)

**✅ VOUS DEVEZ VOIR :**
- Message vert : "Role EMR_DefaultRole_P9 created successfully"
- Vous êtes de retour sur la page "Roles"
- Le rôle `EMR_DefaultRole_P9` apparaît dans la liste

#### Partie C : Créer le 2ème Rôle (Pour les Instances EC2 d'EMR)

8. **Cliquer à nouveau sur "Create role"** (bouton orange en haut)

9. **Page "Select trusted entity" :**

   - **Trusted entity type :** **"AWS service"** (déjà sélectionné)

   - **Use case :**
     - Chercher dans la liste : **"EC2"**
     - **Cliquer sur "EC2"**

   - **Cliquer sur "Next"**

10. **Page "Add permissions" :**

    **Ajouter la 1ère permission :**
    - Dans la barre de recherche, taper : `AmazonS3FullAccess`
    - **Cocher** `AmazonS3FullAccess`

    **Ajouter la 2ème permission :**
    - Effacer la barre et taper : `AmazonElasticMapReduceforEC2Role`
    - **Cocher** `AmazonElasticMapReduceforEC2Role`

    **✅ VÉRIFICATION :** 2 policies cochées :
    - AmazonS3FullAccess
    - AmazonElasticMapReduceforEC2Role

    - **Cliquer sur "Next"**

11. **Page "Name, review, and create" :**

    - **Role name :** Taper EXACTEMENT : `EMR_EC2_DefaultRole_P9`
    - **Description :** `Role for EMR EC2 instances P9`
    - **Cliquer sur "Create role"**

**✅ VOUS DEVEZ VOIR :**
- Message vert : "Role EMR_EC2_DefaultRole_P9 created successfully"
- Dans la liste des rôles, vous avez maintenant :
  - `EMR_DefaultRole_P9`
  - `EMR_EC2_DefaultRole_P9`

**📌 PHASE 0 TERMINÉE !**
- ✅ Budget avec 3 alertes configuré
- ✅ 2 rôles IAM créés
- ✅ Région eu-west-1 sélectionnée

**⏸️ PAUSE POSSIBLE :** Vous pouvez faire une pause ici et revenir plus tard

---

## PHASE 1 : Création Bucket S3 et Upload Dataset (2 heures)

**⏱️ Temps actif : 30 min | Temps attente : 1h30 (upload)**

### Étape 1.1 : Créer le Bucket S3

**📍 CE QUE VOUS ALLEZ FAIRE :** Créer un "bucket" (= dossier cloud) pour stocker vos données

#### Partie A : Accéder à S3

1. **Vérifier région :** En haut à droite → doit afficher **eu-west-1** ⚠️
2. **Barre de recherche** (en haut) : Taper `S3`
3. **Cliquer sur "S3"** dans les résultats

**✅ VOUS DEVEZ VOIR :**
- Page "Amazon S3"
- Texte "Buckets" à gauche
- Bouton orange "Create bucket" à droite

#### Partie B : Créer le bucket

4. **Cliquer sur "Create bucket"** (bouton orange)

5. **Page "Create bucket" - Remplir les champs :**

   **General configuration :**

   - **Bucket name :**
     - Taper : `fruits-classification-p9-maxime`
     - ⚠️ Remplacer "maxime" par VOTRE prénom (en minuscules)
     - ⚠️ Le nom doit être UNIQUE au monde (AWS dira si déjà pris)
     - Exemples valides : `fruits-classification-p9-john`, `fruits-classification-p9-marie`

   - **AWS Region :**
     - **VÉRIFIER que c'est bien :** `EU (Ireland) eu-west-1`
     - ⚠️ Si ce n'est pas eu-west-1, cliquer sur le menu déroulant et sélectionner `EU (Ireland) eu-west-1`

   **Object Ownership :**
   - Laisser **"ACLs disabled (recommended)"** (déjà sélectionné)

   **Block Public Access settings for this bucket :**
   - **IMPORTANT :** Vérifier que **"Block all public access"** est COCHÉ ✅
   - (Sécurité : empêche accès public à vos données)

   **Bucket Versioning :**
   - Laisser **"Disable"** (économie de coûts)

   **Encryption :**
   - Laisser **"Server-side encryption with Amazon S3 managed keys (SSE-S3)"** (déjà sélectionné)

   **Descendre en bas de la page**

   - **Cliquer sur "Create bucket"** (bouton orange)

**✅ VOUS DEVEZ VOIR :**
- Message vert : "Successfully created bucket fruits-classification-p9-maxime"
- Votre bucket apparaît dans la liste des buckets

---

### Étape 1.2 : Créer la Structure de Dossiers dans S3

**📍 CE QUE VOUS ALLEZ FAIRE :** Créer 3 dossiers : dataset, notebooks, results

1. **Dans la liste des buckets**, **cliquer sur le nom de votre bucket** : `fruits-classification-p9-maxime`

**✅ VOUS DEVEZ VOIR :**
- Page du bucket (vide pour l'instant)
- Boutons en haut : "Upload", "Create folder", etc.

#### Créer le dossier "Test" (données d'entrée)

2. **Cliquer sur "Create folder"**
3. **Folder name :** Taper `Test`
4. **Cliquer sur "Create folder"** (bouton orange en bas)

**✅ VOUS DEVEZ VOIR :**
- Message vert : "Successfully created folder Test/"
- Dossier "Test/" apparaît dans la liste

#### Créer le dossier "Results" (données de sortie)

5. **Cliquer sur "Create folder"** (à nouveau)
6. **Folder name :** Taper `Results`
7. **Cliquer sur "Create folder"**

**✅ VÉRIFICATION FINALE :** Structure créée :
```
fruits-classification-p9-maxime/
├── Test/
└── Results/
```

8. **Revenir à la racine du bucket :**
    - En haut de la page, cliquer sur le nom du bucket : `fruits-classification-p9-maxime`

---

### Étape 1.3 : Installer et Configurer AWS CLI (Pour Upload Dataset)

**📍 CE QUE VOUS ALLEZ FAIRE :** Installer l'outil ligne de commande AWS pour uploader rapidement les 87k images

#### Partie A : Installer AWS CLI sur Mac

1. **Ouvrir Terminal** : Applications → Utilitaires → Terminal

2. **Vérifier si AWS CLI déjà installé :**
   ```bash
   aws --version
   ```

   **Si vous voyez :** `aws-cli/2.x.x` → AWS CLI déjà installé, passez à Partie B

   **Si vous voyez :** `command not found` → Continuer ci-dessous

3. **Installer AWS CLI avec Homebrew :**
   ```bash
   # Si vous n'avez pas Homebrew, l'installer d'abord :
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

   # Puis installer AWS CLI :
   brew install awscli
   ```

   ⏱️ Attendre 2-3 minutes

4. **Vérifier installation :**
   ```bash
   aws --version
   ```

   **✅ VOUS DEVEZ VOIR :** `aws-cli/2.x.x Python/3.x.x Darwin/...`

#### Partie B : Obtenir vos Access Keys AWS

**📍 CE QU'IL VOUS FAUT :** 2 clés pour que AWS CLI puisse accéder à votre compte

1. **Retourner dans AWS Console** (navigateur)

2. **En haut à DROITE**, cliquer sur **votre nom de compte**
   - Un menu déroulant apparaît

3. **Cliquer sur "Security credentials"**

**✅ VOUS DEVEZ VOIR :**
- Page "My Security Credentials"
- Section "Access keys"

4. **Descendre jusqu'à la section "Access keys"**

5. **Cliquer sur "Create access key"** (bouton orange)

6. **Page "Access key best practices & alternatives" :**
   - Sélectionner : **"Command Line Interface (CLI)"**
   - **Cocher** la case : "I understand the above recommendation..."
   - **Cliquer sur "Next"**

7. **Page "Set description tag" (optionnel) :**
   - Description : Taper `P9 Project CLI Access`
   - **Cliquer sur "Create access key"**

8. **Page "Retrieve access keys" - IMPORTANT :**

   **✅ VOUS DEVEZ VOIR :**
   - **Access key** : Quelque chose comme `AKIAIOSFODNN7EXAMPLE`
   - **Secret access key** : Quelque chose comme `wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY`

   ⚠️ **CRITIQUE :** Ces clés ne seront affichées qu'UNE SEULE FOIS !

   **FAIRE IMMÉDIATEMENT :**
   - **Cliquer sur "Download .csv file"** → Sauvegarder sur votre Mac
   - OU **noter les clés** quelque part de sûr (TextEdit, Notes, etc.)

   - **Cliquer sur "Done"**

#### Partie C : Configurer AWS CLI

9. **Retourner dans Terminal**

10. **Configurer AWS CLI :**
    ```bash
    aws configure
    ```

11. **AWS CLI va vous poser 4 questions - Répondre :**

    ```
    AWS Access Key ID [None]: [COLLER votre Access Key]
    AWS Secret Access Key [None]: [COLLER votre Secret Access Key]
    Default region name [None]: eu-west-1
    Default output format [None]: json
    ```

    **Appuyer sur ENTRÉE après chaque ligne**

**✅ VOUS DEVEZ VOIR :** Le curseur revient (pas de message d'erreur = OK)

12. **Tester la configuration :**
    ```bash
    aws s3 ls
    ```

    **✅ VOUS DEVEZ VOIR :**
    - La liste de vos buckets S3
    - Au minimum : `fruits-classification-p9-maxime`

**Si vous voyez une erreur :** Vérifier que vous avez bien copié les 2 clés

---

### Étape 1.4 : Uploader le Dataset sur S3 (1-2 heures)

**📍 CE QUE VOUS ALLEZ FAIRE :** Uploader les 67 000 images (~2GB) sur S3

**⚠️ IMPORTANT :** Cette étape prend 1-2 heures. Vous pouvez lancer l'upload et faire autre chose.

#### Option A : Upload via AWS CLI (RECOMMANDÉ - Plus rapide)

1. **Dans Terminal, aller dans le dossier du projet :**
   ```bash
   cd /Users/maximenejad/Developer/OPC/P9
   ```

2. **Vérifier que le dataset existe :**
   ```bash
   ls -la data/raw/fruits-360_dataset/fruits-360/Training/ | head
   ```

   **✅ VOUS DEVEZ VOIR :** Liste de dossiers (Apple Braeburn 1, Apple Crimson Snow, etc.)

3. **Uploader le dataset Training sur S3 :**

   **⚠️ Remplacer "maxime" par VOTRE prénom dans la commande ci-dessous :**

   ```bash
   aws s3 sync ./data/raw/fruits-360_dataset/fruits-360/Training/ \
     s3://fruits-classification-p9-maxime/Test/ \
     --region eu-west-1
   ```

   **Appuyer sur ENTRÉE**

**✅ VOUS DEVEZ VOIR :**
- Plein de lignes défilent : `upload: ...` avec noms de fichiers
- Exemple : `upload: data/raw/.../Apple_Braeburn_1/0_100.jpg to s3://...`

⏱️ **TEMPS D'ATTENTE : 30-60 minutes**

💡 **ASTUCE :** Vous pouvez faire autre chose pendant ce temps. Laissez le Terminal ouvert et actif.

4. **Quand l'upload est terminé :**

   **✅ VOUS DEVEZ VOIR :** Le curseur revient (plus de lignes qui défilent)

5. **Vérifier que l'upload a fonctionné :**
   ```bash
   aws s3 ls s3://fruits-classification-p9-maxime/Test/ --recursive | wc -l
   ```

   **✅ VOUS DEVEZ VOIR :** Un nombre proche de `67000` (nombre d'images Training)

**FÉLICITATIONS !** Dataset uploadé sur S3 ✅

#### Option B : Upload via AWS Console (Plus lent - 2-3 heures)

**Si AWS CLI ne fonctionne pas, utiliser l'interface web :**

1. **AWS Console → S3 → Votre bucket → Test/**
2. **Cliquer "Upload"**
3. **Cliquer "Add folder"**
4. **Sélectionner :** `data/raw/fruits-360_dataset/fruits-360/Training`
5. **Cliquer "Upload"**
6. ⏱️ Attendre 2-3 heures

---

**📌 PHASE 1 TERMINÉE !**
- ✅ Bucket S3 créé dans eu-west-1
- ✅ Structure de dossiers créée
- ✅ Dataset uploadé sur S3 (67k images)
- ✅ AWS CLI configuré

**⏸️ PAUSE RECOMMANDÉE :** Bon moment pour faire une pause (30 min - 1 jour)

---

## PHASE 2 : Création Cluster EMR (1 heure)

**⏱️ Temps actif : 45 min | Temps attente : 15 min (démarrage cluster)**

### Étape 2.1 : Créer le Cluster EMR

**📍 CE QUE VOUS ALLEZ FAIRE :** Créer un "cluster" (= plusieurs ordinateurs) pour faire les calculs Big Data

#### Partie A : Accéder au service EMR

1. **Vérifier région :** En haut à droite → **eu-west-1** ⚠️
2. **Barre de recherche** : Taper `EMR`
3. **Cliquer sur "EMR"**

**✅ VOUS DEVEZ VOIR :**
- Page "Amazon EMR"
- Texte "Clusters" à gauche
- Bouton orange "Create cluster" à droite

4. **Cliquer sur "Create cluster"**

#### Partie B : Configuration du Cluster - SOFTWARE

**✅ VOUS DEVEZ VOIR :** Page "Create Cluster" avec plein d'options

5. **Section "General Configuration" :**

   - **Cluster name :**
     - Taper : `Fruits-Classification-P9-Cluster`

   - **Amazon EMR release :**
     - Dans le menu déroulant, sélectionner : **emr-6.15.0** (ou dernière version 6.x)

6. **Section "Application bundle" :**

   - **Sélectionner : "Custom"**

   - **Dans la liste des applications, COCHER :**
     - ✅ **Spark**
     - ✅ **JupyterEnterpriseGateway**
     - ✅ **Hadoop**

   - **NE PAS cocher :** Hive, Presto, etc. (pas nécessaires)

#### Partie C : Configuration du Cluster - HARDWARE

7. **Section "Cluster configuration" :**

   **Instance groups (Uniform instance groups) - Laisser sélectionné**

   **Primary (Master) node :**
   - **Instance type :**
     - Cliquer sur le menu déroulant
     - Chercher : `m6g.xlarge` (ou `m5.xlarge` si m6g pas disponible)
     - Sélectionner : **m6g.xlarge**

   - **Instance count :** `1` (déjà rempli)

   - **Instance purchasing option :**
     - **Sélectionner : "Spot"** ⚠️ IMPORTANT (économise 70-90%)

   **Core nodes :**
   - **Instance type :**
     - Sélectionner : **m6g.large** (ou `m5.large`)

   - **Instance count :** `2`

   - **Instance purchasing option :**
     - **Sélectionner : "Spot"** ⚠️ IMPORTANT

**💰 VÉRIFICATION COÛTS :**
- En haut de la page, vous devriez voir : "Estimated cost: $X.XX/hour"
- Doit être environ : **$0.35-0.40/hour** (avec Spot)
- Pour 3 heures : ~1€

#### Partie D : Configuration - NETWORKING

8. **Section "Networking" :**

   - **Amazon VPC :**
     - Laisser : **"Default VPC"** (déjà sélectionné)

   - **Subnet :**
     - Laisser : (n'importe quel subnet eu-west-1a, b ou c)

9. **Section "Cluster termination and node replacement" :**

   - **Termination protection :**
     - **DÉCOCHER** ❌ (Important pour pouvoir terminer le cluster)

   - **Cluster auto-termination :**
     - **COCHER** ✅ "Use cluster auto-termination"
     - **Idle time :** Taper `3` (heures)
     - *(Le cluster s'éteindra automatiquement après 3h d'inactivité)*

#### Partie E : Configuration - SECURITY

10. **Section "Security configuration and EC2 key pair" :**

    **EC2 key pair :**

    **Option 1 : Créer une nouvelle clé (RECOMMANDÉ) :**
    - Cliquer sur **"Create new EC2 key pair"** (lien bleu)
    - **Une nouvelle fenêtre s'ouvre**
    - **Key pair name :** Taper `emr-p9-keypair`
    - **Key pair type :** Laisser **RSA**
    - **Private key file format :** Laisser **.pem**
    - **Cliquer sur "Create key pair"**
    - **⚠️ IMPORTANT :** Le fichier `emr-p9-keypair.pem` se télécharge
    - **SAUVEGARDER ce fichier** dans `~/.ssh/` sur votre Mac :
      ```bash
      # Dans Terminal :
      mv ~/Downloads/emr-p9-keypair.pem ~/.ssh/
      chmod 400 ~/.ssh/emr-p9-keypair.pem
      ```
    - **Retourner dans la fenêtre AWS** (l'autre onglet)
    - **Rafraîchir la liste** : Cliquer sur l'icône "rafraîchir" à côté du menu
    - **Sélectionner :** `emr-p9-keypair`

    **Option 2 : Sélectionner une clé existante (si vous en avez déjà) :**
    - Dans le menu déroulant, sélectionner votre clé existante

11. **Section "Identity and Access Management (IAM) roles" :**

    - **Amazon EMR service role :**
      - Dans le menu déroulant, chercher et sélectionner : **EMR_DefaultRole_P9**

    - **EC2 instance profile for Amazon EMR :**
      - Dans le menu déroulant, chercher et sélectionner : **EMR_EC2_DefaultRole_P9**

**✅ VÉRIFICATION AVANT CRÉATION :**
- Cluster name : Fruits-Classification-P9-Cluster
- EMR release : emr-6.15.0
- Applications : Spark, JupyterEnterpriseGateway, Hadoop
- Master : 1x m6g.xlarge Spot
- Core : 2x m6g.large Spot
- Termination protection : OFF
- Auto-termination : 3 hours
- EC2 key pair : emr-p9-keypair
- IAM roles : EMR_DefaultRole_P9 et EMR_EC2_DefaultRole_P9

#### Partie F : Lancer la Création

12. **Descendre en BAS de la page**

13. **Cliquer sur "Create cluster"** (bouton orange)

**✅ VOUS DEVEZ VOIR :**
- Vous êtes redirigé vers la page du cluster
- **Status : "Starting"** (en orange)

⏱️ **ATTENDRE 10-15 minutes** pour que le cluster démarre

**Statuts successifs :**
- Starting (5 min)
- Bootstrapping (5 min)
- Running (1 min)
- **Waiting** ← ✅ Cluster prêt quand ce statut apparaît

💡 **PENDANT L'ATTENTE :** Vous pouvez rafraîchir la page toutes les 2 minutes pour voir l'évolution

**✅ QUAND STATUS = "WAITING" :** Cluster prêt ! Passez à l'étape suivante

---

### Étape 2.2 : Noter le DNS Master et Configurer Security Group

**📍 CE QUE VOUS ALLEZ FAIRE :** Récupérer l'adresse du cluster et ouvrir le port pour JupyterHub

#### Partie A : Récupérer le DNS Master

1. **Vous êtes sur la page du cluster** (status "Waiting")

2. **Dans l'onglet "Summary" :**
   - Chercher la ligne : **"Master public DNS"**
   - Vous voyez quelque chose comme : `ec2-34-245-XXX-XXX.eu-west-1.compute.amazonaws.com`

3. **COPIER cette adresse** (sélectionner et Cmd+C)

4. **SAUVEGARDER cette adresse** dans un fichier texte (vous en aurez besoin plus tard)

#### Partie B : Configurer Security Group (Ouvrir port JupyterHub)

5. **Sur la même page, chercher l'onglet "Security and access"**
   - Cliquer sur cet onglet

6. **Vous voyez une section "Security groups" avec :**
   - Security group for Primary (Master) : sg-XXXXXXXXX

7. **Cliquer sur le lien du Security group du Master** (sg-XXXXXXXXX en bleu)

   **Une nouvelle page s'ouvre** : EC2 Security Groups

8. **En bas de la page, onglet "Inbound rules" :**
   - Cliquer sur l'onglet **"Inbound rules"**

9. **Cliquer sur "Edit inbound rules"** (bouton à droite)

10. **Page "Edit inbound rules" :**

    - **Cliquer sur "Add rule"** (bouton en bas à gauche)

    **Nouvelle règle apparaît :**
    - **Type :** Sélectionner **"Custom TCP"**
    - **Port range :** Taper `9443`
    - **Source :** Sélectionner **"My IP"** (AWS détecte automatiquement votre IP)
    - **Description :** Taper `JupyterHub access`

    - **Cliquer sur "Save rules"** (bouton orange en bas à droite)

**✅ VOUS DEVEZ VOIR :**
- Message vert : "Security group rules modified successfully"
- Nouvelle règle dans la liste : TCP 9443 avec votre IP

11. **Fermer cet onglet** et **retourner sur la page EMR**

**📌 PHASE 2 TERMINÉE !**
- ✅ Cluster EMR créé (Spot + Graviton2)
- ✅ Status : Waiting (prêt à utiliser)
- ✅ DNS Master récupéré
- ✅ Port 9443 ouvert pour JupyterHub

**⏸️ PAUSE POSSIBLE :** Cluster actif, vous pouvez faire une pause de 30 min max

---

## PHASE 3 : Connexion JupyterHub (15 minutes)

**⏱️ Temps actif : 15 min | Temps attente : 0**

### Étape 3.1 : Se Connecter à JupyterHub EMR

**📍 CE QUE VOUS ALLEZ FAIRE :** Ouvrir JupyterHub qui tourne sur le cluster EMR

1. **Ouvrir un NOUVEL onglet** dans votre navigateur

2. **Dans la barre d'adresse, taper :**

   ```
   https://[VOTRE-DNS-MASTER]:9443
   ```

   **⚠️ Remplacer `[VOTRE-DNS-MASTER]` par le DNS que vous avez copié**

   **Exemple :**
   ```
   https://ec2-34-245-123-456.eu-west-1.compute.amazonaws.com:9443
   ```

   **Appuyer sur ENTRÉE**

3. **⚠️ AVERTISSEMENT SÉCURITÉ :**

   **Vous voyez : "Your connection is not private" ou "Connexion non sécurisée"**

   **C'est NORMAL** (certificat auto-signé par AWS)

   **CHROME :**
   - Cliquer sur **"Advanced"** (ou "Paramètres avancés")
   - Cliquer sur **"Proceed to XXX (unsafe)"**

   **FIREFOX :**
   - Cliquer sur **"Advanced"**
   - Cliquer sur **"Accept the Risk and Continue"**

4. **Page de LOGIN JupyterHub :**

   **✅ VOUS DEVEZ VOIR :**
   - Logo Jupyter
   - 2 champs : Username et Password
   - Bouton "Sign in"

   **Remplir :**
   - **Username :** Taper `jovyan` (nom par défaut EMR)
   - **Password :** Taper `jupyter` (mot de passe par défaut EMR)

   **Cliquer sur "Sign in"**

**✅ VOUS DEVEZ VOIR :**
- Interface JupyterHub
- Liste de fichiers (peut être vide)
- Boutons en haut : "Upload", "New", etc.

**FÉLICITATIONS !** Vous êtes connecté à JupyterHub sur EMR ✅

---

### Étape 3.2 : Tester l'Environnement

**📍 CE QUE VOUS ALLEZ FAIRE :** Vérifier que Spark et TensorFlow fonctionnent

1. **Cliquer sur "New"** (en haut à droite)
2. **Sélectionner :** **"Python 3"** ou **"PySpark"**

**Un nouveau notebook s'ouvre**

3. **Dans la première cellule, taper :**

   ```python
   import pyspark
   print(f"PySpark version: {pyspark.__version__}")

   import tensorflow as tf
   print(f"TensorFlow version: {tf.__version__}")

   from pyspark.sql import SparkSession
   spark = SparkSession.builder.appName("P9-Test").getOrCreate()
   print("Spark session créée ✅")
   ```

4. **Exécuter la cellule :**
   - Appuyer sur **Shift + Entrée**

⏱️ Attendre 10-30 secondes

**✅ VOUS DEVEZ VOIR :**
```
PySpark version: 3.4.x
TensorFlow version: 2.5.x
Spark session créée ✅
```

**Si vous voyez des erreurs :** Vérifier que le cluster est bien en status "Waiting"

5. **Tester accès S3 :**

   **⚠️ Remplacer "maxime" par VOTRE prénom dans la commande ci-dessous :**

   ```python
   # Tester lecture S3
   df = spark.read.format("image").load("s3://fruits-classification-p9-maxime/Test/Apple*/")
   print(f"Images chargées: {df.count()}")
   ```

   **Exécuter : Shift + Entrée**

⏱️ Attendre 30-60 secondes

**✅ VOUS DEVEZ VOIR :**
```
Images chargées: XXXX (nombre d'images Apple)
```

**PARFAIT !** Tout fonctionne ✅

6. **Fermer ce notebook de test** (ne pas sauvegarder)

**📌 PHASE 3 TERMINÉE !**
- ✅ JupyterHub accessible
- ✅ PySpark fonctionne
- ✅ TensorFlow fonctionne
- ✅ Accès S3 fonctionne

---

## PHASE 4 : Exécution du Notebook PySpark (2 heures)

**⏱️ Temps actif : 15 min | Temps attente : 1h45 (calculs)**

### Étape 4.1 : Uploader le Notebook sur JupyterHub

**📍 CE QUE VOUS ALLEZ FAIRE :** Uploader votre notebook PySpark modifié

1. **Dans JupyterHub, cliquer sur "Upload"** (bouton en haut à droite)

2. **Dans la fenêtre qui s'ouvre :**
   - Naviguer vers : `/Users/maximenejad/Developer/OPC/P9/notebook/`
   - Sélectionner : `P8_Notebook_Linux_EMR_PySpark_V1.0.ipynb`
   - **Cliquer sur "Open"** (ou "Ouvrir")

3. **Le fichier apparaît dans la liste avec un bouton bleu "Upload"**
   - **Cliquer sur le bouton bleu "Upload"**

⏱️ Attendre 5-10 secondes

**✅ VOUS DEVEZ VOIR :**
- Notebook apparaît dans la liste : `P8_Notebook_Linux_EMR_PySpark_V1.0.ipynb`

4. **Cliquer sur le nom du notebook** pour l'ouvrir

**✅ VOUS DEVEZ VOIR :**
- Notebook s'ouvre
- Plein de cellules de code et markdown
- Titre : "Déployez un modèle dans le cloud"

---

### Étape 4.2 : Configurer les Chemins S3 dans le Notebook

**📍 CE QUE VOUS ALLEZ FAIRE :** Modifier les chemins pour pointer vers votre bucket S3

1. **Chercher la section cloud (vers cellule 60+) :**
   - Défiler vers le bas
   - Chercher : **"4.10.4 Définition des PATH"**

2. **Dans cette section, vous voyez du code comme :**

   ```python
   PATH = 's3://p8-data'
   PATH_Data = PATH+'/Test'
   PATH_Result = PATH+'/Results'
   ```

3. **REMPLACER uniquement la ligne PATH par :**

   **⚠️ Remplacer "maxime" par VOTRE prénom :**

   ```python
   PATH = 's3://fruits-classification-p9-maxime'
   PATH_Data = PATH+'/Test'
   PATH_Result = PATH+'/Results'

   print('PATH:        '+\
         PATH+'\nPATH_Data:   '+\
         PATH_Data+'\nPATH_Result: '+PATH_Result)
   ```

4. **Sauvegarder le notebook :**
   - Menu : File → Save
   - Ou : Cmd+S (Mac)

---

### Étape 4.3 : Exécuter le Pipeline Complet

**📍 CE QUE VOUS ALLEZ FAIRE :** Lancer tous les calculs (35-60 min)

**⚠️ IMPORTANT :** Exécuter les cellules de la SECTION CLOUD uniquement (à partir de la cellule ~57)

#### Ordre d'exécution :

1. **Cellule INSTALLATION PACKAGES (Section cloud - 4.10.2) :**
   - Chercher la cellule avec : `!pip install Pandas pillow tensorflow pyspark pyarrow`
   - **Cliquer sur la cellule**
   - **Shift + Entrée** pour exécuter
   - ⏱️ **Attendre 2-3 minutes** (installation TensorFlow)
   - **✅ Vérifier :** Message "Successfully installed tensorflow-2.5.0..."

1bis. **Cellule IMPORTS (Section cloud - 4.10.3) :**
   - Chercher la cellule avec tous les imports (gzip, pickle, PySpark ML, etc.)
   - **Cliquer sur la cellule**
   - **Shift + Entrée** pour exécuter
   - **✅ Vérifier :** Aucune erreur d'import

2. **Cellule SPARK SESSION :**
   - Normalement déjà créée par EMR
   - Si vous voyez `spark = SparkSession.builder...` → Exécuter
   - **✅ Vérifier :** Message "Spark session created"

3. **Cellule CHARGEMENT DATASET :**
   - `df = spark.read.format("image").load(PATH_Data)`
   - **Exécuter**
   - ⏱️ Attendre 2-5 minutes
   - **✅ Vérifier :** `df.count()` affiche nombre d'images

4. **Cellule PREPROCESSING :**
   - Normalisation des images
   - **Exécuter**
   - ⏱️ Attendre 1-2 minutes

5. **Cellule BROADCAST TENSORFLOW :**
   - Compression + diffusion des poids
   - **Exécuter**
   - **✅ Vérifier :** Messages "Compression: XXX → YYY bytes" et "Broadcast créé ✅"

6. **Cellule FEATURE EXTRACTION :**
   - `df_features = df.withColumn('features', predict_batch_udf(col('image')))`
   - **Exécuter**
   - ⏱️ **ATTENDRE 30-40 MINUTES** (le plus long)
   - **✅ Vérifier :** Barre de progression Spark (apparaît en bas)

**💡 PENDANT L'ATTENTE :** Vous pouvez faire autre chose, laisser l'onglet ouvert

7. **Cellule PCA PYSPARK :**
   - Réduction de dimension 1280 → 256
   - **Exécuter**
   - ⏱️ Attendre 5-10 minutes
   - **✅ Vérifier :** Message "Variance expliquée: XX%" (doit être ≥ 90%)

8. **Cellule SAUVEGARDE S3 :**
   - `save_pca_results(df_pca, pca_output_path)`
   - **Exécuter**
   - ⏱️ Attendre 5 minutes
   - **✅ Vérifier :** Message "✅ Sauvegarde terminée"

**⏱️ DURÉE TOTALE : 35-60 minutes**

---

### Étape 4.4 : Capturer des Screenshots (Pour Présentation)

**📍 CE QUE VOUS ALLEZ FAIRE :** Prendre des photos d'écran pour votre soutenance

**PENDANT l'exécution du notebook, capturer :**

1. **Screenshot AWS EMR Console :**
   - Retourner sur la page EMR dans AWS Console
   - Cluster status "Waiting" ou "Running"
   - **Cmd + Shift + 4** (Mac) → Capturer la page
   - Sauvegarder dans `~/Desktop/`

2. **Screenshot JupyterHub :**
   - Page JupyterHub avec notebook en exécution
   - Montrer les cellules et les outputs
   - **Cmd + Shift + 4**

3. **Screenshot Cellule PCA :**
   - Quand la cellule PCA affiche "Variance expliquée: XX%"
   - **Cmd + Shift + 4**

4. **Screenshot S3 Bucket :**
   - AWS Console → S3 → Votre bucket → Results/pca_output/
   - Montrer les fichiers .parquet créés
   - **Cmd + Shift + 4**

**Sauvegarder tous les screenshots** dans un dossier pour la présentation

**📌 PHASE 4 TERMINÉE !**
- ✅ Notebook uploadé sur JupyterHub
- ✅ Chemins S3 configurés
- ✅ Pipeline exécuté avec succès
- ✅ PCA : Variance ≥ 90% validée
- ✅ Résultats sauvegardés sur S3
- ✅ Screenshots capturés

---

## PHASE 5 : Validation et Terminaison (30 minutes)

**⏱️ Temps actif : 30 min | Temps attente : 0**

### Étape 5.1 : Vérifier les Résultats sur S3

**📍 CE QUE VOUS ALLEZ FAIRE :** Vérifier que les fichiers PCA sont bien sur S3

1. **Ouvrir Terminal sur votre Mac**

2. **Lister les résultats PCA sur S3 :**

   **⚠️ Remplacer "maxime" par VOTRE prénom :**

   ```bash
   aws s3 ls s3://fruits-classification-p9-maxime/Results/pca_output/ --recursive
   ```

**✅ VOUS DEVEZ VOIR :**
- Plein de fichiers `.parquet` :
  ```
  part-00000-XXX.parquet
  part-00001-XXX.parquet
  ...
  _SUCCESS
  ```

3. **Télécharger un fichier pour validation :**

   ```bash
   aws s3 cp s3://fruits-classification-p9-maxime/Results/pca_output/part-00000-XXX.parquet \
     ~/Desktop/sample_pca.parquet
   ```

   **Remplacer `part-00000-XXX.parquet` par le vrai nom de fichier de la liste**

4. **Vérifier le fichier avec Python :**

   ```bash
   python3 << 'EOF'
   import pandas as pd
   df = pd.read_parquet('~/Desktop/sample_pca.parquet')
   print(f"Colonnes: {df.columns.tolist()}")
   print(f"Nombre de lignes: {len(df)}")
   print(df.head())
   EOF
   ```

**✅ VOUS DEVEZ VOIR :**
- Colonnes : ['path', 'label', 'features_pca']
- Nombre de lignes : XXX
- Tableau avec les données

**PARFAIT !** Résultats PCA validés ✅

---

### Étape 5.2 : Vérifier les Coûts AWS

**📍 CE QUE VOUS ALLEZ FAIRE :** Vérifier que vous n'avez pas dépassé 10€

1. **AWS Console, barre de recherche :** Taper `Cost Explorer`
2. **Cliquer sur "Cost Explorer"**

3. **Page Cost Explorer :**
   - **Date range :** Sélectionner "Last 7 days"
   - **Group by :** Sélectionner "Service"
   - **Filter :** Ajouter filtre : Service = EMR, S3

**✅ VOUS DEVEZ VOIR :**
- Graphique avec coûts par service
- Total : **< 10€** (normalement ~1.69€)

**Détails attendus :**
- EMR : ~1.11€ (3 heures)
- S3 : ~0.58€ (stockage + transferts)
- **Total : ~1.69€**

**✅ Si < 10€ :** Tout est OK !
**⚠️ Si > 10€ :** Vérifier qu'il n'y a pas d'autres services actifs

---

### Étape 5.3 : ⚠️ TERMINER LE CLUSTER EMR (CRITIQUE !)

**📍 CE QUE VOUS ALLEZ FAIRE :** Éteindre le cluster pour arrêter les coûts

**⚠️ NE PAS OUBLIER CETTE ÉTAPE ! SINON COÛTS CONTINUENT !**

1. **AWS Console → EMR → Clusters**

2. **Vous voyez votre cluster dans la liste**

3. **COCHER la case** à gauche du nom du cluster

4. **Cliquer sur le bouton "Terminate"** (bouton en haut)

5. **Popup de confirmation :**
   - **Lire le message** : "Are you sure you want to terminate..."
   - **Cliquer sur "Terminate"**

**✅ VOUS DEVEZ VOIR :**
- Status du cluster change : "Waiting" → "Terminating"

⏱️ **ATTENDRE 5-10 minutes**

6. **Rafraîchir la page** (bouton refresh) toutes les 2 minutes

**✅ QUAND STATUS = "TERMINATED" :**
- Cluster éteint ✅
- Coûts arrêtés ✅

**VÉRIFICATION FINALE :**

7. **Vérifier qu'AUCUN autre cluster n'est actif :**
   - Dans la liste, filtrer par status : "Waiting" ou "Running"
   - **Liste doit être VIDE**

**✅ SI LISTE VIDE :** Plus aucun cluster actif, coûts EMR arrêtés ✅

---

### Étape 5.4 : Checklist Finale

**📋 Vérifier que tout est OK avant de finir :**

- [ ] Résultats PCA présents sur S3 (fichiers .parquet)
- [ ] Variance PCA ≥ 90% validée
- [ ] Coûts AWS totaux < 10€ (normalement ~1.69€)
- [ ] Cluster EMR status = "Terminated"
- [ ] Aucun autre cluster actif
- [ ] Screenshots capturés (EMR, JupyterHub, PCA, S3)
- [ ] Fichier .pem sauvegardé dans ~/.ssh/ (pour accès futur si besoin)

**✅ SI TOUT EST COCHÉ :** PHASE 5 TERMINÉE ! Projet AWS réussi ! 🎉

---

**📌 TOUTES LES PHASES TERMINÉES !**

**✅ CE QUE VOUS AVEZ ACCOMPLI :**
1. Configuration AWS complète (Budget, IAM, région eu-west-1)
2. Bucket S3 créé avec dataset uploadé (67k images)
3. Cluster EMR créé et configuré (Spot + Graviton2)
4. JupyterHub accessible et fonctionnel
5. Notebook PySpark exécuté avec succès
6. Broadcast TensorFlow optimisé ✅
7. PCA PySpark (1280 → 256 dimensions, variance ≥ 90%) ✅
8. Résultats sauvegardés sur S3 ✅
9. Coûts maîtrisés (~1.69€ au lieu de 10€) ✅
10. Cluster terminé (coûts arrêtés) ✅

**🎓 PROCHAINE ÉTAPE :**
- Créer le support de présentation (Feature 5)
- Utiliser les screenshots capturés
- Préparer la soutenance de 20 minutes

---

## 🆘 Troubleshooting (Résolution de Problèmes)

### Problème 1 : Cluster ne démarre pas

**SYMPTÔME :** Status reste bloqué sur "Starting" ou erreur "Insufficient capacity"

**CAUSE :** Capacité Spot insuffisante dans eu-west-1

**SOLUTION :**
1. Terminer le cluster actuel
2. Recréer cluster avec **"On-Demand"** au lieu de "Spot"
3. ⚠️ Coûts plus élevés (~3-4€ au lieu de 1.69€) mais ça fonctionnera

**ALTERNATIVE :**
- Utiliser instances **m5.xlarge** au lieu de m6g.xlarge (x86 au lieu de ARM)

---

### Problème 2 : JupyterHub inaccessible

**SYMPTÔME :** Page ne charge pas, timeout, ou "Connection refused"

**CAUSES POSSIBLES :**

**Cause A : Security group mal configuré**

**SOLUTION :**
1. AWS Console → EMR → Votre cluster → "Security and access"
2. Cliquer sur Security group du Master
3. Vérifier règle inbound : Port 9443, Source = My IP
4. Si absente : Ajouter la règle (voir Phase 2, Étape 2.2)
5. **Important :** Vérifier que c'est bien VOTRE IP publique
   - Aller sur https://whatismyipaddress.com pour voir votre IP
   - Comparer avec l'IP dans la règle

**Cause B : Cluster pas encore prêt**

**SOLUTION :**
- Vérifier que status = "Waiting" (pas "Starting" ou "Bootstrapping")
- Attendre encore 5-10 minutes

**Cause C : Mauvaise URL**

**SOLUTION :**
- Vérifier URL : `https://[DNS-MASTER]:9443` (pas http, et bien port 9443)
- Vérifier DNS Master copié correctement

---

### Problème 3 : Accès S3 refusé depuis EMR

**SYMPTÔME :** Erreur dans le notebook : "Access Denied" ou "Permission denied" en lisant S3

**CAUSE :** Rôle IAM EMR_EC2_DefaultRole_P9 n'a pas les permissions S3

**SOLUTION :**
1. AWS Console → IAM → Roles
2. Chercher : `EMR_EC2_DefaultRole_P9`
3. Cliquer dessus
4. Onglet "Permissions"
5. Vérifier que la policy **AmazonS3FullAccess** est attachée
6. Si absente :
   - Cliquer "Attach policies"
   - Chercher `AmazonS3FullAccess`
   - Cocher et "Attach"
7. **Redémarrer le cluster** (Terminate puis Create à nouveau)

---

### Problème 4 : Dépassement de coûts

**SYMPTÔME :** Email AWS disant que vous avez dépensé > 10€

**CAUSES POSSIBLES :**
- Cluster EMR non terminé
- Instances On-Demand au lieu de Spot
- Cluster tournant depuis plusieurs jours

**SOLUTION IMMÉDIATE :**
1. **AWS Console → EMR → Clusters**
2. **Vérifier TOUS les clusters** (pas seulement le premier)
3. **TERMINER IMMÉDIATEMENT** tous les clusters actifs (status ≠ Terminated)
4. **Vérifier autres services :**
   - EC2 → Instances (vérifier qu'aucune instance ne tourne)
   - RDS → Databases (vérifier qu'aucune DB active)
5. **Cost Explorer :** Identifier quel service coûte cher

**PRÉVENTION :**
- Toujours configurer auto-termination (3 heures)
- Vérifier status cluster après chaque session
- Activer alertes budget (Phase 0, Étape 0.3)

---

### Problème 5 : Dataset upload très lent

**SYMPTÔME :** AWS CLI upload prend > 3 heures

**CAUSES POSSIBLES :**
- Connexion internet lente
- Upload via Console (plus lent que CLI)

**SOLUTION :**
1. **Vérifier votre connexion internet :**
   ```bash
   speedtest-cli
   ```
   - Upload speed doit être > 5 Mbps

2. **Utiliser AWS CLI (plus rapide que Console)**

3. **Upload en plusieurs fois :**
   ```bash
   # Uploader seulement quelques classes pour tester :
   aws s3 sync ./data/raw/fruits-360_dataset/fruits-360/Training/Apple* \
     s3://fruits-classification-p9-maxime/Test/ \
     --region eu-west-1
   ```

4. **Lancer upload le soir et laisser tourner la nuit**

---

### Problème 6 : Variance PCA < 90%

**SYMPTÔME :** Cellule PCA affiche "Variance expliquée: 85%" (< 90%)

**CAUSE :** 256 composantes ne suffisent pas

**SOLUTION :**
1. **Dans le notebook, modifier la cellule PCA :**
   ```python
   # Au lieu de n_components=256, utiliser :
   df_pca, pca_model = apply_pca_reduction(df_prepared, n_components=512)
   ```

2. **Ré-exécuter la cellule PCA**

3. **Vérifier nouvelle variance** (doit être ≥ 90% avec 512 composantes)

**ALTERNATIVE :**
- Utiliser `n_components=384` (compromis entre 256 et 512)

---

### Problème 7 : Import TensorFlow échoue

**SYMPTÔME :** Erreur "ModuleNotFoundError: No module named 'tensorflow'"

**CAUSE :** Cellule d'installation des packages (4.10.2) n'a pas été exécutée

**SOLUTION :**
1. **Retourner au début de la section cloud du notebook**
2. **Chercher la cellule 4.10.2 :** `!pip install Pandas pillow tensorflow pyspark pyarrow`
3. **Exécuter cette cellule** (attendre 2-3 minutes)
4. **Restart kernel si nécessaire** : Menu Kernel → Restart
5. **Ré-exécuter les cellules depuis le début de la section cloud**

---

## 📚 Ressources Complémentaires

### Documentation AWS Officielle

- [AWS EMR Getting Started](https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-gs.html)
- [Amazon S3 User Guide](https://docs.aws.amazon.com/s3/index.html)
- [AWS EMR Pricing Calculator](https://aws.amazon.com/emr/pricing/)
- [AWS Cost Explorer](https://aws.amazon.com/aws-cost-management/aws-cost-explorer/)

### Commandes AWS CLI Utiles

```bash
# Lister tous les clusters EMR
aws emr list-clusters --region eu-west-1

# Décrire un cluster spécifique
aws emr describe-cluster --cluster-id j-XXXXXXXXXXXXX --region eu-west-1

# Terminer un cluster via CLI
aws emr terminate-clusters --cluster-ids j-XXXXXXXXXXXXX --region eu-west-1

# Vérifier les coûts du mois en cours
aws ce get-cost-and-usage \
  --time-period Start=2025-10-01,End=2025-10-31 \
  --granularity MONTHLY \
  --metrics BlendedCost \
  --region eu-west-1

# Lister tous les buckets S3
aws s3 ls

# Lister contenu d'un bucket
aws s3 ls s3://fruits-classification-p9-maxime/ --recursive

# Télécharger un dossier complet depuis S3
aws s3 sync s3://fruits-classification-p9-maxime/Results/ ./local_results/

# Supprimer un bucket S3 (ATTENTION : supprime tout)
aws s3 rb s3://fruits-classification-p9-maxime --force
```

### Nettoyage Après Soutenance (Optionnel)

**Si vous voulez supprimer TOUT pour économiser (après soutenance) :**

```bash
# 1. Terminer tous les clusters EMR
aws emr list-clusters --region eu-west-1 --active
aws emr terminate-clusters --cluster-ids j-XXX j-YYY --region eu-west-1

# 2. Supprimer le dataset (garder Results/)
aws s3 rm s3://fruits-classification-p9-maxime/Test/ --recursive

# 3. OU supprimer tout le bucket
aws s3 rb s3://fruits-classification-p9-maxime --force

# 4. Supprimer les rôles IAM (optionnel)
# AWS Console → IAM → Roles → Sélectionner → Delete
```

⚠️ **Attention :** Une fois supprimées, les données ne peuvent pas être récupérées !

---

**Version :** 2.0 - Guide Ultra-Détaillé
**Dernière mise à jour :** 6 octobre 2025
**Auteur :** Assistant Claude pour Projet P9 Fruits Classification
**Public :** Débutant AWS (aucune expérience préalable requise)

---

**🎉 FÉLICITATIONS !**

Si vous avez suivi ce guide jusqu'au bout, vous avez :
- ✅ Maîtrisé les bases d'AWS (S3, EMR, IAM)
- ✅ Déployé une architecture Big Data cloud
- ✅ Exécuté un pipeline PySpark distribué
- ✅ Optimisé les coûts (Spot, Graviton2)
- ✅ Respecté le RGPD (eu-west-1)
- ✅ Validé les critères d'évaluation du projet

**Vous êtes prêt pour la soutenance ! 🚀**
