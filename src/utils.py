"""Utility functions for model weights compression and image processing."""

import gzip
import pickle

import numpy as np


def compress_weights(weights: list[np.ndarray]) -> bytes:
    """
    Compress model weights using gzip.

    Args:
        weights: List of numpy arrays representing model weights

    Returns:
        Compressed bytes representation of the weights

    Example:
        >>> model = MobileNetV2(weights='imagenet')
        >>> weights = model.get_weights()
        >>> compressed = compress_weights(weights)
        >>> len(compressed) < sum(w.nbytes for w in weights)
        True
    """
    serialized = pickle.dumps(weights)
    return gzip.compress(serialized)


def decompress_weights(compressed_weights: bytes) -> list[np.ndarray]:
    """
    Decompress model weights.

    Args:
        compressed_weights: Compressed bytes representation of weights

    Returns:
        List of numpy arrays representing model weights

    Example:
        >>> original_weights = [np.random.rand(3, 3)]
        >>> compressed = compress_weights(original_weights)
        >>> decompressed = decompress_weights(compressed)
        >>> np.allclose(original_weights[0], decompressed[0])
        True
    """
    decompressed = gzip.decompress(compressed_weights)
    return pickle.loads(decompressed)  # noqa: S301


def validate_image_dimensions(
    image: np.ndarray, expected_shape: tuple[int, int, int] = (224, 224, 3),
) -> bool:
    """
    Validate that an image has the expected dimensions.

    Args:
        image: Numpy array representing an image
        expected_shape: Expected (height, width, channels) tuple

    Returns:
        True if image dimensions match, False otherwise

    Example:
        >>> img = np.random.rand(224, 224, 3)
        >>> validate_image_dimensions(img)
        True
        >>> img_wrong = np.random.rand(100, 100, 3)
        >>> validate_image_dimensions(img_wrong)
        False
    """
    return image.shape == expected_shape


def normalize_image(image: np.ndarray) -> np.ndarray:
    """
    Normalize image to [0, 1] range.

    Args:
        image: Numpy array representing an image

    Returns:
        Normalized image array

    Example:
        >>> img = np.array([[[255, 128, 0]]], dtype=np.uint8)
        >>> normalized = normalize_image(img)
        >>> np.allclose(normalized, [[[1.0, 0.5019608, 0.0]]])
        True
    """
    return image.astype(np.float32) / 255.0
