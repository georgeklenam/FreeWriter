from django.core.management.base import BaseCommand
from bookapp.models import Book
from django.core.files import File
import os
import re

class Command(BaseCommand):
    help = 'Fix missing PDF files for existing books'

    def handle(self, *args, **options):
        self.stdout.write('Fixing missing PDF files...')
        
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
        
        for book in books:
            self.stdout.write(f'Processing book: {book.title}')
            
            # Check if book already has a PDF
            if book.pdf:
                self.stdout.write(f'  - Book already has PDF: {book.pdf.name}')
                continue
            
            # Try to find a matching PDF for this book
            matching_pdf = self.find_matching_pdf(book.title, pdf_files)
            
            if matching_pdf:
                pdf_path = os.path.join(pdf_dir, matching_pdf)
                
                # Assign the PDF to the book
                with open(pdf_path, 'rb') as pdf_file:
                    book.pdf.save(matching_pdf, File(pdf_file), save=True)
                self.stdout.write(f'  - Assigned PDF: {matching_pdf}')
                fixed_count += 1
            else:
                self.stdout.write(f'  - No matching PDF found for: {book.title}')
                # Add PDFDrive.com link as fallback
                pdfdrive_url = self.generate_pdfdrive_url(book.title)
                book.pdf_url = pdfdrive_url
                book.save()
                self.stdout.write(f'  - Added PDFDrive link: {pdfdrive_url}')
                fixed_count += 1
        
        self.stdout.write(self.style.SUCCESS(f'Fixed {fixed_count} PDF references!'))
        
        # Show remaining unused PDFs
        used_pdfs = [book.pdf.name.split('/')[-1] for book in Book.objects.filter(pdf__isnull=False)]
        unused_pdfs = [pdf for pdf in pdf_files if pdf not in used_pdfs]
        
        if unused_pdfs:
            self.stdout.write(f'\nUnused PDFs ({len(unused_pdfs)}):')
            for pdf in unused_pdfs[:10]:  # Show first 10
                self.stdout.write(f'  - {pdf}')
            if len(unused_pdfs) > 10:
                self.stdout.write(f'  ... and {len(unused_pdfs) - 10} more')

    def find_matching_pdf(self, book_title, pdf_files):
        """Find the best matching PDF for a book title"""
        book_title_lower = book_title.lower()
        
        # Clean title for matching
        clean_title = re.sub(r'\b(the|a|an|and|or|but|in|on|at|to|for|of|with|by)\b', '', book_title_lower)
        clean_title = re.sub(r'[^\w\s]', '', clean_title).strip()
        
        # Try exact matches first
        for pdf in pdf_files:
            pdf_lower = pdf.lower()
            pdf_clean = re.sub(r'[^\w\s]', '', pdf_lower).replace('_', ' ').replace('-', ' ')
            
            # Check if book title words appear in PDF name
            title_words = clean_title.split()
            if any(word in pdf_clean for word in title_words if len(word) > 2):
                return pdf
        
        # Handle specific cases
        if 'random walk' in book_title_lower:
            return 'A_Random_Walk_Down_Wall_Street.pdf'
        elif 'oliver' in book_title_lower:
            return 'oliver-twist.pdf'
        elif 'serial killer' in book_title_lower:
            return 'My_Sister_the_Serial_Killer.pdf'
        elif 'manga guide' in book_title_lower:
            return 'The_Manga_Guide_to_Molecular_Biology__PDFDrive_.pdf'
        elif 'manga master' in book_title_lower:
            return 'Mastering_Manga_How_to_Draw_Manga_Faces__PDFDrive_.pdf'
        elif 'linux' in book_title_lower:
            return 'Linux_Tips_Tricks_PPS__Hacks_Vol_3.pdf'
        elif 'hacking' in book_title_lower:
            return 'The_Basics_Of_Hacking_And_Penetration_Testing__Ethical_Hacking_And_Penetration_Testing.pdf'
        elif 'intelligent' in book_title_lower:
            return 'The_Intelligent_Investor.pdf'
        elif 'science' in book_title_lower:
            return 'The_Handy_Science_Answer_Book_The_Handy_Answer_Book_Series____PDFDrive_.pdf'
        elif 'penis' in book_title_lower:
            return 'Penis_Exercises_A_Healthy_Book_for_Enlargement_Enhancement_Hardness__Health__PDFDrive_.pdf'
        elif 'purple' in book_title_lower:
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
