#!/bin/bash

echo ""
echo ""

cd /app/

# Wait for the database to be ready
python /app/manage.py wait_for_db

# Make migrations if needed
python /app/manage.py makemigrations

# Apply database migrations
python /app/manage.py migrate 

# Collect static files
python /app/manage.py collectstatic --noinput

# Create superuser if it doesn't exist
python /app/manage.py shell <<EOF
import os
from django.contrib.auth import get_user_model

User = get_user_model()
username = os.getenv("DJANGO_SUPERUSER_USERNAME", "admin")
email = os.getenv("DJANGO_SUPERUSER_EMAIL", "admin@example.com")
password = os.getenv("DJANGO_SUPERUSER_PASSWORD", "password")

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print("Superuser created successfully!")
else:
    print("Superuser already exists, skipping creation.")
EOF

# Start the Django development server
python /app/manage.py runserver "0.0.0.0:8000"

# Hand off to the CMD
exec "$@"