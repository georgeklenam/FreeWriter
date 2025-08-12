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
from django.db.utils import OperationalError

def setup_database():
    """Set up the database with all necessary migrations"""
    print("Setting up FreeWriter database...")
    
    try:
        # Check database connection first
        print("Checking database connection...")
        connection.ensure_connection()
        
        # Run migrations (don't create new ones during deployment)
        print("Running migrations...")
        call_command('migrate', '--noinput')
        
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
                
                # Check for essential columns
                essential_columns = ['id', 'title', 'author', 'summary']
                missing_columns = [col for col in essential_columns if col not in columns]
                
                if missing_columns:
                    print(f"WARNING: Missing essential columns: {missing_columns}")
                    print("This might indicate a migration issue.")
                else:
                    print("Essential columns are present.")
            else:
                print("ERROR: bookapp_book table not found")
                print("Migrations may have failed. Check the logs above.")
                return False
        
        print("Database setup completed successfully!")
        return True
        
    except OperationalError as e:
        print(f"Database connection error: {e}")
        print("Make sure your database is running and accessible.")
        return False
    except Exception as e:
        print(f"Error setting up database: {e}")
        print("Check the error details above and fix any migration issues.")
        return False

if __name__ == '__main__':
    success = setup_database()
    sys.exit(0 if success else 1)
