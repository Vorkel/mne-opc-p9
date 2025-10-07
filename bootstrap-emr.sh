#!/bin/bash
# Bootstrap script pour EMR - Installation des packages Python nécessaires

# Mise à jour de pip et setuptools
sudo python3 -m pip install --upgrade pip setuptools

# Installation des packages pour le projet
sudo python3 -m pip install pandas==1.2.5
sudo python3 -m pip install pillow
sudo python3 -m pip install tensorflow==2.15.0
sudo python3 -m pip install pyarrow
sudo python3 -m pip install optree
