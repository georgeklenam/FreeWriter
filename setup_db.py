#!/usr/bin/env python
"""
Simple database setup script for FreeWriter
"""
import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FreeWriter.settings')
django.setup()

from django.core.management import call_command
from django.db import connection

def setup_database():
    """Set up the database with all necessary migrations"""
    print("Setting up FreeWriter database...")
    
    try:
        # Run migrations
        print("Running migrations...")
        call_command('makemigrations', '--noinput')
        call_command('migrate')
        
        # Check if tables exist
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name='bookapp_book'
            """)
            table_exists = cursor.fetchone()
            
            if table_exists:
                cursor.execute("PRAGMA table_info(bookapp_book)")
                columns = [row[1] for row in cursor.fetchall()]
                print(f"Book table columns: {columns}")
                
                if 'pdf_url' not in columns:
                    print("ERROR: pdf_url column not found in bookapp_book table")
                    print("Please run migrations manually:")
                    print("python manage.py makemigrations")
                    print("python manage.py migrate")
                    return False
            else:
                print("ERROR: bookapp_book table not found")
                return False
        
        print("Database setup completed successfully!")
        return True
        
    except Exception as e:
        print(f"Error setting up database: {e}")
        return False

if __name__ == '__main__':
    success = setup_database()
    sys.exit(0 if success else 1)
