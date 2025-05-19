#!/usr/bin/env bash
set -e  # exit on error

# Move to the API root directory
cd "$(dirname "${BASH_SOURCE[0]}")/.."

# 1) Generate .env
if [ ! -f .env ]; then
  cp .env.example .env
  echo ".env created from .env.example"
else
  echo ".env already exists"
fi

# 2) Create venv
if [ ! -d venv ]; then
  python3 -m venv venv
  echo "Created virtual environment venv"
fi

# 3) Activate venv and install deps
# shellcheck disable=SC1091
source venv/bin/activate
pip install -r requirements.txt

echo "Dependencies installed"

# 4) Run tests
pytest

echo "Setup complete. To run the server: source venv/bin/activate && python app.py"