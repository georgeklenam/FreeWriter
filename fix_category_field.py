#!/usr/bin/env python
"""
Quick fix script for missing category description field
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

def fix_category_description():
    """Fix the missing category description field"""
    print("Checking for missing category description field...")
    
    try:
        # Check if category description field exists
        with connection.cursor() as cursor:
            cursor.execute('PRAGMA table_info(bookapp_category)')
            columns = [row[1] for row in cursor.fetchall()]
            
            if 'description' not in columns:
                print('Category description field missing. Adding it...')
                
                # Add the column directly to the database
                cursor.execute('ALTER TABLE bookapp_category ADD COLUMN description TEXT')
                print('Category description field added successfully!')
                
                # Update the migration record
                try:
                    cursor.execute("""
                        INSERT INTO django_migrations (app, name, applied) 
                        VALUES ('bookapp', '0005_add_category_description', datetime('now'))
                    """)
                    print('Migration record updated.')
                except Exception as e:
                    print(f'Note: Could not update migration record: {e}')
                    
            else:
                print('Category description field already exists.')
                
        print("Category description field fix completed successfully!")
        return True
        
    except Exception as e:
        print(f'Error fixing category field: {e}')
        return False

if __name__ == '__main__':
    success = fix_category_description()
    sys.exit(0 if success else 1)
