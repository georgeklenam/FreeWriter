#!/usr/bin/env python
"""
Migration reset script for FreeWriter
Use this only when you have migration conflicts during deployment
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
import shutil

def reset_migrations():
    """Reset migrations and recreate them"""
    print("Resetting migrations for FreeWriter...")
    
    try:
        # Backup current migrations
        migrations_dir = 'bookapp/migrations'
        backup_dir = 'bookapp/migrations_backup'
        
        if os.path.exists(migrations_dir):
            if os.path.exists(backup_dir):
                shutil.rmtree(backup_dir)
            shutil.copytree(migrations_dir, backup_dir)
            print(f"Backed up migrations to {backup_dir}")
        
        # Remove all migration files except __init__.py
        for filename in os.listdir(migrations_dir):
            if filename != '__init__.py' and filename.endswith('.py'):
                os.remove(os.path.join(migrations_dir, filename))
                print(f"Removed {filename}")
        
        # Remove migration records from database
        with connection.cursor() as cursor:
            try:
                cursor.execute("DELETE FROM django_migrations WHERE app='bookapp'")
                print("Cleared migration records from database")
            except Exception as e:
                print(f"Note: Could not clear migration records: {e}")
        
        # Create fresh initial migration
        print("Creating fresh initial migration...")
        call_command('makemigrations', 'bookapp', '--noinput')
        
        # Apply the new migration
        print("Applying new migration...")
        call_command('migrate', '--noinput')
        
        print("Migration reset completed successfully!")
        return True
        
    except Exception as e:
        print(f"Error resetting migrations: {e}")
        return False

if __name__ == '__main__':
    success = reset_migrations()
    sys.exit(0 if success else 1)
