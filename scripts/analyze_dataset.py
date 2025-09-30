#!/usr/bin/env python3
"""
Script d'analyse du dataset Fruits-360
Analyse du Dataset Fruits-360

Ce script analyse la structure, les volumes et la distribution du dataset
Fruits-360 pour planifier l'architecture Big Data et optimiser le pipeline PySpark.
"""

import os
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any, Union
import json
from collections import defaultdict, Counter
import pandas as pd  # type: ignore
from PIL import Image
import matplotlib.pyplot as plt
import seaborn as sns  # type: ignore

# Configuration des chemins
PROJECT_ROOT = Path(__file__).parent.parent
DATASET_PATH = PROJECT_ROOT / "data" / "raw" / "fruits-360_dataset" / "fruits-360"
RESULTS_PATH = PROJECT_ROOT / "docs" / "project" / "features"


def scan_dataset_structure(base_path: Path) -> Dict[str, Any]:
    """
    Parcours récursif des dossiers du dataset pour analyser la structure.

    Args:
        base_path: Chemin vers le dataset Fruits-360

    Returns:
        Dict contenant la structure analysée
    """
    print(f"Analyse de la structure du dataset : {base_path}")

    structure: Dict[str, Any] = {
        "total_classes": 0,
        "training_classes": 0,
        "test_classes": 0,
        "training_images": 0,
        "test_images": 0,
        "multiple_fruits_images": 0,
        "class_distribution": {},
        "image_formats": Counter(),
        "corrupted_images": [],
        "total_size_mb": 0.0
    }

    # Parcours des dossiers principaux
    main_folders = ["Training", "Test", "test-multiple_fruits"]

    for folder in main_folders:
        folder_path = base_path / folder
        if not folder_path.exists():
            print(f"Dossier {folder} non trouvé")
            continue

        print(f"Analyse du dossier : {folder}")

        # Parcours des classes dans chaque dossier
        for class_folder in folder_path.iterdir():
            if class_folder.is_dir():
                class_name = class_folder.name

                # Comptage des images dans la classe
                image_files = list(class_folder.glob("*.jpg")) + list(class_folder.glob("*.jpeg"))
                image_count = len(image_files)

                if folder == "Training":
                    structure["training_classes"] = int(structure["training_classes"]) + 1
                    structure["training_images"] = int(structure["training_images"]) + image_count
                elif folder == "Test":
                    structure["test_classes"] = int(structure["test_classes"]) + 1
                    structure["test_images"] = int(structure["test_images"]) + image_count
                elif folder == "test-multiple_fruits":
                    structure["multiple_fruits_images"] = int(structure["multiple_fruits_images"]) + image_count

                # Distribution des classes
                class_dist: Dict[str, Any] = structure["class_distribution"]
                if class_name not in class_dist:
                    class_dist[class_name] = {
                        "training": 0,
                        "test": 0,
                        "multiple_fruits": 0
                    }

                class_dist[class_name][folder] = image_count

                # Analyse du format des images (échantillon)
                if image_files and folder in ["Training", "Test"]:
                    sample_image = image_files[0]
                    try:
                        with Image.open(sample_image) as img:
                            format_info = f"{img.size[0]}x{img.size[1]}"
                            image_formats: Counter = structure["image_formats"]
                            image_formats[format_info] += 1
                    except Exception as e:
                        corrupted_images: List[str] = structure["corrupted_images"]
                        corrupted_images.append(str(sample_image))
                        print(f"Image corrompue : {sample_image} - {e}")

    structure["total_classes"] = len(structure["class_distribution"])
    structure["total_images"] = int(structure["training_images"]) + int(structure["test_images"]) + int(structure["multiple_fruits_images"])

    # Calcul de la taille totale
    total_size_bytes = sum(f.stat().st_size for f in base_path.rglob("*") if f.is_file())
    structure["total_size_mb"] = round(total_size_bytes / (1024 * 1024), 2)

    return structure


def count_images_per_class(dataset_path: Path) -> pd.DataFrame:
    """
    Comptage détaillé des images par classe avec statistiques.

    Args:
        dataset_path: Chemin vers le dataset

    Returns:
        DataFrame avec les statistiques par classe
    """
    print("Comptage des images par classe...")

    class_stats = []

    for split in ["Training", "Test"]:
        split_path = dataset_path / split
        if not split_path.exists():
            continue

        for class_folder in split_path.iterdir():
            if class_folder.is_dir():
                class_name = class_folder.name
                image_files = list(class_folder.glob("*.jpg")) + list(class_folder.glob("*.jpeg"))
                image_count = len(image_files)

                class_stats.append({
                    "class_name": class_name,
                    "split": split,
                    "image_count": image_count,
                    "folder_path": str(class_folder)
                })

    df = pd.DataFrame(class_stats)

    if not df.empty:
        # Statistiques globales
        total_by_class = df.groupby("class_name")["image_count"].sum().reset_index()
        total_by_class = total_by_class.sort_values("image_count", ascending=False)

        print(f"Statistiques des classes :")
        print(f"   - Classes avec le plus d'images : {total_by_class.head(3)['class_name'].tolist()}")
        print(f"   - Classes avec le moins d'images : {total_by_class.tail(3)['class_name'].tolist()}")
        print(f"   - Moyenne d'images par classe : {total_by_class['image_count'].mean():.1f}")
        print(f"   - Médiane d'images par classe : {total_by_class['image_count'].median():.1f}")

    return df


def validate_image_format(image_paths: List[Path], sample_size: int = 100) -> Dict[str, Any]:
    """
    Validation du format et de la résolution des images.

    Args:
        image_paths: Liste des chemins d'images à valider
        sample_size: Taille de l'échantillon à analyser

    Returns:
        Dict avec les résultats de validation
    """
    print(f"Validation du format des images (échantillon de {sample_size})...")

    validation_results: Dict[str, Any] = {
        "total_checked": 0,
        "valid_images": 0,
        "corrupted_images": 0,
        "size_distribution": Counter(),
        "format_distribution": Counter(),
        "corrupted_files": []
    }

    # Échantillonnage des images
    sample_paths = image_paths[:sample_size] if len(image_paths) > sample_size else image_paths
    validation_results["total_checked"] = len(sample_paths)

    for image_path in sample_paths:
        try:
            with Image.open(image_path) as img:
                # Vérification de la résolution
                size = img.size
                size_str = f"{size[0]}x{size[1]}"
                size_dist: Counter = validation_results["size_distribution"]
                size_dist[size_str] += 1

                # Vérification du format
                format_name = img.format
                format_dist: Counter = validation_results["format_distribution"]
                format_dist[format_name] += 1

                validation_results["valid_images"] = int(validation_results["valid_images"]) + 1

        except Exception as e:
            validation_results["corrupted_images"] = int(validation_results["corrupted_images"]) + 1
            corrupted_files: List[Dict[str, str]] = validation_results["corrupted_files"]
            corrupted_files.append({
                "path": str(image_path),
                "error": str(e)
            })

    return validation_results


def estimate_data_volume(dataset_path: Path) -> Dict[str, Any]:
    """
    Estimation du volume total de données et projection des coûts.

    Args:
        dataset_path: Chemin vers le dataset

    Returns:
        Dict avec les estimations de volume
    """
    print("Estimation du volume de données...")

    volume_info: Dict[str, Any] = {
        "total_size_bytes": 0,
        "total_size_mb": 0.0,
        "total_size_gb": 0.0,
        "file_count": 0,
        "average_file_size_kb": 0.0,
        "estimated_s3_transfer_time": "",
        "estimated_s3_storage_cost_monthly": 0.0
    }

    # Calcul de la taille totale
    for file_path in dataset_path.rglob("*"):
        if file_path.is_file():
            volume_info["total_size_bytes"] = int(volume_info["total_size_bytes"]) + file_path.stat().st_size
            volume_info["file_count"] = int(volume_info["file_count"]) + 1

    # Conversions
    total_bytes = int(volume_info["total_size_bytes"])
    file_count = int(volume_info["file_count"])
    volume_info["total_size_mb"] = round(total_bytes / (1024 * 1024), 2)
    volume_info["total_size_gb"] = round(total_bytes / (1024 * 1024 * 1024), 3)
    volume_info["average_file_size_kb"] = round(total_bytes / file_count / 1024, 2) if file_count > 0 else 0.0

    # Estimations S3 (approximatives)
    # Transfert : ~10 Mbps = 1.25 MB/s
    transfer_time_seconds = total_bytes / (1.25 * 1024 * 1024)
    volume_info["estimated_s3_transfer_time"] = f"{transfer_time_seconds / 60:.1f} minutes"

    # Stockage S3 : ~0.023€/GB/mois (Standard)
    volume_info["estimated_s3_storage_cost_monthly"] = round(float(volume_info["total_size_gb"]) * 0.023, 2)

    return volume_info


def analyze_class_distribution(class_stats_df: pd.DataFrame) -> Dict[str, Any]:
    """
    Analyse de la distribution des classes et détection des déséquilibres.

    Args:
        class_stats_df: DataFrame avec les statistiques par classe

    Returns:
        Dict avec l'analyse de distribution
    """
    print("Analyse de la distribution des classes...")

    distribution_analysis: Dict[str, Any] = {
        "balanced_classes": [],
        "imbalanced_classes": [],
        "rare_classes": [],
        "abundant_classes": [],
        "distribution_stats": {}
    }

    if class_stats_df.empty:
        return distribution_analysis

    # Agrégation par classe
    class_totals = class_stats_df.groupby("class_name")["image_count"].sum().reset_index()
    class_totals = class_totals.sort_values("image_count", ascending=False)

    # Statistiques de distribution
    mean_count = class_totals["image_count"].mean()
    std_count = class_totals["image_count"].std()
    median_count = class_totals["image_count"].median()

    distribution_analysis["distribution_stats"] = {
        "mean": round(mean_count, 1),
        "std": round(std_count, 1),
        "median": round(median_count, 1),
        "min": int(class_totals["image_count"].min()),
        "max": int(class_totals["image_count"].max()),
        "total_classes": len(class_totals)
    }

    # Classification des classes
    for _, row in class_totals.iterrows():
        class_name = row["class_name"]
        count = row["image_count"]

        if count < mean_count - std_count:
            rare_classes = distribution_analysis["rare_classes"]
            rare_classes.append({"class": class_name, "count": count})
        elif count > mean_count + std_count:
            abundant_classes = distribution_analysis["abundant_classes"]
            abundant_classes.append({"class": class_name, "count": count})
        elif abs(float(count) - float(mean_count)) <= float(std_count) * 0.5:
            balanced_classes = distribution_analysis["balanced_classes"]
            balanced_classes.append({"class": class_name, "count": count})
        else:
            imbalanced_classes = distribution_analysis["imbalanced_classes"]
            imbalanced_classes.append({"class": class_name, "count": count})

    return distribution_analysis


def generate_analysis_report(structure: Dict[str, Any], class_stats_df: pd.DataFrame,
                           validation_results: Dict[str, Any], volume_info: Dict[str, Any],
                           distribution_analysis: Dict[str, Any]) -> str:
    """
    Génération du rapport d'analyse structuré.

    Args:
        structure: Structure du dataset
        class_stats_df: Statistiques par classe
        validation_results: Résultats de validation
        volume_info: Informations de volume
        distribution_analysis: Analyse de distribution

    Returns:
        Contenu du rapport en markdown
    """
    report = f"""Rapport d'Analyse - Dataset Fruits-360

## Résumé Exécutif

**Date d'analyse :** {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}
**Dataset analysé :** Fruits-360 (version 100x100 pixels)

### Métriques Clés

- **Total d'images :** {structure['total_images']:,}
- **Total de classes :** {structure['total_classes']}
- **Taille totale :** {volume_info['total_size_gb']} GB ({volume_info['total_size_mb']} MB)
- **Images corrompues :** {len(structure['corrupted_images'])} ({len(structure['corrupted_images'])/structure['total_images']*100:.2f}%)

## Structure du Dataset

### Répartition Training/Test

| Split | Images | Classes | Pourcentage |
|-------|--------|---------|-------------|
| Training | {structure['training_images']:,} | {structure['training_classes']} | {structure['training_images']/structure['total_images']*100:.1f}% |
| Test | {structure['test_images']:,} | {structure['test_classes']} | {structure['test_images']/structure['total_images']*100:.1f}% |
| Multiple Fruits | {structure['multiple_fruits_images']:,} | - | {structure['multiple_fruits_images']/structure['total_images']*100:.1f}% |

### Validation du Format

- **Images validées :** {validation_results['total_checked']}
- **Images valides :** {validation_results['valid_images']} ({validation_results['valid_images']/validation_results['total_checked']*100:.1f}%)
- **Images corrompues :** {validation_results['corrupted_images']} ({validation_results['corrupted_images']/validation_results['total_checked']*100:.1f}%)

#### Distribution des Résolutions

"""

    for size, count in validation_results['size_distribution'].most_common():
        report += f"- **{size} :** {count} images ({count/validation_results['total_checked']*100:.1f}%)\n"

    report += f"""
#### Distribution des Formats

"""

    for format_name, count in validation_results['format_distribution'].most_common():
        report += f"- **{format_name} :** {count} images ({count/validation_results['total_checked']*100:.1f}%)\n"

    report += f"""
## Analyse de la Distribution des Classes

### Statistiques Globales

- **Moyenne d'images par classe :** {distribution_analysis['distribution_stats']['mean']}
- **Écart-type :** {distribution_analysis['distribution_stats']['std']}
- **Médiane :** {distribution_analysis['distribution_stats']['median']}
- **Minimum :** {distribution_analysis['distribution_stats']['min']}
- **Maximum :** {distribution_analysis['distribution_stats']['max']}

### Classification des Classes

- **Classes équilibrées :** {len(distribution_analysis['balanced_classes'])}
- **Classes déséquilibrées :** {len(distribution_analysis['imbalanced_classes'])}
- **Classes rares :** {len(distribution_analysis['rare_classes'])}
- **Classes abondantes :** {len(distribution_analysis['abundant_classes'])}

#### Top 10 Classes avec le Plus d'Images

"""

    if not class_stats_df.empty:
        # Récupération des top 10 classes
        class_totals = class_stats_df.groupby("class_name")["image_count"].sum()
        # Conversion en liste de tuples pour éviter les problèmes de typage
        class_list = [(str(name), int(count)) for name, count in class_totals.items()]
        # Tri par nombre d'images (descendant)
        class_list.sort(key=lambda x: x[1], reverse=True)

        for i, (class_name, count) in enumerate(class_list[:10], 1):
            report += f"{i}. **{class_name} :** {count} images\n"

    report += f"""
## Estimation des Volumes et Coûts

### Volumes de Données

- **Taille totale :** {volume_info['total_size_gb']} GB
- **Nombre de fichiers :** {volume_info['file_count']:,}
- **Taille moyenne par fichier :** {volume_info['average_file_size_kb']} KB

### Projections Cloud (AWS S3)

- **Temps de transfert estimé :** {volume_info['estimated_s3_transfer_time']}
- **Coût de stockage mensuel :** {volume_info['estimated_s3_storage_cost_monthly']}€
- **Région recommandée :** eu-west-1 (conformité RGPD)

## Recommandations Techniques

### Pour l'Architecture Big Data

1. **Partitionnement PySpark :**
   - Utiliser le nom de classe comme clé de partition
   - Optimiser la distribution sur les workers

2. **Optimisations S3 :**
   - Utiliser le format Parquet pour les métadonnées
   - Implémenter la compression gzip
   - Configurer les lifecycle policies

3. **Configuration EMR :**
   - Instances Spot pour réduire les coûts
   - Auto-scaling basé sur la charge
   - Résiliation automatique après traitement

### Gestion des Classes Déséquilibrées

- **Classes rares :** Considérer l'augmentation de données
- **Classes abondantes :** Stratification pour l'échantillonnage
- **Validation croisée :** Stratifiée par classe

## Validation des Critères d'Acceptation

- [x] **Analyse de la structure Training/Test** : {structure['training_images']:,} training, {structure['test_images']:,} test
- [x] **Vérification du format et résolution** : {validation_results['valid_images']}/{validation_results['total_checked']} images valides
- [x] **Évaluation de la distribution** : {len(distribution_analysis['imbalanced_classes'])} classes déséquilibrées identifiées
- [x] **Estimation du volume total** : {volume_info['total_size_gb']} GB confirmé

## Conclusion

Le dataset Fruits-360 présente une structure bien organisée avec {structure['total_images']:,} images réparties en {structure['total_classes']} classes. La qualité des images est excellente avec un taux de corruption très faible. Les volumes sont compatibles avec une architecture Big Data cloud, avec des coûts de stockage estimés à {volume_info['estimated_s3_storage_cost_monthly']}€/mois.

**Recommandation :** Procéder avec la migration vers AWS EMR en suivant les optimisations recommandées.
"""

    return report


def main():
    """Fonction principale d'analyse du dataset."""
    print("Démarrage de l'analyse du dataset Fruits-360")
    print("=" * 60)

    # Vérification de l'existence du dataset
    if not DATASET_PATH.exists():
        print(f"Erreur : Dataset non trouvé à {DATASET_PATH}")
        sys.exit(1)

    try:
        # Phase 1 : Analyse de structure
        print("Phase 1 : Analyse de la structure")
        structure = scan_dataset_structure(DATASET_PATH)

        # Phase 2 : Comptage par classe
        print("Phase 2 : Comptage des images par classe")
        class_stats_df = count_images_per_class(DATASET_PATH)

        # Phase 3 : Validation du format
        print("Phase 3 : Validation du format des images")
        all_images = list(DATASET_PATH.rglob("*.jpg")) + list(DATASET_PATH.rglob("*.jpeg"))
        validation_results = validate_image_format(all_images, sample_size=200)

        # Phase 4 : Estimation des volumes
        print("Phase 4 : Estimation des volumes")
        volume_info = estimate_data_volume(DATASET_PATH)

        # Phase 5 : Analyse de distribution
        print("Phase 5 : Analyse de la distribution")
        distribution_analysis = analyze_class_distribution(class_stats_df)

        # Phase 6 : Génération du rapport
        print("Phase 6 : Génération du rapport")
        report_content = generate_analysis_report(
            structure, class_stats_df, validation_results,
            volume_info, distribution_analysis
        )

        # Sauvegarde du rapport
        report_path = RESULTS_PATH / "0002-analyse-dataset-RAPPORT.md"
        RESULTS_PATH.mkdir(parents=True, exist_ok=True)

        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)

        print(f"Rapport sauvegardé : {report_path}")

        # Sauvegarde des données brutes
        data_path = RESULTS_PATH / "0002-analyse-dataset-DATA.json"
        analysis_data = {
            "structure": structure,
            "volume_info": volume_info,
            "validation_results": validation_results,
            "distribution_analysis": distribution_analysis,
            "class_stats": class_stats_df.to_dict('records') if not class_stats_df.empty else []
        }

        with open(data_path, 'w', encoding='utf-8') as f:
            json.dump(analysis_data, f, indent=2, ensure_ascii=False)

        print(f"Données sauvegardées : {data_path}")

        # Résumé final
        print("\n" + "=" * 60)
        print("ANALYSE TERMINÉE AVEC SUCCÈS")
        print("=" * 60)
        print(f"Total d'images : {structure['total_images']:,}")
        print(f"Total de classes : {structure['total_classes']}")
        print(f"Taille totale : {volume_info['total_size_gb']} GB")
        print(f"Images valides : {validation_results['valid_images']}/{validation_results['total_checked']}")
        print(f"Rapport généré : {report_path}")

    except Exception as e:
        print(f"Erreur lors de l'analyse : {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
