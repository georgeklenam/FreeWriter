from django.core.management.base import BaseCommand
from bookapp.models import Book
from django.core.files import File
import os

class Command(BaseCommand):
    help = 'Link existing real images to books'

    def handle(self, *args, **options):
        self.stdout.write('Linking existing real images to books...')
        
        # Get all image files from media/img directory
        img_dir = os.path.join('media', 'img')
        if not os.path.exists(img_dir):
            self.stdout.write(self.style.ERROR(f'Image directory not found: {img_dir}'))
            return
        
        image_files = [f for f in os.listdir(img_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))]
        self.stdout.write(f'Found {len(image_files)} image files in {img_dir}')
        
        books = Book.objects.all()
        self.stdout.write(f'Found {books.count()} books in database')
        
        linked_count = 0
        
        for book in books:
            self.stdout.write(f'Processing book: {book.title}')
            
            # Try to find a matching image for this book
            matching_image = self.find_matching_image(book.title, image_files)
            
            if matching_image:
                img_path = os.path.join(img_dir, matching_image)
                
                # Assign the image to the book
                with open(img_path, 'rb') as img_file:
                    book.cover_image.save(matching_image, File(img_file), save=True)
                self.stdout.write(f'  - Linked image: {matching_image}')
                linked_count += 1
            else:
                self.stdout.write(f'  - No matching image found for: {book.title}')
        
        self.stdout.write(self.style.SUCCESS(f'Linked {linked_count} images to books!'))
        
        # Show remaining unused images
        used_images = [book.cover_image.name.split('/')[-1] for book in Book.objects.filter(cover_image__isnull=False)]
        unused_images = [img for img in image_files if img not in used_images]
        
        if unused_images:
            self.stdout.write(f'\nUnused images ({len(unused_images)}):')
            for img in unused_images[:10]:  # Show first 10
                self.stdout.write(f'  - {img}')
            if len(unused_images) > 10:
                self.stdout.write(f'  ... and {len(unused_images) - 10} more')

    def find_matching_image(self, book_title, image_files):
        """Find the best matching image for a book title"""
        import re
        
        book_title_lower = book_title.lower()
        
        # Clean title for matching
        clean_title = re.sub(r'\b(the|a|an|and|or|but|in|on|at|to|for|of|with|by)\b', '', book_title_lower)
        clean_title = re.sub(r'[^\w\s]', '', clean_title).strip()
        
        # Try exact matches first
        for img in image_files:
            img_lower = img.lower()
            img_clean = re.sub(r'[^\w\s]', '', img_lower).replace('_', ' ').replace('-', ' ')
            
            # Check if book title words appear in image name
            title_words = clean_title.split()
            if any(word in img_clean for word in title_words if len(word) > 2):
                return img
        
        # Handle specific cases
        if 'random walk' in book_title_lower:
            return 'A_Random_Walk.jpeg'
        elif 'oliver' in book_title_lower:
            return 'oliver.jpeg'
        elif 'serial killer' in book_title_lower:
            return 'serial_killer.jpg'
        elif 'manga guide' in book_title_lower:
            return 'manga guide.jpeg'
        elif 'manga master' in book_title_lower:
            return 'manga master.jpeg'
        elif 'linux' in book_title_lower:
            return 'linux_tips.jpeg'
        elif 'hacking' in book_title_lower:
            return 'basics_of_hacking.jpeg'
        elif 'intelligent' in book_title_lower:
            return 'intelligent.jpg'
        elif 'science' in book_title_lower:
            return 'science.jpeg'
        elif 'penis' in book_title_lower:
            return 'penis exersice.jpeg'
        elif 'purple' in book_title_lower:
            return 'purple.jpeg'
        
        return None
