#!/bin/bash
# Quick launch script for Deep Core Quest

# Check if dependencies are installed
if ! python3 -c "import pygame" 2>/dev/null; then
    echo "Installing dependencies..."
    pip3 install -r requirements.txt
fi

# Launch game
echo "Launching Deep Core Quest..."
python3 main.py
