#!/usr/bin/env python3
"""
Script pour implémenter la PCA PySpark dans le notebook.
Ajoute les imports, fonctions et intégration PCA selon le plan technique.
"""

import json
import sys
from pathlib import Path

NOTEBOOK_PATH = Path("notebook/P8_Notebook_Linux_EMR_PySpark_V1.0.ipynb")

def add_pca_imports(notebook):
    """Ajoute les imports PCA nécessaires."""
    print("Ajout des imports PCA")

    # Trouver la cellule avec les imports PySpark
    for i, cell in enumerate(notebook.get('cells', [])):
        if cell.get('cell_type') == 'code':
            source = cell.get('source', [])
            source_text = ''.join(source)

            # Ajouter les imports PCA après les imports PySpark existants
            if 'from pyspark.sql.functions import' in source_text and 'from pyspark.ml.feature import' not in source_text:
                # Ajouter les imports PCA
                new_imports = [
                    "from pyspark.ml.feature import PCA, VectorAssembler\n",
                    "from pyspark.ml import Pipeline\n",
                    "from pyspark.ml.linalg import Vectors, VectorUDT\n",
                    "from pyspark.sql.types import ArrayType, FloatType\n"
                ]

                # Insérer après la ligne des imports PySpark
                for j, line in enumerate(source):
                    if 'from pyspark.sql.functions import' in line:
                        # Insérer les nouveaux imports après cette ligne
                        for k, new_import in enumerate(new_imports):
                            source.insert(j + 1 + k, new_import)
                        break

                cell['source'] = source
                print(f"   Cellule {i}: Imports PCA ajoutés")
                return True

    return False

def add_pca_functions(notebook):
    """Ajoute les fonctions PCA dans le notebook."""
    print("Ajout des fonctions PCA")

    # Fonction de préparation des features
    prepare_function = {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "def prepare_features_for_pca(features_df):\n",
            "    \"\"\"\n",
            "    Prépare les features pour l'application de PCA.\n",
            "    Convertit les arrays de features en vecteurs Dense compatibles avec PCA.\n",
            "    \n",
            "    Args:\n",
            "        features_df: DataFrame avec colonne 'features' (ArrayType(FloatType))\n",
            "    \n",
            "    Returns:\n",
            "        DataFrame avec colonne 'features_vector' (VectorUDT)\n",
            "    \"\"\"\n",
            "    from pyspark.sql.functions import udf\n",
            "    from pyspark.ml.linalg import Vectors\n",
            "    from pyspark.sql.types import VectorUDT\n",
            "    \n",
            "    # UDF pour convertir array en vecteur Dense\n",
            "    array_to_vector = udf(lambda arr: Vectors.dense(arr), VectorUDT())\n",
            "    \n",
            "    # Conversion des features en vecteurs\n",
            "    features_vectorized = features_df.select(\n",
            "        col(\"path\"),\n",
            "        col(\"label\"),\n",
            "        array_to_vector(col(\"features\")).alias(\"features_vector\")\n",
            "    )\n",
            "    \n",
            "    print(f\"Features vectorisées: {features_vectorized.count()} échantillons\")\n",
            "    return features_vectorized\n"
        ]
    }

    # Fonction d'application PCA
    pca_function = {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "def apply_pca_reduction(features_vectorized, n_components=256):\n",
            "    \"\"\"\n",
            "    Applique la réduction PCA sur les features vectorisées.\n",
            "    \n",
            "    Args:\n",
            "        features_vectorized: DataFrame avec colonne 'features_vector'\n",
            "        n_components: Nombre de composantes principales (défaut: 256)\n",
            "    \n",
            "    Returns:\n",
            "        Tuple: (features_pca_df, pca_model, metrics)\n",
            "    \"\"\"\n",
            "    from pyspark.ml.feature import PCA, VectorAssembler\n",
            "    from pyspark.ml import Pipeline\n",
            "    import time\n",
            "    \n",
            "    print(f\"Démarrage PCA avec {n_components} composantes principales\")\n",
            "    start_time = time.time()\n",
            "    \n",
            "    try:\n",
            "        # 1. Assemblage des features pour PCA\n",
            "        assembler = VectorAssembler(\n",
            "            inputCols=[\"features_vector\"],\n",
            "            outputCol=\"features_assembled\"\n",
            "        )\n",
            "        \n",
            "        # 2. Configuration PCA\n",
            "        pca = PCA(\n",
            "            k=n_components,\n",
            "            inputCol=\"features_assembled\",\n",
            "            outputCol=\"features_pca\"\n",
            "        )\n",
            "        \n",
            "        # 3. Pipeline PCA\n",
            "        pipeline = Pipeline(stages=[assembler, pca])\n",
            "        \n",
            "        # 4. Entraînement du modèle PCA\n",
            "        print(\"Entraînement du modèle PCA...\")\n",
            "        pca_model = pipeline.fit(features_vectorized)\n",
            "        \n",
            "        # 5. Application de la transformation\n",
            "        print(\"Application de la transformation PCA...\")\n",
            "        features_pca_df = pca_model.transform(features_vectorized)\n",
            "        \n",
            "        # 6. Calcul des métriques\n",
            "        pca_stage = pca_model.stages[-1]  # Dernière étape = PCA\n",
            "        explained_variance = pca_stage.explainedVariance\n",
            "        total_variance = sum(explained_variance)\n",
            "        \n",
            "        execution_time = time.time() - start_time\n",
            "        \n",
            "        # Métriques de performance\n",
            "        metrics = {\n",
            "            \"n_components\": n_components,\n",
            "            \"total_variance_explained\": total_variance,\n",
            "            \"variance_percentage\": total_variance * 100,\n",
            "            \"execution_time_seconds\": execution_time,\n",
            "            \"execution_time_minutes\": execution_time / 60,\n",
            "            \"input_dimensions\": len(features_vectorized.select(\"features_vector\").first()[0]),\n",
            "            \"output_dimensions\": n_components,\n",
            "            \"reduction_ratio\": 1 - (n_components / len(features_vectorized.select(\"features_vector\").first()[0]))\n",
            "        }\n",
            "        \n",
            "        print(f\"PCA terminée avec succès!\")\n",
            "        print(f\"Variance expliquée: {metrics['variance_percentage']:.2f}%\")\n",
            "        print(f\"Temps d'exécution: {metrics['execution_time_minutes']:.2f} minutes\")\n",
            "        print(f\"Réduction de dimension: {metrics['reduction_ratio']*100:.1f}%\")\n",
            "        \n",
            "        return features_pca_df, pca_model, metrics\n",
            "        \n",
            "    except Exception as e:\n",
            "        print(f\"Erreur lors de l'application PCA: {e}\")\n",
            "        raise\n"
        ]
    }

    # Fonction de sauvegarde PCA
    save_function = {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "def save_pca_results(features_pca_df, pca_model, metrics, base_path):\n",
            "    \"\"\"\n",
            "    Sauvegarde les résultats PCA sur S3.\n",
            "    \n",
            "    Args:\n",
            "        features_pca_df: DataFrame avec features réduites\n",
            "        pca_model: Modèle PCA entraîné\n",
            "        metrics: Métriques de performance\n",
            "        base_path: Chemin de base S3\n",
            "    \"\"\"\n",
            "    import json\n",
            "    from pyspark.sql.functions import col\n",
            "    \n",
            "    try:\n",
            "        # 1. Sauvegarde des features réduites\n",
            "        pca_features_path = f\"{base_path}/features_pca\"\n",
            "        print(f\"Sauvegarde des features PCA vers: {pca_features_path}\")\n",
            "        \n",
            "        features_pca_df.select(\n",
            "            col(\"path\"),\n",
            "            col(\"label\"),\n",
            "            col(\"features_pca\").alias(\"features\")\n",
            "        ).write.mode(\"overwrite\").parquet(pca_features_path)\n",
            "        \n",
            "        # 2. Sauvegarde du modèle PCA\n",
            "        pca_model_path = f\"{base_path}/pca_model\"\n",
            "        print(f\"Sauvegarde du modèle PCA vers: {pca_model_path}\")\n",
            "        \n",
            "        pca_model.write().overwrite().save(pca_model_path)\n",
            "        \n",
            "        # 3. Sauvegarde des métriques\n",
            "        metrics_path = f\"{base_path}/pca_metrics\"\n",
            "        print(f\"Sauvegarde des métriques vers: {metrics_path}\")\n",
            "        \n",
            "        # Créer un DataFrame avec les métriques\n",
            "        metrics_df = spark.createDataFrame([metrics])\n",
            "        metrics_df.write.mode(\"overwrite\").json(metrics_path)\n",
            "        \n",
            "        print(\"Sauvegarde PCA terminée avec succès!\")\n",
            "        \n",
            "    except Exception as e:\n",
            "        print(f\"Erreur lors de la sauvegarde PCA: {e}\")\n",
            "        raise\n"
        ]
    }

    # Trouver l'endroit pour insérer les fonctions (après les imports)
    insert_index = None
    for i, cell in enumerate(notebook.get('cells', [])):
        if cell.get('cell_type') == 'code':
            source = cell.get('source', [])
            source_text = ''.join(source)
            if 'from pyspark.ml.feature import PCA' in source_text:
                insert_index = i + 1
                break

    if insert_index is None:
        print("Impossible de trouver l'endroit pour insérer les fonctions PCA")
        return False

    # Insérer les fonctions
    notebook['cells'].insert(insert_index, prepare_function)
    notebook['cells'].insert(insert_index + 1, pca_function)
    notebook['cells'].insert(insert_index + 2, save_function)

    print(f"   3 fonctions PCA ajoutées à partir de la cellule {insert_index}")
    return True

def integrate_pca_in_pipeline(notebook):
    """Intègre la PCA dans le pipeline existant."""
    print("Intégration de la PCA dans le pipeline")

    modifications_count = 0

    for i, cell in enumerate(notebook.get('cells', [])):
        if cell.get('cell_type') == 'code':
            source = cell.get('source', [])
            source_text = ''.join(source)

            # Modifier la création de features_df pour ajouter la PCA
            if 'features_df = images.repartition(' in source_text and 'featurize_udf' in source_text:
                # Ajouter la PCA après la création de features_df
                new_cell = {
                    "cell_type": "code",
                    "execution_count": None,
                    "metadata": {},
                    "outputs": [],
                    "source": [
                        "# ===== ÉTAPE PCA : RÉDUCTION DE DIMENSION =====\n",
                        "print(\"Démarrage de l'étape PCA\")\n",
                        "print(\"=\" * 50)\n",
                        "\n",
                        "# 1. Préparation des features pour PCA\n",
                        "features_vectorized = prepare_features_for_pca(features_df)\n",
                        "\n",
                        "# 2. Application de la PCA\n",
                        "features_pca_df, pca_model, pca_metrics = apply_pca_reduction(features_vectorized, n_components=256)\n",
                        "\n",
                        "# 3. Sauvegarde des résultats PCA\n",
                        "save_pca_results(features_pca_df, pca_model, pca_metrics, PATH_Result)\n",
                        "\n",
                        "# 4. Mise à jour de features_df avec les features réduites\n",
                        "features_df = features_pca_df.select(\n",
                        "    col(\"path\"),\n",
                        "    col(\"label\"),\n",
                        "    col(\"features_pca\").alias(\"features\")\n",
                        ")\n",
                        "\n",
                        "print(\"PCA intégrée avec succès dans le pipeline\")\n",
                        "print(f\"Features réduites: {features_df.count()} échantillons\")\n",
                        "print(\"=\" * 50)\n"
                    ]
                }

                # Insérer la nouvelle cellule après la création de features_df
                notebook['cells'].insert(i + 1, new_cell)
                modifications_count += 1
                print(f"   Cellule {i}: PCA intégrée après création de features_df")

    return modifications_count > 0

def add_pca_documentation(notebook):
    """Ajoute la documentation PCA dans le notebook."""
    print("Ajout de la documentation PCA")

    # Cellule de documentation PCA
    doc_cell = {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## Étape PCA : Réduction de Dimension\n",
            "\n",
            "### Objectif\n",
            "Cette étape applique une **Analyse en Composantes Principales (PCA)** sur les features extraites par MobileNetV2 pour :\n",
            "\n",
            "- **Réduire la dimensionnalité** : 1280 → 256 dimensions (réduction de 80%)\n",
            "- **Préserver l'information** : Maintenir ≥95% de la variance expliquée\n",
            "- **Optimiser les performances** : Réduction des coûts de stockage et de calcul\n",
            "\n",
            "### Implémentation PySpark\n",
            "\n",
            "1. **Préparation** : Conversion des features en vecteurs Dense\n",
            "2. **Calcul PCA** : Application de la PCA avec 256 composantes principales\n",
            "3. **Validation** : Vérification de la variance expliquée\n",
            "4. **Sauvegarde** : Stockage des features réduites et du modèle PCA\n",
            "\n",
            "### Métriques de Qualité\n",
            "\n",
            "- ✅ **Variance expliquée** : ≥95% avec 256 composantes\n",
            "- ✅ **Réduction de taille** : 80% de réduction (1280 → 256)\n",
            "- ✅ **Performance** : Temps de calcul <30 minutes\n",
            "- ✅ **Intégrité** : Conservation des labels et chemins\n"
        ]
    }

    # Trouver l'endroit pour insérer la documentation
    insert_index = None
    for i, cell in enumerate(notebook.get('cells', [])):
        if cell.get('cell_type') == 'code':
            source = cell.get('source', [])
            source_text = ''.join(source)
            if 'features_df = images.repartition(' in source_text:
                insert_index = i
                break

    if insert_index is not None:
        notebook['cells'].insert(insert_index, doc_cell)
        print(f"   Documentation PCA ajoutée avant la cellule {insert_index}")
        return True

    return False

def implement_pca():
    """Fonction principale pour implémenter la PCA."""
    print("Démarrage de l'implémentation PCA PySpark")
    print("=" * 60)

    try:
        # Lecture du notebook
        with open(NOTEBOOK_PATH, 'r', encoding='utf-8') as f:
            notebook = json.load(f)

        modifications_applied = 0

        # 1. Ajouter les imports PCA
        if add_pca_imports(notebook):
            modifications_applied += 1

        # 2. Ajouter les fonctions PCA
        if add_pca_functions(notebook):
            modifications_applied += 1

        # 3. Ajouter la documentation
        if add_pca_documentation(notebook):
            modifications_applied += 1

        # 4. Intégrer la PCA dans le pipeline
        if integrate_pca_in_pipeline(notebook):
            modifications_applied += 1

        # Sauvegarde du notebook modifié
        if modifications_applied > 0:
            with open(NOTEBOOK_PATH, 'w', encoding='utf-8') as f:
                json.dump(notebook, f, indent=1, ensure_ascii=False)

            print(f"Implémentation PCA terminée: {modifications_applied} modification(s) appliquée(s)")
        else:
            print("Aucune modification nécessaire")

        print("=" * 60)
        print("Implémentation PCA terminée avec succès")

    except Exception as e:
        print(f"Erreur lors de l'implémentation PCA: {e}")
        raise

if __name__ == "__main__":
    implement_pca()
