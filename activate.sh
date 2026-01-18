#!/bin/bash

# 1. Check if the script is being sourced
if [[ "$0" == "$BASH_SOURCE" ]]; then
    echo "ERROR: You must source this script to keep the environment active."
    echo "Usage: source setup.sh"
    exit 1
fi

VENV_DIR=".venv"

# 2. Create the venv if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
fi

# 3. Activate the virtual environment
# Sourcing this file modifies your current shell's PATH
echo "Activating environment..."
source "$VENV_DIR/bin/activate"

# 4. Install dependencies from pyproject.toml
if [ -f "pyproject.toml" ]; then
    echo "Installing script and dependencies..."
    pip install --upgrade pip
    pip install -e .
else
    echo "Warning: pyproject.toml not found in current directory."
fi

echo "Virtual environment is now active."
