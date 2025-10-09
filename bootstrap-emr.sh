#!/bin/bash
# Bootstrap script pour EMR - Installation des packages Python nécessaires
# Project: P9 - Fruits Classification
# Author: Maxime Nejad
# Last updated: 2025-10-08

set -e  # Exit on error
set -o pipefail  # Fail on pipe errors

# Configuration
LOG_FILE="/tmp/bootstrap-emr.log"
PYTHON_VERSION="3.9"

# Logging function
log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"
}

error() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] ERROR: $*" | tee -a "$LOG_FILE" >&2
    exit 1
}

log "===== EMR Bootstrap Script Started ====="
log "Python version: $(python3 --version)"
log "Pip version: $(python3 -m pip --version)"

# Mise à jour de pip et setuptools
log "Updating pip and setuptools..."
sudo python3 -m pip install --upgrade pip==24.0 setuptools==69.0.3 wheel==0.42.0 || error "Failed to upgrade pip/setuptools"

# Installation des packages pour le projet avec versions verrouillées
log "Installing project dependencies..."

PACKAGES=(
    "pandas==1.5.3"
    "pillow==10.2.0"
    "rich==13.7.0"
    "tensorflow==2.15.0"
    "pyarrow==14.0.2"
    "optree==0.11.0"
    "scikit-learn==1.3.2"
    "boto3==1.34.44"
    "fsspec==2024.2.0"
    "s3fs==2024.2.0"
)

for package in "${PACKAGES[@]}"; do
    log "Installing $package..."
    sudo python3 -m pip install "$package" || error "Failed to install $package"
done

log "===== Package Installation Complete ====="

# Verification checks
log "===== Running Verification Checks ====="

check_import() {
    local module=$1
    log "Checking $module..."
    python3 -c "import $module; print(f'✅ $module version: {$module.__version__}')" >> "$LOG_FILE" 2>&1 || {
        error "Failed to import $module"
    }
}

# Check critical imports
check_import "pandas"
check_import "PIL"
check_import "tensorflow"
check_import "pyarrow"
check_import "sklearn"

# Check TensorFlow GPU availability (optional, won't fail)
log "Checking TensorFlow configuration..."
python3 -c "import tensorflow as tf; print('TensorFlow version:', tf.__version__); print('GPU available:', tf.config.list_physical_devices('GPU'))" >> "$LOG_FILE" 2>&1 || log "Warning: TensorFlow check failed (non-critical)"

# Check PySpark availability
log "Checking PySpark..."
python3 -c "import pyspark; print('PySpark version:', pyspark.__version__)" >> "$LOG_FILE" 2>&1 || log "Warning: PySpark not available yet (will be available in notebook)"

# Display installed packages
log "Installed packages:"
python3 -m pip list >> "$LOG_FILE" 2>&1

log "===== Bootstrap Script Complete ====="
log "All checks passed successfully!"
log "Log saved to: $LOG_FILE"

exit 0
