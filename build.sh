#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

# Run Django migrations
python manage.py migrate

# Collect static files for production
python manage.py collectstatic --no-input