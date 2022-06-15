#!/bin/sh

echo "Collect static file"
python manage.py collectstatic --no-input

echo "Migrate"
python manage.py migrate

exec "$@"