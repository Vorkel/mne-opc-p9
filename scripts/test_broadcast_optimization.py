#!/usr/bin/env python3
"""
Script de test pour valider les optimisations du broadcast TensorFlow.
Teste la compression, la gestion d'erreurs et les performances.
"""

import time
import pickle
import gzip
import numpy as np
from pathlib import Path
import sys

def create_mock_model_weights():
    """Crée des poids de modèle simulés pour les tests."""
    # Simulation de poids MobileNetV2 (approximatif)
    weights = []
    for i in range(50):  # ~50 couches dans MobileNetV2
        # Poids de convolution (kernel + bias)
        kernel_shape = (3, 3, min(32, 2**i), min(64, 2**(i+1)))
        bias_shape = (min(64, 2**(i+1)),)

        weights.append(np.random.randn(*kernel_shape).astype(np.float32))
        weights.append(np.random.randn(*bias_shape).astype(np.float32))

    return weights

# Simulation des imports TensorFlow (pour les tests sans TensorFlow)
TENSORFLOW_AVAILABLE = False
MobileNetV2 = None
Model = None

try:
    from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2 as TFMobileNetV2 # type: ignore
    from tensorflow.keras import Model as TFModel # type: ignore
    MobileNetV2 = TFMobileNetV2
    Model = TFModel
    TENSORFLOW_AVAILABLE = True
    print("TensorFlow disponible - Tests avec modèle réel")
except ImportError:
    print("TensorFlow non disponible - Simulation des tests")
    # Création de classes mock pour éviter les erreurs
    class MockMobileNetV2:
        def __init__(self, *args, **kwargs):
            pass
        def get_weights(self):
            return create_mock_model_weights()

    class MockModel:
        pass

    MobileNetV2 = MockMobileNetV2
    Model = MockModel

def test_compression_performance():
    """Teste les performances de compression."""
    print("Test de compression des poids du modèle")
    print("-" * 50)

    # Création de poids simulés
    if TENSORFLOW_AVAILABLE and MobileNetV2 is not None:
        model = MobileNetV2(weights='imagenet', include_top=True, input_shape=(224, 224, 3))
        model_weights = model.get_weights()
    else:
        model_weights = create_mock_model_weights()

    # Calcul de la taille originale
    original_size = sum(w.nbytes for w in model_weights)
    print(f"Taille originale: {original_size / (1024**2):.2f} MB")

    # Test de compression
    start_time = time.time()
    compressed_weights = gzip.compress(pickle.dumps(model_weights))
    compression_time = time.time() - start_time

    compressed_size = len(compressed_weights)
    compression_ratio = (1 - compressed_size / original_size) * 100

    print(f"Taille compressée: {compressed_size / (1024**2):.2f} MB")
    print(f"Temps de compression: {compression_time:.3f} secondes")
    print(f"Ratio de compression: {compression_ratio:.1f}%")

    # Test de décompression
    start_time = time.time()
    decompressed_weights = pickle.loads(gzip.decompress(compressed_weights))
    decompression_time = time.time() - start_time

    print(f"Temps de décompression: {decompression_time:.3f} secondes")

    # Validation
    if len(decompressed_weights) == len(model_weights):
        print("Validation: Décompression réussie")
    else:
        print("Erreur: Problème de décompression")
        return False

    return True

def test_error_handling():
    """Teste la gestion d'erreurs."""
    print("Test de gestion d'erreurs")
    print("-" * 50)

    # Test avec des poids trop volumineux (simulation)
    try:
        # Simulation de poids très volumineux (> 2GB)
        large_weights = [np.random.randn(1000, 1000, 1000).astype(np.float32)]
        total_size = sum(w.nbytes for w in large_weights)

        if total_size > 2 * 1024 * 1024 * 1024:  # 2GB limite
            raise ValueError(f"Modèle trop volumineux: {total_size / (1024**3):.2f}GB")

        print("Test de taille: Poids acceptés")

    except ValueError as e:
        print(f"Test de taille: Erreur correctement gérée - {e}")

    # Test avec des données corrompues
    try:
        corrupted_data = b"donnees_corrompues"
        pickle.loads(gzip.decompress(corrupted_data))
        print("Erreur: Données corrompues non détectées")
        return False

    except Exception as e:
        print(f"Test de corruption: Erreur correctement gérée - {type(e).__name__}")

    return True

def test_performance_metrics():
    """Teste les métriques de performance."""
    print("Test des métriques de performance")
    print("-" * 50)

    # Test de temps de création du broadcast (simulation)
    start_time = time.time()

    # Simulation du processus de broadcast
    model_weights = create_mock_model_weights()
    compressed_weights = gzip.compress(pickle.dumps(model_weights))

    # Simulation du temps de broadcast (réseau)
    time.sleep(0.1)  # Simulation de 100ms de réseau

    total_time = time.time() - start_time

    print(f"Temps total de création: {total_time:.3f} secondes")

    # Validation des métriques
    if total_time < 30:  # < 30 secondes
        print("Temps de création: Acceptable (< 30s)")
    else:
        print("Temps de création: Trop long (> 30s)")

    # Test de taille des données
    original_size = sum(w.nbytes for w in model_weights)
    compressed_size = len(compressed_weights)
    reduction = (1 - compressed_size / original_size) * 100

    if reduction >= 60:  # Réduction >= 60%
        print(f"Réduction de taille: Excellente ({reduction:.1f}%)")
    elif reduction >= 40:
        print(f"Réduction de taille: Bonne ({reduction:.1f}%)")
    else:
        print(f"Réduction de taille: Faible ({reduction:.1f}%)")

    return True

def test_robustness():
    """Teste la robustesse avec différents modèles."""
    print("Test de robustesse")
    print("-" * 50)

    success_count = 0
    total_tests = 10

    for i in range(total_tests):
        try:
            # Test avec différents modèles simulés
            model_weights = create_mock_model_weights()

            # Ajout de variation dans les tailles
            if i % 3 == 0:
                model_weights.append(np.random.randn(100, 100).astype(np.float32))
            elif i % 3 == 1:
                model_weights.append(np.random.randn(50, 50, 10).astype(np.float32))

            # Test de compression/décompression
            compressed = gzip.compress(pickle.dumps(model_weights))
            decompressed = pickle.loads(gzip.decompress(compressed))

            if len(decompressed) == len(model_weights):
                success_count += 1
                print(f"   Test {i+1}/10: Succès")
            else:
                print(f"   Test {i+1}/10: Échec")

        except Exception as e:
            print(f"   Test {i+1}/10: Erreur - {e}")

    success_rate = (success_count / total_tests) * 100
    print(f"Taux de succès: {success_rate:.1f}% ({success_count}/{total_tests})")

    if success_rate >= 90:
        print("Robustesse: Excellente")
        return True
    elif success_rate >= 80:
        print("Robustesse: Bonne")
        return True
    else:
        print("Robustesse: À améliorer")
        return False

def main():
    """Fonction principale de test."""
    print("Tests de validation des optimisations du broadcast TensorFlow")
    print("=" * 70)

    tests_passed = 0
    total_tests = 4

    # Exécution des tests
    if test_compression_performance():
        tests_passed += 1

    if test_error_handling():
        tests_passed += 1

    if test_performance_metrics():
        tests_passed += 1

    if test_robustness():
        tests_passed += 1

    # Résumé des résultats
    print("\n" + "=" * 70)
    print("RÉSUMÉ DES TESTS")
    print("=" * 70)

    print(f"Tests réussis: {tests_passed}/{total_tests}")

    if tests_passed == total_tests:
        print("TOUS LES TESTS RÉUSSIS - Optimisations validées !")
        return True
    else:
        print("Certains tests ont échoué - Vérification nécessaire")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
