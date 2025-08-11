from django.core.management.base import BaseCommand
from bookapp.models import Book, Category
from django.core.files import File
import os
import re

class Command(BaseCommand):
    help = 'Create books based on existing images in media folder'

    def handle(self, *args, **options):
        self.stdout.write('Creating books from existing images...')
        
        # Get all image files from media/img directory
        img_dir = os.path.join('media', 'img')
        if not os.path.exists(img_dir):
            self.stdout.write(self.style.ERROR(f'Image directory not found: {img_dir}'))
            return
        
        image_files = [f for f in os.listdir(img_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))]
        self.stdout.write(f'Found {len(image_files)} image files in {img_dir}')
        
        # Create categories if they don't exist
        categories = {
            'fiction': Category.objects.get_or_create(slug='fiction', defaults={'name': 'Fiction'})[0],
            'business': Category.objects.get_or_create(slug='business', defaults={'name': 'Business'})[0],
            'science': Category.objects.get_or_create(slug='science', defaults={'name': 'Science'})[0],
            'technology': Category.objects.get_or_create(slug='technology', defaults={'name': 'Technology'})[0],
            'self-help': Category.objects.get_or_create(slug='self-help', defaults={'name': 'Self-Help'})[0],
        }
        
        created_count = 0
        
        for img_file in image_files:
            # Generate book title from image filename
            book_title = self.generate_book_title(img_file)
            book_slug = self.generate_slug(book_title)
            
            # Skip if book already exists
            if Book.objects.filter(slug=book_slug).exists():
                self.stdout.write(f'Book already exists: {book_title}')
                continue
            
            # Determine category based on image name
            category = self.determine_category(img_file)
            
            # Create the book
            book = Book.objects.create(
                title=book_title,
                slug=book_slug,
                author=self.generate_author(img_file),
                summary=self.generate_summary(book_title, category),
                recommended_books=self.is_recommended(img_file),
                fiction_books=category.name.lower() == 'fiction',
                business_books=category.name.lower() == 'business',
            )
            
            # Add category
            book.category.add(categories[category.slug])
            
            # Assign the image
            img_path = os.path.join(img_dir, img_file)
            with open(img_path, 'rb') as img_file_obj:
                book.cover_image.save(img_file, File(img_file_obj), save=True)
            
            # Assign PDF file if available
            pdf_file = self.find_matching_pdf(img_file)
            if pdf_file:
                pdf_dir = os.path.join('media', 'pdf')
                pdf_path = os.path.join(pdf_dir, pdf_file)
                if os.path.exists(pdf_path):
                    with open(pdf_path, 'rb') as pdf_file_obj:
                        book.pdf.save(pdf_file, File(pdf_file_obj), save=True)
                    self.stdout.write(f'  - Assigned PDF: {pdf_file}')
                else:
                    self.stdout.write(f'  - PDF not found: {pdf_file}')
                    # Add PDFDrive.com link as fallback
                    pdfdrive_url = self.generate_pdfdrive_url(book_title)
                    book.pdf_url = pdfdrive_url
                    book.save()
                    self.stdout.write(f'  - Added PDFDrive link: {pdfdrive_url}')
            else:
                self.stdout.write(f'  - No matching PDF found')
                # Add PDFDrive.com link as fallback
                pdfdrive_url = self.generate_pdfdrive_url(book_title)
                book.pdf_url = pdfdrive_url
                book.save()
                self.stdout.write(f'  - Added PDFDrive link: {pdfdrive_url}')
            
            self.stdout.write(f'Created book: {book_title} (Category: {category.name})')
            created_count += 1
        
        self.stdout.write(self.style.SUCCESS(f'Created {created_count} books from images!'))

    def generate_book_title(self, img_filename):
        """Generate a book title from image filename"""
        # Remove file extension
        name = os.path.splitext(img_filename)[0]
        
        # Replace underscores and hyphens with spaces
        name = name.replace('_', ' ').replace('-', ' ')
        
        # Capitalize words
        name = ' '.join(word.capitalize() for word in name.split())
        
        # Handle special cases
        if 'random walk' in name.lower():
            return 'A Random Walk Down Wall Street'
        elif 'oliver' in name.lower():
            return 'Oliver Twist'
        elif 'serial killer' in name.lower():
            return 'My Sister the Serial Killer'
        elif 'manga' in name.lower():
            if 'guide' in name.lower():
                return 'The Manga Guide to Molecular Biology'
            elif 'master' in name.lower():
                return 'Mastering Manga: How to Draw Manga Faces'
        elif 'linux' in name.lower():
            return 'Linux Tips, Tricks & Hacks'
        elif 'hacking' in name.lower():
            return 'The Basics of Hacking and Penetration Testing'
        elif 'intelligent' in name.lower():
            return 'The Intelligent Investor'
        elif 'science' in name.lower():
            return 'The Handy Science Answer Book'
        elif 'penis' in name.lower():
            return 'Penis Exercises: A Healthy Book for Enhancement'
        elif 'purple' in name.lower():
            return 'Purple Hibiscus'
        
        return name

    def generate_slug(self, title):
        """Generate a slug from title"""
        slug = re.sub(r'[^\w\s-]', '', title.lower())
        slug = re.sub(r'[-\s]+', '-', slug).strip('-')
        return slug

    def generate_author(self, img_filename):
        """Generate author name based on image filename"""
        name_lower = img_filename.lower()
        
        if 'random walk' in name_lower:
            return 'Burton G. Malkiel'
        elif 'oliver' in name_lower:
            return 'Charles Dickens'
        elif 'serial killer' in name_lower:
            return 'Oyinkan Braithwaite'
        elif 'manga' in name_lower:
            if 'guide' in name_lower:
                return 'Masaharu Takemura'
            elif 'master' in name_lower:
                return 'Christopher Hart'
        elif 'linux' in name_lower:
            return 'Linux Community'
        elif 'hacking' in name_lower:
            return 'Patrick Engebretson'
        elif 'intelligent' in name_lower:
            return 'Benjamin Graham'
        elif 'science' in name_lower:
            return 'Science Reference Team'
        elif 'penis' in name_lower:
            return 'Health Publications'
        elif 'purple' in name_lower:
            return 'Chimamanda Ngozi Adichie'
        
        return 'Various Authors'

    def generate_summary(self, title, category):
        """Generate a summary based on title and category"""
        summaries = {
            'Fiction': f'A captivating {title.lower()} that will keep you engaged from start to finish.',
            'Business': f'Essential business knowledge and strategies for success in {title.lower()}.',
            'Science': f'Explore the fascinating world of science through {title.lower()}.',
            'Technology': f'Master the latest technology trends and techniques in {title.lower()}.',
            'Self-Help': f'Transform your life with practical advice and insights from {title.lower()}.',
        }
        return summaries.get(category.name, f'An informative and engaging book about {title.lower()}.')

    def determine_category(self, img_filename):
        """Determine book category based on image filename"""
        name_lower = img_filename.lower()
        
        if any(word in name_lower for word in ['fiction', 'oliver', 'serial', 'purple']):
            return Category.objects.get_or_create(slug='fiction', defaults={'name': 'Fiction'})[0]
        elif any(word in name_lower for word in ['business', 'random walk', 'intelligent']):
            return Category.objects.get_or_create(slug='business', defaults={'name': 'Business'})[0]
        elif any(word in name_lower for word in ['science', 'manga guide']):
            return Category.objects.get_or_create(slug='science', defaults={'name': 'Science'})[0]
        elif any(word in name_lower for word in ['hacking', 'linux', 'technology']):
            return Category.objects.get_or_create(slug='technology', defaults={'name': 'Technology'})[0]
        elif any(word in name_lower for word in ['penis', 'exercise', 'health']):
            return Category.objects.get_or_create(slug='self-help', defaults={'name': 'Self-Help'})[0]
        
        # Default to fiction
        return Category.objects.get_or_create(slug='fiction', defaults={'name': 'Fiction'})[0]

    def is_recommended(self, img_filename):
        """Determine if book should be recommended"""
        name_lower = img_filename.lower()
        recommended_keywords = ['random walk', 'intelligent', 'oliver', 'serial killer', 'manga guide']
        return any(keyword in name_lower for keyword in recommended_keywords)

    def find_matching_pdf(self, img_filename):
        """Find matching PDF file for an image"""
        pdf_dir = os.path.join('media', 'pdf')
        if not os.path.exists(pdf_dir):
            return None
        
        pdf_files = [f for f in os.listdir(pdf_dir) if f.lower().endswith('.pdf')]
        
        # Clean image filename for matching
        img_name = os.path.splitext(img_filename)[0].lower()
        img_name = img_name.replace('_', ' ').replace('-', ' ')
        
        # Try to find matching PDF
        for pdf_file in pdf_files:
            pdf_name = os.path.splitext(pdf_file)[0].lower()
            pdf_name = pdf_name.replace('_', ' ').replace('-', ' ')
            
            # Check for exact matches or partial matches
            if img_name in pdf_name or pdf_name in img_name:
                return pdf_file
            
            # Check for common keywords
            img_words = img_name.split()
            pdf_words = pdf_name.split()
            
            # If more than 2 words match, consider it a match
            common_words = set(img_words) & set(pdf_words)
            if len(common_words) >= 2:
                return pdf_file
        
        # Handle specific cases
        if 'random walk' in img_name:
            return 'A_Random_Walk_Down_Wall_Street.pdf'
        elif 'oliver' in img_name:
            return 'oliver-twist.pdf'
        elif 'serial killer' in img_name:
            return 'My_Sister_the_Serial_Killer.pdf'
        elif 'manga guide' in img_name:
            return 'The_Manga_Guide_to_Molecular_Biology__PDFDrive_.pdf'
        elif 'manga master' in img_name:
            return 'Mastering_Manga_How_to_Draw_Manga_Faces__PDFDrive_.pdf'
        elif 'linux' in img_name:
            return 'Linux_Tips_Tricks_PPS__Hacks_Vol_3.pdf'
        elif 'hacking' in img_name:
            return 'The_Basics_Of_Hacking_And_Penetration_Testing__Ethical_Hacking_And_Penetration_Testing.pdf'
        elif 'intelligent' in img_name:
            return 'The_Intelligent_Investor.pdf'
        elif 'science' in img_name:
            return 'The_Handy_Science_Answer_Book_The_Handy_Answer_Book_Series____PDFDrive_.pdf'
        elif 'penis' in img_name:
            return 'Penis_Exercises_A_Healthy_Book_for_Enlargement_Enhancement_Hardness__Health__PDFDrive_.pdf'
        elif 'purple' in img_name:
            return 'Purple_Hibiscus.pdf'
        
        return None

    def generate_pdfdrive_url(self, book_title):
        """Generate a welib.org search URL for a book title"""
        import urllib.parse
        
        # Clean the title for URL
        clean_title = book_title.replace(':', '').replace('(', '').replace(')', '')
        clean_title = ' '.join(clean_title.split())  # Remove extra spaces
        
        # Encode for URL
        encoded_title = urllib.parse.quote(clean_title)
        
        # Create welib.org search URL
        return f'https://www.welib.org/search?q={encoded_title}'
