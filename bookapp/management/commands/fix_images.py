from django.core.management.base import BaseCommand
from bookapp.models import Book
from django.core.files import File
import os
import re

class Command(BaseCommand):
    help = 'Fix missing images for existing books without creating duplicates'

    def handle(self, *args, **options):
        self.stdout.write('Fixing missing images for existing books...')
        
        # Get all image files from media/img directory
        img_dir = os.path.join('media', 'img')
        if not os.path.exists(img_dir):
            self.stdout.write(self.style.ERROR(f'Image directory not found: {img_dir}'))
            return
        
        image_files = [f for f in os.listdir(img_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))]
        self.stdout.write(f'Found {len(image_files)} image files in {img_dir}')
        
        # Get all books from database
        books = Book.objects.all()
        self.stdout.write(f'Found {books.count()} books in database')
        
        fixed_count = 0
        used_images = set()
        
        for book in books:
            self.stdout.write(f'Processing book: {book.title}')
            
            # Skip if book already has a valid image
            if book.cover_image and os.path.exists(book.cover_image.path):
                self.stdout.write(f'  - Book already has valid image: {book.cover_image.name}')
                used_images.add(os.path.basename(book.cover_image.name))
                continue
            
            # Try to find a matching image for this book
            matching_image = self.find_matching_image(book.title, image_files, used_images)
            
            if matching_image:
                img_path = os.path.join(img_dir, matching_image)
                
                # Assign the image to the book
                with open(img_path, 'rb') as img_file:
                    book.cover_image.save(matching_image, File(img_file), save=True)
                self.stdout.write(f'  - Assigned image: {matching_image}')
                used_images.add(matching_image)
                fixed_count += 1
            else:
                self.stdout.write(f'  - No matching image found for: {book.title}')
        
        self.stdout.write(self.style.SUCCESS(f'Fixed {fixed_count} missing images!'))
        
        # Show remaining unused images
        unused_images = [img for img in image_files if img not in used_images]
        
        if unused_images:
            self.stdout.write(f'\nUnused images ({len(unused_images)}):')
            for img in unused_images[:10]:  # Show first 10
                self.stdout.write(f'  - {img}')
            if len(unused_images) > 10:
                self.stdout.write(f'  ... and {len(unused_images) - 10} more')

    def find_matching_image(self, book_title, image_files, used_images):
        """Find the best matching image for a book title"""
        import re
        
        book_title_lower = book_title.lower()
        
        # Clean title for matching
        clean_title = re.sub(r'\b(the|a|an|and|or|but|in|on|at|to|for|of|with|by)\b', '', book_title_lower)
        clean_title = re.sub(r'[^\w\s]', '', clean_title).strip()
        
        # Try exact matches first (excluding already used images)
        available_images = [img for img in image_files if img not in used_images]
        
        for img in available_images:
            img_lower = img.lower()
            img_clean = re.sub(r'[^\w\s]', '', img_lower).replace('_', ' ').replace('-', ' ')
            
            # Check if book title words appear in image name
            title_words = clean_title.split()
            if any(word in img_clean for word in title_words if len(word) > 2):
                return img
        
        # Handle specific cases
        if 'random walk' in book_title_lower:
            for img in available_images:
                if 'random walk' in img.lower():
                    return img
        elif 'oliver' in book_title_lower:
            for img in available_images:
                if 'oliver' in img.lower():
                    return img
        elif 'serial killer' in book_title_lower:
            for img in available_images:
                if 'serial' in img.lower():
                    return img
        elif 'manga guide' in book_title_lower:
            for img in available_images:
                if 'manga guide' in img.lower():
                    return img
        elif 'manga master' in book_title_lower:
            for img in available_images:
                if 'manga master' in img.lower():
                    return img
        elif 'linux' in book_title_lower:
            for img in available_images:
                if 'linux' in img.lower():
                    return img
        elif 'hacking' in book_title_lower:
            for img in available_images:
                if 'hacking' in img.lower():
                    return img
        elif 'intelligent' in book_title_lower:
            for img in available_images:
                if 'intelligent' in img.lower():
                    return img
        elif 'science' in book_title_lower:
            for img in available_images:
                if 'science' in img.lower():
                    return img
        elif 'penis' in book_title_lower:
            for img in available_images:
                if 'penis' in img.lower():
                    return img
        elif 'purple' in book_title_lower:
            for img in available_images:
                if 'purple' in img.lower():
                    return img
        
        # If no specific match found, return any available image
        if available_images:
            return available_images[0]
        
        return None
