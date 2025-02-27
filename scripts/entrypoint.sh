#!/bin/bash
chmod +x /app/scripts/entrypoint.sh
set -e
set -x

python manage.py migrate

python manage.py loaddata products

echo "from django.contrib.auth import get_user_model; \
User = get_user_model(); \
User.objects.filter(username='$DJANGO_SUPERUSER_USERNAME').delete(); \
User.objects.create_superuser('$DJANGO_SUPERUSER_USERNAME', '$DJANGO_SUPERUSER_EMAIL', '$DJANGO_SUPERUSER_PASSWORD')" | python manage.py shell


python manage.py test

python manage.py collectstatic --noinput

exec gunicorn --bind 0.0.0.0:8000 --workers 3 core.wsgi:application
