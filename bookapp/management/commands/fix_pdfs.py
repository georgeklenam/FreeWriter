from django.core.management.base import BaseCommand
from bookapp.models import Book
from django.core.files import File
import os
import re

class Command(BaseCommand):
    help = 'Fix missing PDF files for existing books without creating duplicates'

    def handle(self, *args, **options):
        self.stdout.write('Fixing missing PDF files for existing books...')
        
        # Get all PDF files from media/pdf directory
        pdf_dir = os.path.join('media', 'pdf')
        if not os.path.exists(pdf_dir):
            self.stdout.write(self.style.ERROR(f'PDF directory not found: {pdf_dir}'))
            return
        
        pdf_files = [f for f in os.listdir(pdf_dir) if f.lower().endswith('.pdf')]
        self.stdout.write(f'Found {len(pdf_files)} PDF files in {pdf_dir}')
        
        # Get all books from database
        books = Book.objects.all()
        self.stdout.write(f'Found {books.count()} books in database')
        
        fixed_count = 0
        used_pdfs = set()
        
        for book in books:
            self.stdout.write(f'Processing book: {book.title}')
            
            # Skip if book already has a valid PDF
            if book.pdf and os.path.exists(book.pdf.path):
                self.stdout.write(f'  - Book already has PDF: {book.pdf.name}')
                used_pdfs.add(os.path.basename(book.pdf.name))
                continue
            
            # Try to find a matching PDF for this book
            matching_pdf = self.find_matching_pdf(book.title, pdf_files, used_pdfs)
            
            if matching_pdf:
                pdf_path = os.path.join(pdf_dir, matching_pdf)
                
                # Assign the PDF to the book
                with open(pdf_path, 'rb') as pdf_file:
                    book.pdf.save(matching_pdf, File(pdf_file), save=True)
                self.stdout.write(f'  - Assigned PDF: {matching_pdf}')
                used_pdfs.add(matching_pdf)
                fixed_count += 1
            else:
                self.stdout.write(f'  - No matching PDF found for: {book.title}')
                # Add Welib.org link as fallback if not already present
                if not book.pdf_url:
                    pdfdrive_url = self.generate_pdfdrive_url(book.title)
                    book.pdf_url = pdfdrive_url
                    book.save()
                    self.stdout.write(f'  - Added Welib.org link: {pdfdrive_url}')
                    fixed_count += 1
        
        self.stdout.write(self.style.SUCCESS(f'Fixed {fixed_count} PDF references!'))
        
        # Show remaining unused PDFs
        unused_pdfs = [pdf for pdf in pdf_files if pdf not in used_pdfs]
        
        if unused_pdfs:
            self.stdout.write(f'\nUnused PDFs ({len(unused_pdfs)}):')
            for pdf in unused_pdfs[:10]:  # Show first 10
                self.stdout.write(f'  - {pdf}')
            if len(unused_pdfs) > 10:
                self.stdout.write(f'  ... and {len(unused_pdfs) - 10} more')

    def find_matching_pdf(self, book_title, pdf_files, used_pdfs):
        """Find the best matching PDF for a book title"""
        book_title_lower = book_title.lower()
        
        # Clean title for matching
        clean_title = re.sub(r'\b(the|a|an|and|or|but|in|on|at|to|for|of|with|by)\b', '', book_title_lower)
        clean_title = re.sub(r'[^\w\s]', '', clean_title).strip()
        
        # Try exact matches first (excluding already used PDFs)
        available_pdfs = [pdf for pdf in pdf_files if pdf not in used_pdfs]
        
        for pdf in available_pdfs:
            pdf_lower = pdf.lower()
            pdf_clean = re.sub(r'[^\w\s]', '', pdf_lower).replace('_', ' ').replace('-', ' ')
            
            # Check if book title words appear in PDF name
            title_words = clean_title.split()
            if any(word in pdf_clean for word in title_words if len(word) > 2):
                return pdf
        
        # Handle specific cases
        if 'random walk' in book_title_lower:
            for pdf in available_pdfs:
                if 'random walk' in pdf.lower():
                    return pdf
        elif 'oliver' in book_title_lower:
            for pdf in available_pdfs:
                if 'oliver' in pdf.lower():
                    return pdf
        elif 'serial killer' in book_title_lower:
            for pdf in available_pdfs:
                if 'serial killer' in pdf.lower():
                    return pdf
        elif 'manga guide' in book_title_lower:
            for pdf in available_pdfs:
                if 'manga guide' in pdf.lower():
                    return pdf
        elif 'manga master' in book_title_lower:
            for pdf in available_pdfs:
                if 'manga master' in pdf.lower():
                    return pdf
        elif 'linux' in book_title_lower:
            for pdf in available_pdfs:
                if 'linux' in pdf.lower():
                    return pdf
        elif 'hacking' in book_title_lower:
            for pdf in available_pdfs:
                if 'hacking' in pdf.lower():
                    return pdf
        elif 'intelligent' in book_title_lower:
            for pdf in available_pdfs:
                if 'intelligent' in pdf.lower():
                    return pdf
        elif 'science' in book_title_lower:
            for pdf in available_pdfs:
                if 'science' in pdf.lower():
                    return pdf
        elif 'penis' in book_title_lower:
            for pdf in available_pdfs:
                if 'penis' in pdf.lower():
                    return pdf
        elif 'purple' in book_title_lower:
            for pdf in available_pdfs:
                if 'purple' in pdf.lower():
                    return pdf
        
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
