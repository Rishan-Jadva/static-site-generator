#!/bin/bash

# Check if commit message is provided
if [ -z "$1" ]; then
  echo "Usage: $0 <commit-message>"
  exit 1
fi

# Run Python scripts
python3 add.py
python3 src/main.py

# Git operations
git add .
git commit -m "$1"
git push origin main
