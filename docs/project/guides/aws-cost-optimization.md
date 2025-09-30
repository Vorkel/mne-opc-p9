# Guide d'Optimisation des Coûts AWS - Projet P9

## Vue d'ensemble

**Objectif :** Minimiser les coûts AWS pour le projet P9 tout en maintenant les performances
**Budget cible :** < 10€ pour l'ensemble du projet (développement + démonstration)
**Stratégie :** Optimisation maximale avec instances Spot et résiliation immédiate

## Stratégies d'Optimisation des Coûts

### 1. Instances Spot (PRIORITÉ ABSOLUE)

**Réduction :** Jusqu'à 90% des coûts
**Configuration recommandée :**

```yaml
# Configuration EMR avec instances Spot
InstanceGroups:
  - Name: "Master"
    InstanceRole: "MASTER"
    InstanceType: "m6g.xlarge" # Graviton2 pour économies supplémentaires
    Market: "SPOT"
    InstanceCount: 1

  - Name: "Workers"
    InstanceRole: "CORE"
    InstanceType: "m6g.large" # Graviton2
    Market: "SPOT"
    InstanceCount: 2
    AutoScalingPolicy:
      MinCapacity: 1
      MaxCapacity: 4
```

**Avantages :**

- Coût réduit de 60-90% par rapport aux instances On-Demand
- Parfait pour les tâches de traitement par batch
- Tolérance aux interruptions pour ce type de projet

**Risques et mitigation :**

- **Risque :** Interruption possible des instances
- **Mitigation :** Sauvegarde fréquente des résultats intermédiaires sur S3

### 2. Instances Graviton2

**Réduction :** 35% des coûts + 15% de performance
**Types recommandés :**

- **Master :** m6g.xlarge (4 vCPU, 16 GB RAM)
- **Workers :** m6g.large (2 vCPU, 8 GB RAM)

**Avantages :**

- Processeurs ARM optimisés par AWS
- Meilleur rapport prix/performance
- Compatible avec Spark et TensorFlow

### 3. Auto-scaling Intelligent

**Configuration :**

```yaml
AutoScalingPolicy:
  Rules:
    - Name: "ScaleOut"
      Action:
        Market: "SPOT"
        SimpleScalingPolicyConfiguration:
          AdjustmentType: "CHANGE_IN_CAPACITY"
          ScalingAdjustment: 1
          CoolDown: 300
      Trigger:
        CloudWatchAlarmDefinition:
          ComparisonOperator: "GREATER_THAN"
          EvaluationPeriods: 2
          MetricName: "YARNMemoryAvailablePercentage"
          Namespace: "AWS/ElasticMapReduce"
          Period: 300
          Statistic: "AVERAGE"
          Threshold: 15.0
          Unit: "PERCENT"
```

**Bénéfices :**

- Ajout automatique de workers en cas de charge élevée
- Réduction automatique pour économiser les coûts
- Utilisation optimale des ressources

### 4. Optimisation du Stockage

**S3 comme stockage principal :**

- **Coût :** ~0.023€/GB/mois (Standard)
- **Avantage :** Séparation stockage/calcul
- **Optimisation :** Pas de coût de stockage sur les instances EMR

**Formats optimisés :**

```python
# Conversion en Parquet pour optimiser les coûts
df.write.mode("overwrite") \
  .option("compression", "snappy") \
  .parquet("s3://fruits-bucket/processed-data/")
```

**Bénéfices :**

- Réduction de 50-80% de la taille des fichiers
- Amélioration des performances de lecture
- Diminution des coûts de transfert

### 5. Résiliation Immédiate

**Script d'arrêt automatique :**

```bash
#!/bin/bash
# auto-terminate.sh
echo "Traitement terminé - Arrêt du cluster dans 5 minutes"
sleep 300
aws emr terminate-clusters --cluster-ids $CLUSTER_ID
```

**Configuration :**

- Arrêt automatique après traitement
- Surveillance des coûts en temps réel
- Alertes si dépassement de budget

### 6. Monitoring et Alertes

**AWS Budgets :**

```yaml
Budget:
  BudgetName: "P9-Fruits-Project"
  BudgetLimit:
    Amount: "10"
    Unit: "USD"
  TimeUnit: "MONTHLY"
  BudgetType: "COST"
  CostFilters:
    Service:
      - "Amazon Elastic MapReduce"
      - "Amazon S3"
```

**CloudWatch Alarms :**

- Alerte à 5€ (50% du budget)
- Alerte à 8€ (80% du budget)
- Arrêt automatique à 10€

## Estimation des Coûts

### Coût par Heure (Instances Spot + Graviton2)

| Instance Type | Prix Spot (€/h) | Prix On-Demand (€/h) | Économie |
| ------------- | --------------- | -------------------- | -------- |
| m6g.xlarge    | 0.08            | 0.20                 | 60%      |
| m6g.large     | 0.04            | 0.10                 | 60%      |

### Estimation Totale du Projet

**Développement (5 jours × 1.5h/jour) :**

- Master (m6g.xlarge) : 7.5h × 0.08€ = 0.60€
- Workers (2×m6g.large) : 15h × 0.04€ = 0.60€
- **Total développement : 1.20€**

**Démonstration (1.5h) :**

- Master + Workers : 1.5h × 0.16€ = 0.24€
- **Total démonstration : 0.24€**

**Stockage S3 (1 mois) :**

- Dataset (10 GB) : 10 × 0.023€ = 0.23€
- Résultats (1 GB) : 1 × 0.023€ = 0.02€
- **Total stockage : 0.25€**

**TOTAL ESTIMÉ : 1.69€** (83% d'économie par rapport au budget de 10€)

## Checklist d'Optimisation

### Avant le Déploiement

- [ ] Configuration des instances Spot activée
- [ ] Sélection des instances Graviton2 (m6g.\*)
- [ ] Configuration de l'auto-scaling
- [ ] Script d'arrêt automatique prêt
- [ ] Budget AWS configuré avec alertes

### Pendant l'Exécution

- [ ] Surveillance des coûts en temps réel
- [ ] Vérification de l'utilisation des instances Spot
- [ ] Monitoring des performances
- [ ] Sauvegarde fréquente des résultats

### Après l'Exécution

- [ ] Résiliation immédiate du cluster
- [ ] Archivage des résultats sur S3
- [ ] Analyse des coûts réels
- [ ] Documentation des leçons apprises

## Commandes de Gestion des Coûts

### Vérification des Coûts

```bash
# Voir les coûts EMR du mois
aws ce get-cost-and-usage \
  --time-period Start=2024-01-01,End=2024-01-31 \
  --granularity MONTHLY \
  --metrics BlendedCost \
  --group-by Type=DIMENSION,Key=SERVICE
```

### Arrêt d'Urgence

```bash
# Arrêt immédiat du cluster
aws emr terminate-clusters --cluster-ids j-XXXXXXXXX
```

### Nettoyage S3

```bash
# Suppression des fichiers temporaires
aws s3 rm s3://fruits-bucket/temp/ --recursive
```

## Risques et Mitigation

| Risque               | Impact   | Probabilité | Mitigation                                    |
| -------------------- | -------- | ----------- | --------------------------------------------- |
| Interruption Spot    | Moyen    | Faible      | Sauvegarde fréquente, redémarrage automatique |
| Dépassement budget   | CRITIQUE | Très faible | Alertes automatiques, arrêt forcé à 10€       |
| Performance dégradée | Moyen    | Faible      | Monitoring, ajustement auto-scaling           |
| Coûts cachés         | Élevé    | Faible      | Surveillance stricte, nettoyage automatique   |

## Bonnes Pratiques (Budget 10€)

1. **Toujours utiliser des instances Spot** pour les tâches de traitement (PRIORITÉ ABSOLUE)
2. **Préférer les instances Graviton2** pour le meilleur rapport prix/performance
3. **Configurer l'auto-scaling** pour optimiser l'utilisation
4. **Surveiller les coûts en temps réel** avec des alertes strictes (5€, 8€, 10€)
5. **Résilier immédiatement** après traitement
6. **Archiver les résultats** sur S3 pour éviter les coûts de stockage EMR
7. **Utiliser des formats optimisés** (Parquet) pour réduire les coûts de traitement
8. **Limiter les heures d'utilisation** : 1.5h/jour max pour le développement
9. **Nettoyer automatiquement** tous les fichiers temporaires
10. **Vérifier quotidiennement** les coûts via AWS Cost Explorer

---

**Dernière mise à jour :** [Date]
**Responsable :** Data Scientist
**Budget approuvé :** 10€ maximum
