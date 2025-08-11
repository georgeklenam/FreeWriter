#!/bin/bash

# Production startup script for FreeWriter

echo "Starting FreeWriter production server..."

# Wait for database to be ready
echo "Checking database..."
python manage.py migrate --settings=FreeWriter.settings_prod

# Create superuser if it doesn't exist
echo "Checking for superuser..."
python manage.py shell --settings=FreeWriter.settings_prod -c "
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@freewriter.com', 'f001')
    print('Superuser created: admin/f001')
else:
    print('Superuser already exists')
"

# Create books from existing images if no books exist
echo "Checking for books..."
python manage.py shell --settings=FreeWriter.settings_prod -c "
from bookapp.models import Book
if Book.objects.count() == 0:
    print('No books found, creating books from existing images...')
    from django.core.management import call_command
    call_command('create_books_from_images', settings='FreeWriter.settings_prod')
else:
    print(f'Found {Book.objects.count()} books in database')
"

# Collect static files (in case they weren't collected during build)
echo "Collecting static files..."
python manage.py collectstatic --noinput --settings=FreeWriter.settings_prod

echo "Starting Gunicorn server..."
exec gunicorn --bind 0.0.0.0:8000 --workers 3 --timeout 120 --access-logfile - --error-logfile - FreeWriter.wsgi:application
