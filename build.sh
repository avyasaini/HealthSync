#!/usr/bin/env bash
# Exit on error
set -o errexit

echo "Starting build process..."

# Install dependencies from requirements.txt
pip install -r requirements.txt

# Create necessary directories
echo "Creating application directories..."
mkdir -p uploads static templates data

# Initialize sqlite DB if not exists
# (Not critical here, Flask SQLAlchemy handles it in app.py generally)
echo "Build process finished."
