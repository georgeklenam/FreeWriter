#!/usr/bin/env python
"""
Quick fix script for missing model fields
"""
import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FreeWriter.settings')
django.setup()

from django.db import connection
from django.core.management import call_command

def fix_missing_fields():
    """Fix missing model fields"""
    print("Checking for missing model fields...")
    
    try:
        # Check if category description field exists
        with connection.cursor() as cursor:
            cursor.execute('PRAGMA table_info(bookapp_category)')
            category_columns = [row[1] for row in cursor.fetchall()]
            
            if 'description' not in category_columns:
                print('Category description field missing. Adding it...')
                cursor.execute('ALTER TABLE bookapp_category ADD COLUMN description TEXT')
                print('Category description field added successfully!')
                
                # Update the migration record
                try:
                    cursor.execute("""
                        INSERT INTO django_migrations (app, name, applied) 
                        VALUES ('bookapp', '0005_add_category_description', datetime('now'))
                    """)
                    print('Migration record updated for category description.')
                except Exception as e:
                    print(f'Note: Could not update migration record: {e}')
            else:
                print('Category description field already exists.')
        
        # Check if book timestamp fields exist
        with connection.cursor() as cursor:
            cursor.execute('PRAGMA table_info(bookapp_book)')
            book_columns = [row[1] for row in cursor.fetchall()]
            
            missing_fields = []
            if 'created_at' not in book_columns:
                missing_fields.append('created_at')
                cursor.execute('ALTER TABLE bookapp_book ADD COLUMN created_at DATETIME')
                print('Book created_at field added successfully!')
            
            if 'updated_at' not in book_columns:
                missing_fields.append('updated_at')
                cursor.execute('ALTER TABLE bookapp_book ADD COLUMN updated_at DATETIME')
                print('Book updated_at field added successfully!')
            
            if missing_fields:
                # Update the migration record
                try:
                    cursor.execute("""
                        INSERT INTO django_migrations (app, name, applied) 
                        VALUES ('bookapp', '0006_add_book_timestamps', datetime('now'))
                    """)
                    print('Migration record updated for book timestamps.')
                except Exception as e:
                    print(f'Note: Could not update migration record: {e}')
            else:
                print('Book timestamp fields already exist.')
                
        print("All missing model fields have been fixed successfully!")
        return True
        
    except Exception as e:
        print(f'Error fixing model fields: {e}')
        return False

if __name__ == '__main__':
    success = fix_missing_fields()
    sys.exit(0 if success else 1)
