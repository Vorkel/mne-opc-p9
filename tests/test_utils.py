"""Unit tests for utility functions."""

import numpy as np

from src.utils import (
    compress_weights,
    decompress_weights,
    normalize_image,
    validate_image_dimensions,
)


class TestWeightCompression:
    """Tests for weight compression/decompression functions."""

    def test_compress_decompress_roundtrip(self):
        """Test that compress -> decompress returns identical weights."""
        # Create sample weights
        original_weights = [
            np.random.rand(3, 3, 32, 64).astype(np.float32),
            np.random.rand(64).astype(np.float32),
        ]

        # Compress and decompress
        compressed = compress_weights(original_weights)
        decompressed = decompress_weights(compressed)

        # Verify roundtrip
        assert len(decompressed) == len(original_weights)
        for original, recovered in zip(original_weights, decompressed):
            np.testing.assert_array_equal(original, recovered)

    def test_compression_reduces_size(self):
        """Test that compression actually reduces data size."""
        # Create weights with repeated patterns (compressible)
        weights = [np.ones((100, 100), dtype=np.float32)]

        compressed = compress_weights(weights)
        import pickle

        uncompressed_size = len(pickle.dumps(weights))

        # Compression should significantly reduce size for repeated data
        assert len(compressed) < uncompressed_size

    def test_compress_empty_weights(self):
        """Test compression of empty weights list."""
        weights = []
        compressed = compress_weights(weights)
        decompressed = decompress_weights(compressed)
        assert decompressed == []

    def test_compress_single_value(self):
        """Test compression of single scalar in array."""
        weights = [np.array([42.0], dtype=np.float32)]
        compressed = compress_weights(weights)
        decompressed = decompress_weights(compressed)
        np.testing.assert_array_equal(weights[0], decompressed[0])


class TestImageValidation:
    """Tests for image validation functions."""

    def test_validate_correct_dimensions(self):
        """Test validation passes for correct image dimensions."""
        img = np.random.rand(224, 224, 3)
        assert validate_image_dimensions(img) is True

    def test_validate_incorrect_height(self):
        """Test validation fails for incorrect height."""
        img = np.random.rand(100, 224, 3)
        assert validate_image_dimensions(img) is False

    def test_validate_incorrect_width(self):
        """Test validation fails for incorrect width."""
        img = np.random.rand(224, 100, 3)
        assert validate_image_dimensions(img) is False

    def test_validate_incorrect_channels(self):
        """Test validation fails for incorrect number of channels."""
        img = np.random.rand(224, 224, 1)
        assert validate_image_dimensions(img) is False

    def test_validate_custom_dimensions(self):
        """Test validation with custom expected dimensions."""
        img = np.random.rand(100, 100, 3)
        assert validate_image_dimensions(img, expected_shape=(100, 100, 3)) is True

    def test_validate_2d_image_fails(self):
        """Test validation fails for 2D grayscale image."""
        img = np.random.rand(224, 224)
        assert validate_image_dimensions(img) is False


class TestImageNormalization:
    """Tests for image normalization functions."""

    def test_normalize_uint8_image(self):
        """Test normalization of uint8 image to [0, 1] range."""
        img = np.array([[[255, 128, 0]]], dtype=np.uint8)
        normalized = normalize_image(img)

        assert normalized.dtype == np.float32
        assert normalized.min() >= 0.0
        assert normalized.max() <= 1.0
        np.testing.assert_allclose(normalized[0, 0, 0], 1.0, rtol=1e-5)
        np.testing.assert_allclose(normalized[0, 0, 1], 128 / 255, rtol=1e-5)
        np.testing.assert_allclose(normalized[0, 0, 2], 0.0, rtol=1e-5)

    def test_normalize_already_float(self):
        """Test normalization of already float image."""
        img = np.array([[[255.0, 128.0, 0.0]]], dtype=np.float32)
        normalized = normalize_image(img)

        assert normalized.dtype == np.float32
        np.testing.assert_allclose(normalized[0, 0, 0], 1.0, rtol=1e-5)

    def test_normalize_zeros(self):
        """Test normalization of all-zero image."""
        img = np.zeros((224, 224, 3), dtype=np.uint8)
        normalized = normalize_image(img)

        assert normalized.dtype == np.float32
        np.testing.assert_array_equal(normalized, np.zeros((224, 224, 3)))

    def test_normalize_max_values(self):
        """Test normalization of max value image."""
        img = np.full((10, 10, 3), 255, dtype=np.uint8)
        normalized = normalize_image(img)

        assert normalized.dtype == np.float32
        np.testing.assert_allclose(normalized, np.ones((10, 10, 3)), rtol=1e-5)


class TestEdgeCases:
    """Tests for edge cases and error handling."""

    def test_compress_large_weights(self):
        """Test compression of large weight arrays."""
        # Simulate a large model layer
        large_weights = [np.random.rand(1000, 1000).astype(np.float32)]

        compressed = compress_weights(large_weights)
        decompressed = decompress_weights(compressed)

        np.testing.assert_array_equal(large_weights[0], decompressed[0])

    def test_normalize_different_shapes(self):
        """Test normalization works with various image shapes."""
        shapes = [(100, 100, 3), (224, 224, 3), (512, 512, 3), (64, 64, 1)]

        for shape in shapes:
            img = np.random.randint(0, 256, size=shape, dtype=np.uint8)
            normalized = normalize_image(img)

            assert normalized.shape == shape
            assert normalized.min() >= 0.0
            assert normalized.max() <= 1.0
