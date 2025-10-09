"""
Génération du graphique de variance PCA pour la présentation.

Ce script peut être exécuté:
1. Dans le notebook JupyterHub EMR (après PCA)
2. Localement avec des données simulées ou réelles

Usage dans notebook EMR (après PCA):
    python generate_pca_variance_plot.py --from-model pca_model

Usage local avec valeurs réelles:
    python generate_pca_variance_plot.py --variance-values "0.15,0.12,0.10,..."

Usage local avec simulation:
    python generate_pca_variance_plot.py --simulate --n-components 256
"""

import argparse
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def generate_simulated_variance(n_components: int, target_cumsum: float = 0.92) -> np.ndarray:
    """
    Génère des valeurs de variance simulées qui suivent une décroissance exponentielle.

    Args:
        n_components: Nombre de composantes PCA
        target_cumsum: Variance cumulée cible (ex: 0.92 pour 92%)

    Returns:
        Array de valeurs de variance (somme = target_cumsum)
    """
    # Génération décroissance exponentielle
    x = np.arange(1, n_components + 1)
    variance = np.exp(-x / 50)  # Décroissance exponentielle

    # Normalisation pour atteindre target_cumsum
    variance = variance / variance.sum() * target_cumsum

    return variance


def create_pca_variance_plot(
    variance_values: np.ndarray,
    output_path: str = "variance_pca.png",
    title: str = "Variance Expliquée par PCA - Fruits Classification",
    figsize: tuple = (12, 7),
    dpi: int = 300,
) -> None:
    """
    Crée le graphique de variance PCA pour la présentation.

    Args:
        variance_values: Array des valeurs de variance par composante
        output_path: Chemin du fichier de sortie
        title: Titre du graphique
        figsize: Taille de la figure (width, height)
        dpi: Résolution (300 pour haute qualité)
    """
    # Calcul variance cumulative
    cumulative_variance = np.cumsum(variance_values)

    # Création figure
    plt.figure(figsize=figsize)

    # Graphique variance cumulative
    plt.plot(
        range(1, len(cumulative_variance) + 1),
        cumulative_variance,
        linewidth=2.5,
        color="#1E3A8A",
        label="Variance cumulative",
    )

    # Ligne seuil 90%
    plt.axhline(
        y=0.9,
        color="#DC2626",
        linestyle="--",
        linewidth=2,
        label="Seuil 90%",
        alpha=0.8,
    )

    # Ligne seuil 95% (optionnel)
    if cumulative_variance[-1] >= 0.95:
        plt.axhline(
            y=0.95,
            color="#F97316",
            linestyle=":",
            linewidth=1.5,
            label="Seuil 95%",
            alpha=0.6,
        )

    # Marqueur à 256 composantes
    if len(cumulative_variance) >= 256:
        variance_at_256 = cumulative_variance[255]
        plt.plot(
            256,
            variance_at_256,
            marker="o",
            markersize=10,
            color="#DC2626",
            zorder=5,
        )
        plt.annotate(
            f"256 composantes\nVariance: {variance_at_256:.1%}",
            xy=(256, variance_at_256),
            xytext=(256 + 20, variance_at_256 - 0.05),
            fontsize=11,
            fontweight="bold",
            bbox={
                "boxstyle": "round,pad=0.5",
                "facecolor": "white",
                "edgecolor": "#DC2626",
                "linewidth": 2,
            },
            arrowprops={"arrowstyle": "->", "color": "#DC2626", "lw": 2},
        )

    # Labels et titre
    plt.xlabel(
        "Nombre de composantes principales", fontsize=14, fontweight="bold"
    )
    plt.ylabel(
        "Variance expliquée cumulative", fontsize=14, fontweight="bold"
    )
    plt.title(title, fontsize=16, fontweight="bold", pad=20)

    # Légende
    plt.legend(fontsize=12, loc="lower right", framealpha=0.9)

    # Grille
    plt.grid(True, alpha=0.3, linestyle="--", linewidth=0.5)

    # Limites axes
    plt.xlim(0, len(cumulative_variance))
    plt.ylim(0, 1.05)

    # Format axes
    plt.gca().yaxis.set_major_formatter(
        plt.FuncFormatter(lambda y, _: f"{y:.0%}")
    )

    # Serrer layout
    plt.tight_layout()

    # Sauvegarde
    plt.savefig(output_path, dpi=dpi, bbox_inches="tight", facecolor="white")
    print(f"✅ Graphique sauvegardé : {output_path}")

    # Statistiques
    print(f"\n📊 Statistiques :")
    print(f"  Nombre de composantes : {len(variance_values)}")
    print(f"  Variance finale : {cumulative_variance[-1]:.2%}")

    if len(cumulative_variance) >= 256:
        print(f"  Variance à 256 composantes : {cumulative_variance[255]:.2%}")

    # Trouver nombre de composantes pour 90% et 95%
    idx_90 = np.argmax(cumulative_variance >= 0.9)
    if idx_90 > 0:
        print(f"  Composantes pour 90% variance : {idx_90 + 1}")

    idx_95 = np.argmax(cumulative_variance >= 0.95)
    if idx_95 > 0 and cumulative_variance[-1] >= 0.95:
        print(f"  Composantes pour 95% variance : {idx_95 + 1}")

    # Afficher (si interactif)
    # plt.show()


def load_variance_from_string(variance_str: str) -> np.ndarray:
    """
    Charge les valeurs de variance depuis une chaîne de caractères.

    Args:
        variance_str: String de valeurs séparées par virgules "0.15,0.12,0.10,..."

    Returns:
        Array numpy de valeurs de variance
    """
    values = [float(v.strip()) for v in variance_str.split(",")]
    return np.array(values)


def load_variance_from_json(json_path: str) -> np.ndarray:
    """
    Charge les valeurs de variance depuis un fichier JSON.

    Args:
        json_path: Chemin du fichier JSON contenant 'explained_variance'

    Returns:
        Array numpy de valeurs de variance
    """
    with Path(json_path).open() as f:
        data = json.load(f)

    return np.array(data["explained_variance"])


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Génère le graphique de variance PCA"
    )

    # Source des données
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument(
        "--simulate",
        action="store_true",
        help="Générer des données simulées",
    )
    source.add_argument(
        "--variance-values",
        type=str,
        help='Valeurs de variance séparées par virgules "0.15,0.12,..."',
    )
    source.add_argument(
        "--from-json",
        type=str,
        help="Charger depuis fichier JSON",
    )

    # Paramètres
    parser.add_argument(
        "--n-components",
        type=int,
        default=256,
        help="Nombre de composantes (si --simulate)",
    )
    parser.add_argument(
        "--target-variance",
        type=float,
        default=0.92,
        help="Variance cumulée cible (si --simulate)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="variance_pca.png",
        help="Chemin du fichier de sortie",
    )
    parser.add_argument(
        "--title",
        type=str,
        default="Variance Expliquée par PCA - Fruits Classification",
        help="Titre du graphique",
    )
    parser.add_argument(
        "--dpi",
        type=int,
        default=300,
        help="Résolution DPI (300 recommandé)",
    )

    args = parser.parse_args()

    # Charger variance selon source
    if args.simulate:
        print(f"📊 Génération de données simulées ({args.n_components} composantes)...")
        variance = generate_simulated_variance(
            args.n_components, args.target_variance
        )
    elif args.variance_values:
        print("📊 Chargement des valeurs depuis string...")
        variance = load_variance_from_string(args.variance_values)
    elif args.from_json:
        print(f"📊 Chargement depuis {args.from_json}...")
        variance = load_variance_from_json(args.from_json)

    # Créer graphique
    create_pca_variance_plot(
        variance_values=variance,
        output_path=args.output,
        title=args.title,
        dpi=args.dpi,
    )


# Code pour utilisation dans notebook JupyterHub EMR
def create_plot_from_pca_model(pca_model, output_path: str = "variance_pca.png"):
    """
    Fonction helper pour utilisation directe dans le notebook EMR.

    Usage dans notebook:
        from generate_pca_variance_plot import create_plot_from_pca_model

        # Après avoir fit le modèle PCA
        create_plot_from_pca_model(pca_model, "variance_pca.png")

    Args:
        pca_model: Modèle PySpark PCA déjà fit
        output_path: Chemin de sortie
    """
    # Extraire variance expliquée
    variance = np.array(pca_model.explainedVariance)

    # Créer graphique
    create_pca_variance_plot(
        variance_values=variance, output_path=output_path
    )

    print(f"\n📥 Téléchargement du graphique :")
    print(f"  JupyterHub → Clic droit sur '{output_path}' → Download")
    print(f"  Destination : docs/soutenance/visuels/{output_path}")


if __name__ == "__main__":
    main()
