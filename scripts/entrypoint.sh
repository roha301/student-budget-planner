#!/bin/sh
set -e

echo "Running database migrations..."
python manage.py migrate

echo "Collect static files..."
python manage.py collectstatic --noinput || true

exec "$@"
