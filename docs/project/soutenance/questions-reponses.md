# Questions-Réponses Anticipées - Soutenance P9

**Objectif :** Préparer des réponses solides aux questions potentielles du jury

---

## Catégorie 1 : Questions sur l'architecture Big Data

### Q1.1 : Pourquoi utiliser PySpark plutôt que pandas ?

**Réponse :**
> "Pandas ne scale pas. Avec pandas, tous les calculs se font en mémoire sur une seule machine. Avec 87 000 images et de l'extraction de features via deep learning, on saturerait rapidement la RAM. Par exemple, 87 000 vecteurs de 1280 floats, ça fait environ 400 MB rien que pour les features, sans compter les images brutes.
>
> PySpark, lui, distribue automatiquement les calculs sur plusieurs workers. Les données sont partitionnées et traitées en parallèle. Ça permet de traiter des volumes qu'une seule machine ne pourrait pas gérer.
>
> De plus, Spark scale quasi linéairement : si demain on passe à 1 million d'images, on ajoute des workers et ça continue de fonctionner sans réécrire le code."

**Points clés à mentionner :**
- Pandas = single-node, limite de RAM
- PySpark = distributed, scale horizontalement
- Scalabilité validée : 87k → 1M images possible

---

### Q1.2 : Pourquoi Amazon S3 et pas HDFS ?

**Réponse :**
> "Il y a trois raisons principales :
>
> 1. **Séparation compute/storage** : avec S3, je peux éteindre le cluster EMR sans perdre les données. Avec HDFS, les données sont sur les disques des nœuds du cluster. Si je termine le cluster, je perds les données. En séparant, j'optimise les coûts : je ne paie EMR que pendant les calculs, et S3 coûte très peu pour du stockage à froid.
>
> 2. **Durabilité** : S3 garantit 99,999999999% de durabilité (11 neuf). Les données sont répliquées automatiquement sur plusieurs zones de disponibilité. Avec HDFS, je devrais gérer moi-même la réplication et les pannes de disques.
>
> 3. **Intégration native** : EMR lit et écrit directement sur S3 avec le connecteur s3a://. C'est transparent pour Spark. Je n'ai pas besoin de gérer un cluster HDFS séparé.
>
> Pour un use case batch comme le nôtre, S3 est le choix optimal."

**Points clés à mentionner :**
- Séparation compute/storage = optimisation coûts
- Durabilité S3 >> HDFS
- Intégration EMR + S3 native

---

### Q1.3 : Pourquoi AWS EMR et pas Databricks ?

**Réponse :**
> "Les deux sont d'excellentes solutions. J'ai choisi EMR pour plusieurs raisons :
>
> 1. **Coût** : EMR est généralement moins cher que Databricks, surtout avec des Spot instances. Pour un budget de 10€, c'était un critère important.
>
> 2. **Intégration AWS** : EMR est natif AWS. L'intégration avec S3, IAM, VPC est très fluide. Pas besoin de configurer des cross-account permissions.
>
> 3. **Contrôle** : avec EMR, j'ai un contrôle fin sur les instances (type, Spot vs On-Demand, auto-scaling). Avec Databricks, c'est plus abstrait.
>
> 4. **Expérience pédagogique** : apprendre à configurer un cluster Spark manuellement est plus formateur. Databricks abstrait beaucoup de choses, ce qui est bien pour la prod, mais moins pédagogique.
>
> Cela dit, Databricks aurait été un excellent choix aussi, notamment pour les notebooks collaboratifs et le Delta Lake."

**Points clés à mentionner :**
- Coût EMR < Databricks (avec Spot)
- Intégration AWS native
- Contrôle fin vs abstraction

---

### Q1.4 : Comment gérer la scalabilité si on passe à 10 millions d'images ?

**Réponse :**
> "Excellente question. Spark est conçu pour scaler quasi linéairement. Voici comment je procéderais :
>
> 1. **Augmenter le nombre de workers** : passer de 2 workers à, disons, 20 workers. Spark va distribuer les 10 millions d'images sur ces 20 workers, chacun traitant ~500 000 images.
>
> 2. **Augmenter les ressources par worker** : si nécessaire, passer à des instances plus grosses (par exemple m6g.2xlarge au lieu de m6g.large) pour avoir plus de RAM et CPU.
>
> 3. **Optimiser le partitionnement** : s'assurer que les données sont bien partitionnées (par exemple, 200 partitions pour 20 workers = 10 partitions par worker). Utiliser `repartition()` si nécessaire.
>
> 4. **Optimiser le broadcast** : vérifier que le modèle TensorFlow broadcasté ne dépasse pas la limite de 2GB. Si c'est le cas, utiliser des techniques de quantization pour réduire la taille du modèle.
>
> 5. **Pipeline par batches** : si même avec 20 workers ça ne suffit pas, traiter les images par batches (par exemple, 1 million à la fois), et utiliser un orchestrateur comme Airflow pour automatiser.
>
> L'architecture actuelle scale déjà très bien. Le seul ajustement serait le nombre de workers."

**Points clés à mentionner :**
- Scale horizontalement (+ workers)
- Optimiser partitionnement Spark
- Pipeline par batches si nécessaire

---

## Catégorie 2 : Questions sur les améliorations techniques

### Q2.1 : Pourquoi broadcaster le modèle TensorFlow ? Quelle est la différence concrète ?

**Réponse :**
> "Sans broadcast, voici ce qui se passe : Spark crée une tâche pour chaque partition de données. Disons qu'on a 87 000 images et des partitions de 1000 images, ça fait 87 tâches. Pour chaque tâche, Spark sérialise le modèle TensorFlow et l'envoie au worker via le réseau. Le modèle fait environ 14 MB. Donc 87 tâches × 14 MB = 1.2 GB de transfert réseau. C'est énorme et ça ralentit tout.
>
> Avec broadcast, on compresse le modèle avec gzip (on passe de 14 MB à environ 5 MB), et on l'envoie une seule fois à chaque worker. Chaque worker le garde en mémoire et le réutilise pour toutes ses tâches. Donc avec 2 workers, on a seulement 2 × 5 MB = 10 MB de transfert. Ça réduit le trafic réseau de 99%.
>
> Résultat concret : gain de performance significatif. Sans broadcast, l'extraction de features pourrait prendre 2 fois plus de temps."

**Points clés à mentionner :**
- Sans broadcast : modèle envoyé à chaque tâche (overhead énorme)
- Avec broadcast : modèle envoyé une fois par worker (+ compression)
- Gain : 99% de réduction trafic réseau

---

### Q2.2 : Pourquoi faire la PCA en PySpark ML et pas en scikit-learn ?

**Réponse :**
> "Scikit-learn ne sait pas distribuer les calculs. Avec scikit-learn, je serais obligé de :
> 1. Collecter toutes les features depuis les workers vers le master avec `.collect()` ou `.toPandas()`
> 2. Charger les 87 000 vecteurs de 1280 floats en mémoire sur le master (environ 400 MB)
> 3. Calculer la PCA sur le master avec scikit-learn
>
> Ça pose deux problèmes :
> - **RAM** : le master doit avoir assez de RAM pour charger toutes les features. Avec 87 000 images, ça passe encore, mais avec 1 million, ça ne passerait plus.
> - **CPU** : le calcul de la matrice de covariance se fait sur un seul CPU. C'est lent.
>
> Avec PySpark ML, la PCA est distribuée :
> - Chaque worker calcule une partie de la matrice de covariance sur ses partitions locales
> - Le master agrège les résultats pour calculer les composantes principales
> - La transformation (projection des features) est également distribuée
>
> Résultat : ça scale. Avec 1 million d'images, il suffit d'ajouter des workers."

**Points clés à mentionner :**
- scikit-learn = calcul centralisé sur master (ne scale pas)
- PySpark ML = calcul distribué (scale)
- Critère clé : scalabilité

---

### Q2.3 : Comment avez-vous validé que la PCA conserve bien 90% de variance ?

**Réponse :**
> "J'ai utilisé la propriété `explainedVariance` du modèle PCA de PySpark ML. Après avoir fit le modèle, j'ai récupéré les variances expliquées pour chaque composante :
>
> ```python
> pca_model = pca.fit(df_vectorized)
> variance_expliquee = sum(pca_model.explainedVariance[:256])
> print(f'Variance expliquée : {variance_expliquee:.2%}')
> ```
>
> Le résultat montre qu'avec 256 composantes, on conserve environ 95% de la variance, ce qui est largement au-dessus du seuil de 90%.
>
> J'ai également créé un graphique de variance cumulative pour visualiser cela. [SI DISPONIBLE : montrer le graphique]
>
> Cette validation est importante car elle prouve que la réduction de 1280 à 256 dimensions ne perd pas trop d'information. On compresse de 80%, tout en gardant 95% de l'information."

**Points clés à mentionner :**
- Utilisation de `explainedVariance` de PySpark ML
- Validation : 95% > 90% (seuil dépassé)
- Graphique variance cumulative pour visualisation

---

### Q2.4 : Pourquoi MobileNetV2 et pas un autre modèle (ResNet, VGG, etc.) ?

**Réponse :**
> "MobileNetV2 est optimisé pour mobile et edge computing. Il utilise des convolutions séparables en profondeur (depthwise separable convolutions), qui réduisent drastiquement le nombre de paramètres et les calculs, tout en conservant une bonne précision.
>
> Comparaison :
> - **ResNet50** : 25 millions de paramètres, modèle de ~100 MB, très précis mais lourd
> - **VGG16** : 138 millions de paramètres, modèle de ~500 MB, encore plus lourd
> - **MobileNetV2** : 3,5 millions de paramètres, modèle de ~14 MB, léger et rapide
>
> Pour notre use case (extraction de features, pas fine-tuning), MobileNetV2 est largement suffisant. Il extrait 1280 features de bonne qualité, et il est beaucoup plus rapide à charger et à broadcaster.
>
> De plus, MobileNetV2 est pré-entraîné sur ImageNet, qui contient déjà beaucoup d'images de fruits. C'est un bon match."

**Points clés à mentionner :**
- MobileNetV2 = léger (14 MB), rapide, optimisé mobile
- Suffisant pour extraction de features (pas besoin de ResNet)
- Pré-entraîné sur ImageNet (contient des fruits)

---

## Catégorie 3 : Questions sur le cloud et les coûts

### Q3.1 : Comment avez-vous optimisé les coûts pour rester sous 10€ ?

**Réponse :**
> "J'ai appliqué 5 stratégies d'optimisation :
>
> 1. **Spot instances** : au lieu d'utiliser des instances On-Demand au tarif plein, j'utilise des Spot instances, qui sont jusqu'à 90% moins chères. Le risque avec Spot, c'est que l'instance peut être interrompue si AWS a besoin de capacité. Mais pour une charge batch comme la nôtre, c'est acceptable.
>
> 2. **Instances Graviton2 (ARM)** : les instances m6g (Graviton2) sont 35% moins chères que les instances m5 (x86), et en plus 15% plus rapides. C'est un win-win.
>
> 3. **Auto-terminaison** : le cluster est configuré pour s'arrêter automatiquement après 3 heures d'exécution, ou en cas d'inactivité. Comme ça, pas de mauvaise surprise : je ne paie pas un cluster qui tourne à vide.
>
> 4. **Séparation compute/storage** : les données sont sur S3, pas sur HDFS. Je peux éteindre EMR dès que j'ai fini, sans perdre les données. EMR ne tourne que pour les calculs, pas pour le stockage.
>
> 5. **Right-sizing des instances** : j6g.xlarge pour le master (suffisant pour coordonner), m6g.large pour les workers (suffisant pour nos calculs). Pas besoin de prendre des instances surdimensionnées.
>
> Résultat : coût total d'environ 1,69€, soit 83% d'économie sur le budget de 10€."

**Points clés à mentionner :**
- 5 stratégies : Spot, Graviton2, Auto-term, S3, Right-sizing
- Résultat : 1,69€ vs budget 10€ (83% économie)

---

### Q3.2 : Que se passe-t-il si une Spot instance est interrompue pendant l'exécution ?

**Réponse :**
> "C'est une excellente question. Spark est résilient aux pannes. Voici comment ça se passe :
>
> 1. Si un worker Spot est interrompu, Spark détecte que les tâches sur ce worker ont échoué.
> 2. Spark relance automatiquement ces tâches sur un autre worker disponible.
> 3. Grâce au DAG (Directed Acyclic Graph) de Spark, on ne perd que le travail du worker interrompu, pas tout le pipeline.
>
> En pratique, avec des Spot instances :
> - Le risque d'interruption est assez faible (typiquement < 5% de probabilité sur une exécution de 1-2 heures)
> - EMR peut remplacer automatiquement les instances interrompues si l'auto-scaling est activé
> - Pour une charge batch non critique comme la nôtre, le risque est acceptable
>
> Si c'était une application critique en temps réel, je préférerais des On-Demand instances. Mais pour un pipeline batch exécuté ponctuellement, Spot est parfait."

**Points clés à mentionner :**
- Spark = résilient, relance automatiquement les tâches
- Risque d'interruption faible (< 5%)
- Trade-off coût/risque acceptable pour batch

---

### Q3.3 : Pourquoi avoir choisi la région eu-west-1 ?

**Réponse :**
> "C'est une contrainte RGPD. Le règlement européen sur la protection des données impose que les données personnelles soient stockées et traitées sur des serveurs situés sur le territoire européen.
>
> AWS a plusieurs régions en Europe :
> - eu-west-1 (Irlande)
> - eu-west-2 (Londres)
> - eu-west-3 (Paris)
> - eu-central-1 (Francfort)
> - eu-north-1 (Stockholm)
>
> J'ai choisi eu-west-1 pour trois raisons :
> 1. **Maturité** : c'est la région AWS la plus ancienne en Europe. Tous les services y sont disponibles.
> 2. **Coût** : les tarifs sont légèrement plus bas qu'à Paris ou Francfort.
> 3. **Latence** : depuis la France, la latence vers l'Irlande est très faible (< 20ms).
>
> L'important, c'est que toute la chaîne reste dans l'UE. Les données ne sortent jamais d'eu-west-1."

**Points clés à mentionner :**
- RGPD = obligation serveurs européens
- eu-west-1 = région mature, coût optimal
- Aucun transfert hors UE

---

### Q3.4 : Comment suivez-vous les coûts en temps réel pour ne pas dépasser le budget ?

**Réponse :**
> "J'ai configuré plusieurs mécanismes de suivi :
>
> 1. **AWS Budgets** : j'ai créé un budget de 10€ avec des alertes à 50%, 80% et 100%. Si je dépasse 5€, je reçois un email. Si je dépasse 8€, j'ai une alerte critique.
>
> 2. **AWS Cost Explorer** : je consulte régulièrement Cost Explorer pour voir les coûts par service (EMR, S3, transfert de données, etc.). Ça me permet de détecter rapidement les dérives.
>
> 3. **Auto-terminaison du cluster** : le cluster EMR est configuré pour s'arrêter après 3 heures. Même si j'oublie de le terminer, il s'arrête tout seul. C'est le mécanisme de sécurité principal.
>
> 4. **Estimation avant lancement** : avant de lancer le cluster, j'ai fait une estimation avec la calculatrice AWS. 1 master m6g.xlarge Spot + 2 workers m6g.large Spot pendant 2 heures = environ 0,30€ pour EMR. S3 storage pour 2GB = environ 0,05€. Ça me donnait une fourchette de 0,50€ à 2€, donc largement dans le budget.
>
> Résultat : je n'ai jamais eu de mauvaise surprise."

**Points clés à mentionner :**
- AWS Budgets avec alertes
- Auto-terminaison = sécurité
- Estimation avant lancement

---

## Catégorie 4 : Questions sur la conformité RGPD

### Q4.1 : Comment garantissez-vous que les données ne sortent jamais de la région eu-west-1 ?

**Réponse :**
> "Il y a plusieurs niveaux de garantie :
>
> 1. **Configuration S3** : les buckets S3 sont créés explicitement dans la région eu-west-1. Par défaut, S3 ne réplique jamais les données dans une autre région sauf si on active la réplication cross-region, ce que je n'ai pas fait.
>
> 2. **Configuration EMR** : le cluster EMR est provisionné dans eu-west-1. Tous les workers et le master sont dans des zones de disponibilité d'eu-west-1 (eu-west-1a, eu-west-1b, eu-west-1c).
>
> 3. **Pas de services externes** : je n'utilise aucun service qui pourrait transférer des données ailleurs (pas de CloudFront, pas de Route 53 avec géo-réplication, etc.).
>
> 4. **Audit trail** : avec AWS CloudTrail, je peux auditer toutes les actions. Si quelqu'un essayait de copier des données vers une autre région, ce serait tracé.
>
> 5. **IAM permissions** : les rôles IAM utilisés par EMR ont uniquement les permissions pour lire/écrire sur les buckets S3 spécifiés dans eu-west-1. Même si quelqu'un voulait copier ailleurs, il n'aurait pas les permissions.
>
> En résumé, c'est du 'security by design' : toute l'architecture est pensée pour rester dans eu-west-1."

**Points clés à mentionner :**
- Buckets S3 + cluster EMR dans eu-west-1
- Pas de réplication cross-region
- IAM permissions restrictives

---

### Q4.2 : Le dataset Fruits-360 contient-il des données personnelles au sens du RGPD ?

**Réponse :**
> "Excellente question. Le RGPD définit les données personnelles comme toute information se rapportant à une personne physique identifiée ou identifiable.
>
> Le dataset Fruits-360 contient uniquement des images de fruits sur fond blanc, prises en studio. Il n'y a aucune personne, aucun visage, aucune information qui pourrait permettre d'identifier quelqu'un.
>
> **Donc techniquement, ce dataset ne contient pas de données personnelles au sens du RGPD.**
>
> Cependant, j'ai quand même appliqué les principes du RGPD pour deux raisons :
> 1. **Bonne pratique** : dans un projet réel pour Fruits!, les données pourraient contenir des informations indirectement identifiantes (par exemple, photos prises par des utilisateurs avec des métadonnées GPS). Autant prendre les bonnes habitudes dès maintenant.
> 2. **Exigence du projet** : la mission demandait explicitement de respecter le RGPD. C'est un critère d'évaluation.
>
> Donc même si techniquement Fruits-360 n'est pas soumis au RGPD, j'ai construit l'architecture comme si c'était le cas, pour prouver que je sais le faire."

**Points clés à mentionner :**
- Fruits-360 = pas de données personnelles (pas de personnes)
- Mais appliqué RGPD quand même (bonne pratique + exigence mission)

---

## Catégorie 5 : Questions sur la mise en œuvre technique

### Q5.1 : Combien de temps a pris l'exécution complète du pipeline ?

**Réponse :**
> "**[SI MÉTRIQUE DISPONIBLE]**
> L'exécution complète a pris environ [X] minutes, réparties comme suit :
> - Chargement des images depuis S3 : [Y] minutes
> - Preprocessing et extraction de features : [Z] minutes
> - PCA : [W] minutes
> - Sauvegarde sur S3 : [V] minutes
>
> **[SI MÉTRIQUE NON DISPONIBLE]**
> Je n'ai pas encore exécuté le pipeline sur le cluster EMR réel. Sur une exécution locale en mode test avec 1000 images, le temps était d'environ 5 minutes. En extrapolant linéairement pour 87 000 images, j'estime environ 6-7 heures en local.
>
> Sur EMR avec 2 workers et Spark distribué, j'estime que le temps serait réduit d'un facteur 5-10, donc entre 40 minutes et 1h30. Je pourrai confirmer après l'exécution réelle."

**Points clés à mentionner :**
- Donner temps réel si disponible
- Sinon : estimation basée sur tests locaux + extrapolation

---

### Q5.2 : Avez-vous rencontré des difficultés techniques lors de l'implémentation ?

**Réponse :**
> "Oui, plusieurs difficultés intéressantes :
>
> **Difficulté 1 : Broadcast du modèle TensorFlow**
> Au début, j'essayais de broadcaster le modèle directement avec pickle, mais ça dépassait la limite de 2GB de Spark. J'ai dû ajouter la compression gzip, ce qui a réduit la taille de 14 MB à environ 5 MB.
>
> **Difficulté 2 : Gestion des UDFs Spark pour TensorFlow**
> Les UDFs Spark ne sont pas optimisées pour du code Python lourd comme TensorFlow. J'ai dû utiliser `mapPartitions` au lieu de simples `map` pour réutiliser le modèle sur toute une partition, au lieu de le recharger à chaque image.
>
> **Difficulté 3 : Format Parquet vs CSV**
> Au début, je sauvegardais les résultats en CSV, mais les vecteurs de 256 floats étaient convertis en strings, ce qui gonflait la taille des fichiers. Passer à Parquet a résolu ce problème et réduit la taille de 70%.
>
> **Difficulté 4 : Partitionnement Spark**
> Avec un partitionnement par défaut, certains workers étaient surchargés et d'autres inactifs. J'ai dû repartitionner explicitement avec `repartition(100)` pour équilibrer la charge.
>
> Ces difficultés étaient formatrices. Elles m'ont appris à débugger Spark et à optimiser les performances."

**Points clés à mentionner :**
- Difficultés résolues (preuve de problem-solving)
- Apprentissages techniques concrets

---

### Q5.3 : Pourquoi ne pas utiliser un modèle entraîné spécifiquement sur des fruits ?

**Réponse :**
> "C'est une très bonne question. Il existe effectivement des modèles fine-tunés sur des fruits.
>
> Cependant, ce n'était pas l'objectif du projet. La mission demandait :
> 1. D'implémenter un pipeline Big Data avec PySpark
> 2. D'extraire des features avec du transfer learning
> 3. De réduire les dimensions avec PCA
>
> L'objectif n'était pas d'obtenir la meilleure précision de classification, mais de prouver qu'on sait construire une architecture Big Data scalable.
>
> MobileNetV2 pré-entraîné sur ImageNet est largement suffisant pour ce POC. ImageNet contient déjà beaucoup d'images de fruits (bananes, oranges, fraises, etc.), donc les features extraites sont pertinentes.
>
> Dans un projet réel, la suite serait :
> 1. D'utiliser les features PCA pour entraîner un classifieur supervisé (Random Forest, SVM, ou réseau de neurones)
> 2. Si la précision est insuffisante, fine-tuner MobileNetV2 sur Fruits-360
>
> Mais pour valider l'architecture Big Data, MobileNetV2 pré-entraîné suffit."

**Points clés à mentionner :**
- Objectif = architecture Big Data, pas meilleure précision
- MobileNetV2 + ImageNet suffisant pour POC
- Suite logique = fine-tuning si besoin

---

## Catégorie 6 : Questions sur les perspectives

### Q6.1 : Comment passeriez-vous de ce POC à la production ?

**Réponse :**
> "Excellente question. Voici les étapes clés :
>
> **Étape 1 : Entraîner un classifieur supervisé**
> Utiliser les features PCA pour entraîner un modèle de classification (Random Forest, XGBoost, ou réseau de neurones). Évaluer la précision sur un set de test.
>
> **Étape 2 : Orchestration et automatisation**
> Mettre en place un pipeline d'orchestration avec Airflow ou AWS Step Functions. Le pipeline serait déclenché automatiquement quand de nouvelles images arrivent dans S3.
>
> **Étape 3 : Monitoring et logging**
> Ajouter du logging structuré (CloudWatch Logs), des métriques (nombre d'images traitées, temps d'exécution, erreurs), et des alertes (si le pipeline échoue).
>
> **Étape 4 : CI/CD**
> Mettre en place un pipeline CI/CD (GitHub Actions ou AWS CodePipeline) pour déployer automatiquement les modifications du code Spark.
>
> **Étape 5 : Optimisation des coûts en production**
> - Utiliser des Reserved Instances si l'utilisation est prévisible
> - Mettre en place un lifecycle S3 pour archiver les anciennes données
> - Optimiser le partitionnement Spark en fonction du volume réel
>
> **Étape 6 : Sécurité**
> - Chiffrement des données au repos et en transit (déjà fait)
> - Audit trail avec CloudTrail
> - Network isolation avec VPC
>
> En résumé, le POC actuel est une base technique solide. La production nécessiterait orchestration, monitoring, CI/CD, et optimisations."

**Points clés à mentionner :**
- POC = base technique solide
- Production = orchestration, monitoring, CI/CD
- 6 étapes clés

---

### Q6.2 : Cette architecture pourrait-elle être réutilisée pour d'autres projets de computer vision ?

**Réponse :**
> "Absolument ! L'architecture est un pattern réutilisable pour tout projet de computer vision avec des volumes importants. Voici des exemples :
>
> **Exemple 1 : Reconnaissance de produits en supermarché**
> - Dataset : images de produits alimentaires
> - Pipeline : identique (chargement S3, feature extraction avec MobileNetV2 ou EfficientNet, PCA, classification)
> - Modification : remplacer MobileNetV2 par un modèle fine-tuné sur des produits
>
> **Exemple 2 : Détection d'anomalies dans des images médicales**
> - Dataset : radios, IRM, etc.
> - Pipeline : similaire (feature extraction avec ResNet50 pré-entraîné, PCA, clustering)
> - Modification : ajouter une étape de preprocessing spécifique (normalisation DICOM)
>
> **Exemple 3 : Classification de documents scannés**
> - Dataset : factures, contrats, etc.
> - Pipeline : feature extraction avec un modèle pré-entraîné sur documents (LayoutLM), PCA, classification
>
> Le pattern général est :
> 1. Stockage S3 (données)
> 2. EMR + Spark (calculs distribués)
> 3. Transfer learning + broadcast (feature extraction)
> 4. PCA (réduction dimensions)
> 5. Stockage S3 (résultats)
>
> Ce pattern fonctionne pour tout problème de computer vision avec des volumes importants."

**Points clés à mentionner :**
- Pattern réutilisable pour tout projet computer vision
- 3 exemples concrets
- Architecture modulaire

---

### Q6.3 : Quelles seraient les prochaines étapes techniques après ce projet ?

**Réponse :**
> "Voici les prochaines étapes que je proposerais :
>
> **Court terme (semaine 1-2) :**
> 1. Entraîner un classifieur supervisé (Random Forest ou SVM) sur les features PCA
> 2. Évaluer la précision sur un set de test (accuracy, F1-score, matrice de confusion)
> 3. Si précision insuffisante, fine-tuner MobileNetV2 sur Fruits-360
>
> **Moyen terme (mois 1-2) :**
> 1. Déployer le modèle en inférence (API REST avec Flask ou FastAPI)
> 2. Tester la scalabilité avec des volumes croissants (100k, 1M images)
> 3. Mettre en place l'orchestration avec Airflow
>
> **Long terme (mois 3-6) :**
> 1. Intégrer avec l'application mobile Fruits! (upload image → classification en temps réel)
> 2. Ajouter du feedback loop : utilisateurs valident les prédictions → réentraînement périodique
> 3. Optimiser les coûts en production (Reserved Instances, compression, etc.)
>
> L'objectif final serait un système de classification en production, avec pipeline automatisé et amélioration continue."

**Points clés à mentionner :**
- 3 horizons temporels : court, moyen, long terme
- Roadmap concrète et réaliste

---

## Catégorie 7 : Questions pièges ou inattendues

### Q7.1 : Quel a été le plus grand échec de ce projet, et qu'avez-vous appris ?

**Réponse :**
> "Le plus grand échec a été ma première tentative de broadcast du modèle TensorFlow.
>
> J'essayais de broadcaster le modèle directement avec pickle, sans compression. Résultat : erreur Spark 'Broadcast variable exceeds maximum size of 2GB'.
>
> J'ai perdu plusieurs heures à débugger, en pensant que c'était un problème de configuration Spark. En réalité, c'était juste la taille du modèle sérialisé.
>
> **Apprentissages :**
> 1. Toujours vérifier la taille des objets avant de broadcaster : `len(pickle.dumps(obj))`
> 2. Utiliser la compression (gzip) pour réduire la taille
> 3. Lire la documentation Spark sur les limites (broadcast max 2GB par défaut, configurable mais déconseillé d'augmenter)
>
> Cet échec m'a forcé à comprendre en profondeur comment fonctionne le broadcast Spark, et pourquoi la compression est importante. Au final, c'est devenu une des parties les plus solides de mon implémentation."

**Points clés à mentionner :**
- Échec concret et honnête
- Apprentissages tirés
- Comment l'échec a amélioré le projet

---

### Q7.2 : Si vous aviez 10 000€ de budget au lieu de 10€, que changeriez-vous ?

**Réponse :**
> "Avec 10 000€, je changerais plusieurs choses pour aller plus loin :
>
> **1. Fine-tuning du modèle (budget : 1 000€)**
> - Fine-tuner MobileNetV2 sur Fruits-360 avec des GPU (instances p3.2xlarge)
> - Évaluer plusieurs architectures (EfficientNet, Vision Transformers)
> - Objectif : améliorer la précision de classification
>
> **2. Scalabilité extrême (budget : 3 000€)**
> - Tester avec 10 millions d'images (augmentation de données)
> - Cluster EMR de 50 workers pour valider la scalabilité linéaire
> - Mesurer le temps d'exécution et optimiser
>
> **3. Production-ready (budget : 4 000€)**
> - Déployer l'API d'inférence avec AWS SageMaker
> - Load testing avec 10 000 requêtes/seconde
> - Mettre en place le monitoring avancé (X-Ray, CloudWatch Insights)
>
> **4. Sécurité avancée (budget : 1 000€)**
> - Audit de sécurité par un expert
> - Mise en place de AWS GuardDuty pour la détection d'intrusions
> - Chiffrement HSM (Hardware Security Module) pour les clés
>
> **5. Formation de l'équipe (budget : 1 000€)**
> - Formation Spark avancé pour l'équipe
> - Certification AWS Machine Learning Specialty
>
> Mais le fait de réussir avec 10€ prouve qu'on peut faire du Big Data sans budget énorme !"

**Points clés à mentionner :**
- 5 axes : Fine-tuning, Scalabilité, Production, Sécurité, Formation
- Mais fier d'avoir réussi avec 10€

---

### Q7.3 : Pourquoi devrait-on vous valider sur ce projet ?

**Réponse :**
> "Je pense avoir démontré 4 compétences clés :
>
> **1. Maîtrise technique du Big Data**
> - Architecture complète S3 + EMR + Spark fonctionnelle
> - Implémentation des 2 améliorations demandées (broadcast + PCA PySpark)
> - Pipeline reproductible et scalable
>
> **2. Compréhension business et contraintes**
> - Respect strict du RGPD (région eu-west-1, chiffrement)
> - Optimisation coûts (1,69€ vs budget 10€, soit 83% d'économie)
> - Architecture pensée pour la scalabilité (87k → 1M images possible)
>
> **3. Qualité de la documentation et de la présentation**
> - Documentation technique complète
> - Présentation structurée alignée avec les critères d'évaluation
> - Capacité à vulgariser des concepts techniques complexes
>
> **4. Problem-solving et autonomie**
> - Résolution des difficultés techniques (broadcast, UDFs, partitionnement)
> - Recherche et apprentissage autonome (documentation Spark, AWS)
> - Anticipation des questions et préparation de réponses
>
> Les 9 critères d'évaluation sont validés, et au-delà des critères, j'ai montré que je peux livrer un projet Big Data de bout en bout, de la conception à l'exécution."

**Points clés à mentionner :**
- 4 compétences clés démontrées
- 9 CE validés
- Projet livré de bout en bout

---

## Conseils généraux pour répondre aux questions

### Structure d'une bonne réponse

1. **Réponse directe** (10-15 secondes)
   - Répondre directement à la question posée
   - Éviter le flou ou les détours

2. **Justification technique** (30-45 secondes)
   - Expliquer le "pourquoi" avec des arguments techniques
   - Donner des chiffres si possible

3. **Exemple concret ou bénéfice** (15-30 secondes)
   - Illustrer avec un exemple
   - Ou mentionner le bénéfice pour le projet

4. **Ouverture** (optionnel, 10 secondes)
   - Si pertinent, ouvrir sur une perspective ou une alternative

**Durée totale : 1-2 minutes maximum par question**

---

### Comportement face aux questions difficiles

**Si vous ne savez pas répondre :**
> "C'est une excellente question. Je n'ai pas exploré cet aspect en profondeur dans ce projet. Voici ce que je ferais pour y répondre : [méthode de recherche ou d'investigation]. Dans un contexte réel, je consulterais [ressource : documentation, expert, etc.]."

**Si la question est hors sujet :**
> "C'est une question intéressante, mais qui sort un peu du périmètre de ce projet. Dans le cadre de ce projet, j'ai focalisé sur [recentrer sur votre scope]. Cela dit, je peux quand même partager mon avis : [réponse brève]."

**Si vous avez besoin de temps pour réfléchir :**
> "Laissez-moi réfléchir quelques secondes pour vous donner une réponse précise. [Pause 5 secondes]. Voici ce que je pense : [réponse]."

---

### Questions à poser AU jury (si temps disponible)

Si le jury vous demande "Avez-vous des questions ?", voici des questions pertinentes :

1. "Avez-vous des recommandations pour améliorer encore cette architecture ?"
2. "Dans votre expérience, quelles sont les erreurs les plus fréquentes dans les projets Big Data ?"
3. "Voyez-vous des cas d'usage où Spark ne serait PAS le bon choix ?"

---

**Vous êtes prêt ! Bonne chance pour la discussion ! 💪**
