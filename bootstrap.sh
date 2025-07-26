#!/bin/bash

set -e

# --- Configuration ---
VENV_DIR=".venv"

echo "Installing Python3"
sudo apt update
sudo apt install -y python3 python3-venv python3-pip

echo "Creating Python virtual environment"
python3 -m venv "$VENV_DIR"

echo "Activating virtual environment"
source "$VENV_DIR/bin/activate"

echo "Installing Python packages"
pip install --upgrade pip
pip install esptool mpremote
pip install opencv-python

echo "Setup complete!"
echo "To activate the environment, run:"
echo "    source $VENV_DIR/bin/activate"
