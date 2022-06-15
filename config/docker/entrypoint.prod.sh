#!/bin/sh

echo "Collect static file"
python manage.py collectstatic --no-input

echo "Migrate"
python manage.py migrate

echo "Create superuser"
if [ "$DJANGO_SUPERUSER_USERNAME" ]
then
    python manage.py createsuperuser \
        --noinput \
        --username $DJANGO_SUPERUSER_USERNAME \
        --email $DJANGO_SUPERUSER_USERNAME
fi

exec "$@"