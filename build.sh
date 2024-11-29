#!/bin/bash

# Update pip to latest version
python -m pip install --upgrade pip

# Install dependencies with specific flags
pip install --no-cache-dir -r requirements.txt --use-pep517
