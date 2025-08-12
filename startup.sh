#!/bin/bash

# Exit on any error
set -e

echo "Starting FreeWriter application..."

# Function to check if database is ready
check_database() {
    echo "Checking database connection..."
    python -c "
import os
import sys
import django
sys.path.append(os.path.dirname(os.path.abspath('.')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FreeWriter.settings')
django.setup()
from django.db import connection
try:
    connection.ensure_connection()
    print('Database connection successful')
    exit(0)
except Exception as e:
    print(f'Database connection failed: {e}')
    exit(1)
"
}

# Wait for database to be ready
max_attempts=30
attempt=1
while [ $attempt -le $max_attempts ]; do
    echo "Attempt $attempt/$max_attempts to connect to database..."
    if check_database; then
        echo "Database is ready!"
        break
    else
        if [ $attempt -eq $max_attempts ]; then
            echo "Failed to connect to database after $max_attempts attempts. Exiting."
            exit 1
        fi
        echo "Database not ready, waiting 5 seconds..."
        sleep 5
        attempt=$((attempt + 1))
    fi
done

# Set up database
echo "Setting up database..."
if ! python setup_db.py; then
    echo "Database setup failed. Attempting migration reset..."
    if python reset_migrations.py; then
        echo "Migration reset successful, retrying database setup..."
        python setup_db.py
    else
        echo "Migration reset failed. Please check your database configuration."
        exit 1
    fi
fi

# Check for missing fields and fix them
echo "Checking for missing model fields..."
python -c "
import os
import sys
import django
sys.path.append(os.path.dirname(os.path.abspath('.')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FreeWriter.settings')
django.setup()

from django.db import connection
from django.core.management import call_command

try:
    # Check if category description field exists
    with connection.cursor() as cursor:
        cursor.execute('PRAGMA table_info(bookapp_category)')
        category_columns = [row[1] for row in cursor.fetchall()]
        
        if 'description' not in category_columns:
            print('Category description field missing. Running migration...')
            call_command('migrate', 'bookapp', '0005_add_category_description', '--noinput')
            print('Category description field added successfully!')
        else:
            print('Category description field already exists.')
    
    # Check if book timestamp fields exist
    with connection.cursor() as cursor:
        cursor.execute('PRAGMA table_info(bookapp_book)')
        book_columns = [row[1] for row in cursor.fetchall()]
        
        missing_fields = []
        if 'created_at' not in book_columns:
            missing_fields.append('created_at')
        if 'updated_at' not in book_columns:
            missing_fields.append('updated_at')
        
        if missing_fields:
            print(f'Book timestamp fields missing: {missing_fields}. Running migration...')
            call_command('migrate', 'bookapp', '0006_add_book_timestamps', '--noinput')
            print('Book timestamp fields added successfully!')
        else:
            print('Book timestamp fields already exist.')
            
except Exception as e:
    print(f'Error checking model fields: {e}')
    # Try to run all pending migrations
    try:
        print('Attempting to run all pending migrations...')
        call_command('migrate', '--noinput')
        print('Migrations completed successfully!')
    except Exception as migrate_error:
        print(f'Migration failed: {migrate_error}')
        exit(1)
"
if [ $? -ne 0 ]; then
    echo "Failed to fix missing model fields. Exiting."
    exit 1
fi

# Create superuser if it doesn't exist
echo "Checking for superuser..."
python manage.py create_superuser

# Create books from existing images if no books exist
echo "Setting up books..."
python manage.py shell -c "
from bookapp.models import Book
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
"

# Start Gunicorn server
echo "Starting Gunicorn server..."
exec gunicorn --bind 0.0.0.0:8000 --workers 3 --timeout 120 FreeWriter.wsgi:application
