#!/bin/bash

# Exit on any error
set -e

echo "Starting FreeWriter application..."

# Wait for database to be ready and run migrations
echo "Running database migrations..."
python manage.py makemigrations bookapp --noinput
python manage.py migrate

# Create superuser if it doesn't exist
echo "Checking for superuser..."
python manage.py create_superuser

# Wait a moment for database to be fully ready
sleep 2

# Create books from existing images if no books exist
echo "Setting up books..."
python manage.py shell -c "
from bookapp.models import Book
try:
    if Book.objects.count() == 0:
        print('No books found, creating books from existing images...')
        from django.core.management import call_command
        call_command('create_books_from_images')
    else:
        print(f'Found {Book.objects.count()} books in database')
        # Fix missing images and PDFs for existing books
        print('Fixing missing images and PDFs for existing books...')
        call_command('fix_images')
        call_command('fix_pdfs')
except Exception as e:
    print(f'Error during book setup: {e}')
    print('Continuing with server startup...')
"

# Start Gunicorn server
echo "Starting Gunicorn server..."
exec gunicorn --bind 0.0.0.0:8000 --workers 3 --timeout 120 FreeWriter.wsgi:application
