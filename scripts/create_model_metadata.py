"""Script to create model metadata files for versioning."""

import argparse
import json
from datetime import datetime
from pathlib import Path


def create_pca_metadata(
    version: str,
    variance_explained: float,
    n_components: int,
    n_samples: int,
    input_features: int = 1280,
    description: str = "",
) -> dict:
    """
    Create PCA model metadata.

    Args:
        version: Semantic version (e.g., "1.0")
        variance_explained: Proportion of variance retained
        n_components: Number of PCA components
        n_samples: Number of training samples
        input_features: Number of input features (default: 1280)
        description: Model description

    Returns:
        Dictionary with metadata
    """
    date = datetime.now().strftime("%Y-%m-%d")
    date_short = datetime.now().strftime("%Y%m%d")

    metadata = {
        "version": version,
        "date": date,
        "model_type": "PCA",
        "description": description
        or f"PCA reduction model v{version} for MobileNetV2 features",
        "parameters": {
            "n_components": n_components,
            "variance_explained": variance_explained,
            "input_features": input_features,
            "output_features": n_components,
        },
        "training": {
            "n_samples": n_samples,
            "dataset": "Fruits-360",
            "feature_extractor": "MobileNetV2",
            "execution_platform": "AWS EMR 7.10.0",
            "instance_type": "m5.2xlarge",
        },
        "performance": {
            "explained_variance_ratio": variance_explained,
            "dimension_reduction_ratio": n_components / input_features,
            "compression_rate": input_features / n_components,
        },
        "files": {
            "model": f"s3://fruits-classification-p9-mne/Models/pca_model_v{version.replace('.', '_')}.pkl",
            "features": "s3://fruits-classification-p9-mne/Results/",
            "reduced_features": f"s3://fruits-classification-p9-mne/Results_PCA_v{version.replace('.', '_')}/",
        },
        "metadata": {
            "author": "Maxime Nejad",
            "project": "P9 - Fruits Classification",
            "created_at": datetime.now().isoformat() + "Z",
            "framework_versions": {
                "pyspark": "3.5.5",
                "tensorflow": "2.18.0",
                "scikit-learn": "1.3.2",
            },
        },
    }

    return metadata


def save_metadata(metadata: dict, output_dir: Path = Path("models")) -> Path:
    """
    Save metadata to JSON file.

    Args:
        metadata: Metadata dictionary
        output_dir: Output directory (default: models/)

    Returns:
        Path to created file
    """
    output_dir.mkdir(exist_ok=True)

    version = metadata["version"].replace(".", "_")
    date_short = datetime.now().strftime("%Y%m%d")
    filename = f"pca_v{version}_{date_short}.json"
    filepath = output_dir / filename

    with filepath.open("w") as f:
        json.dump(metadata, f, indent=2)

    return filepath


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Create PCA model metadata for versioning",
    )
    parser.add_argument(
        "--version", required=True, help='Semantic version (e.g., "1.0")',
    )
    parser.add_argument(
        "--variance",
        type=float,
        required=True,
        help="Explained variance ratio (e.g., 0.92)",
    )
    parser.add_argument(
        "--n-components",
        type=int,
        default=256,
        help="Number of PCA components (default: 256)",
    )
    parser.add_argument(
        "--n-samples",
        type=int,
        required=True,
        help="Number of training samples",
    )
    parser.add_argument(
        "--input-features",
        type=int,
        default=1280,
        help="Number of input features (default: 1280)",
    )
    parser.add_argument(
        "--description",
        default="",
        help="Optional model description",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("models"),
        help="Output directory (default: models/)",
    )

    args = parser.parse_args()

    # Create metadata
    metadata = create_pca_metadata(
        version=args.version,
        variance_explained=args.variance,
        n_components=args.n_components,
        n_samples=args.n_samples,
        input_features=args.input_features,
        description=args.description,
    )

    # Save to file
    filepath = save_metadata(metadata, args.output_dir)

    print(f"✅ Metadata created: {filepath}")
    print("\nSummary:")
    print(f"  Version: {metadata['version']}")
    print(f"  Variance: {metadata['parameters']['variance_explained']:.2%}")
    print(f"  Dimensions: {metadata['parameters']['input_features']} → {metadata['parameters']['output_features']}")
    print(f"  Samples: {metadata['training']['n_samples']:,}")
    print(f"  S3 Model: {metadata['files']['model']}")


if __name__ == "__main__":
    main()
