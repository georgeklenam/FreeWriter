#!/bin/bash

# Wait for database to be ready
echo "Waiting for database..."
python manage.py migrate --check || {
    echo "Running migrations..."
    python manage.py makemigrations
    python manage.py migrate
}

# Create superuser if it doesn't exist
echo "Checking for superuser..."
python manage.py create_superuser

# Create books from existing images if no books exist
echo "Checking for books..."
python manage.py shell -c "
from bookapp.models import Book
if Book.objects.count() == 0:
    print('No books found, creating books from existing images...')
    from django.core.management import call_command
    call_command('create_books_from_images')
else:
    print(f'Found {Book.objects.count()} books in database')
    # Only fix missing images and PDFs for existing books
    print('Fixing missing images and PDFs for existing books...')
    call_command('fix_images')
    call_command('fix_pdfs')
"

# Start Gunicorn server
echo "Starting Gunicorn server..."
exec gunicorn --bind 0.0.0.0:8000 --workers 3 --timeout 120 FreeWriter.wsgi:application
