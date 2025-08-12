
from django.shortcuts import render, redirect
from .models import Book, Category
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm, BookUploadForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
import os
import re
from django.utils import timezone

# Create your views here.


def home(request):
	"""Discription goes here
	"""
	recommended_books = Book.objects.filter(recommended_books=True)
	fiction_books = Book.objects.filter(fiction_books=True)
	business_books = Book.objects.filter(business_books=True)
	
	# If no specific books are found, show some general books
	if not recommended_books.exists():
		recommended_books = Book.objects.all()[:6]
	if not fiction_books.exists():
		fiction_books = Book.objects.all()[:6]
	if not business_books.exists():
		business_books = Book.objects.all()[:6]
	
	# Debug logging
	print(f"DEBUG: Home view - Recommended: {recommended_books.count()}, Fiction: {fiction_books.count()}, Business: {business_books.count()}")
	
	# Debug image status for each book
	for book in recommended_books:
		if book.cover_image:
			print(f"DEBUG: Recommended book {book.title} - Image: {book.cover_image.url}, Exists: {os.path.exists(book.cover_image.path)}")
		else:
			print(f"DEBUG: Recommended book {book.title} - NO IMAGE")
	
	for book in fiction_books:
		if book.cover_image:
			print(f"DEBUG: Fiction book {book.title} - Image: {book.cover_image.url}, Exists: {os.path.exists(book.cover_image.path)}")
		else:
			print(f"DEBUG: Fiction book {book.title} - NO IMAGE")
	
	for book in business_books:
		if book.cover_image:
			print(f"DEBUG: Business book {book.title} - Image: {book.cover_image.url}, Exists: {os.path.exists(book.cover_image.path)}")
		else:
			print(f"DEBUG: Business book {book.title} - NO IMAGE")
	
	return render(request, 'home.html', {'recommended_books':recommended_books,
	'fiction_books': fiction_books, 'business_books': business_books
	})

def all_books(request):
	books = Book.objects.all()
	print(f"DEBUG: Found {books.count()} books in database")
	for book in books:
		print(f"DEBUG: Book: {book.title} - {book.author}")
		if book.cover_image:
			print(f"DEBUG: Book {book.title} has cover image: {book.cover_image.url}")
			print(f"DEBUG: Image path: {book.cover_image.path}")
			print(f"DEBUG: Image exists: {os.path.exists(book.cover_image.path)}")
		else:
			print(f"DEBUG: Book {book.title} has NO cover image")
	return render(request, 'all_books.html', {'books':books})

def category_detail(request, slug):
	category = Category.objects.get(slug = slug)
	return render(request, 'genre_detail.html', {'category': category})

@login_required(login_url='login')
def book_detail(request, slug):
	book = Book.objects.get(slug = slug)
	book_category = book.category.first()
	similar_books = Book.objects.filter(category__name__startswith = book_category)
	return render(request, 'book_detail.html', {'book': book, 'similar_books': similar_books})

def search_book(request):
	searched_books = Book.objects.filter(title__icontains = request.POST.get('name_of_book'))
	return render(request, 'search_book.html', {'searched_books':searched_books})

def register_page(request):
	register_form = CreateUserForm()
	if request.method == 'POST':
		register_form = CreateUserForm(request.POST)
		if register_form.is_valid():
			register_form.save()
			messages.info(request, "Congrats New FreeWriter member!")
			return redirect('login')

	return render(request, 'register.html', {'register_form': register_form})

def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password1')
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, "Invalid Credentials")

    return render(request, 'login.html', {})


# def logout_user (request):
# 	if request.method == "GET":		
# 		logout(request)

# 		return redirect('home/')

def logout_user (request):
    logout(request)
    request.session.flush()
    #request.user = AnonymousUser
    # Redirect to a success page.
    return redirect('home')

@login_required(login_url='login')
def upload_book(request):
    """Upload a new book"""
    if request.method == 'POST':
        form = BookUploadForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            
            # Generate slug from title
            book.slug = re.sub(r'[^\w\s-]', '', book.title.lower())
            book.slug = re.sub(r'[-\s]+', '-', book.slug).strip('-')
            
            # Set recommended flags based on category
            categories = form.cleaned_data['category']
            book.recommended_books = any(cat.name.lower() in ['business', 'fiction'] for cat in categories)
            book.fiction_books = any(cat.name.lower() == 'fiction' for cat in categories)
            book.business_books = any(cat.name.lower() == 'business' for cat in categories)
            
            # Add PDFDrive.com link if no PDF is uploaded
            if not book.pdf:
                import urllib.parse
                clean_title = book.title.replace(':', '').replace('(', '').replace(')', '')
                clean_title = ' '.join(clean_title.split())
                encoded_title = urllib.parse.quote(clean_title)
                book.pdf_url = f'https://www.welib.org/search?q={encoded_title}'
            
            book.save()
            form.save_m2m()  # Save many-to-many relationships
            
            messages.success(request, f'Book "{book.title}" uploaded successfully!')
            return redirect('book_detail', slug=book.slug)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = BookUploadForm()
    
    return render(request, 'upload_book.html', {'form': form})

def media_test(request):
    """Simple view to test media file serving"""
    from django.http import HttpResponse
    import os
    
    # Check if media directory exists
    media_dir = os.path.join(settings.BASE_DIR, 'media')
    img_dir = os.path.join(media_dir, 'img')
    pdf_dir = os.path.join(media_dir, 'pdf')
    
    response = f"""
    <h1>Media Test</h1>
    <p>BASE_DIR: {settings.BASE_DIR}</p>
    <p>Media directory exists: {os.path.exists(media_dir)}</p>
    <p>Image directory exists: {os.path.exists(img_dir)}</p>
    <p>PDF directory exists: {os.path.exists(pdf_dir)}</p>
    """
    
    if os.path.exists(img_dir):
        img_files = os.listdir(img_dir)
        response += f"<p>Image files: {img_files}</p>"
    
    if os.path.exists(pdf_dir):
        pdf_files = os.listdir(pdf_dir)
        response += f"<p>PDF files: {pdf_files}</p>"
    
    # Check books in database
    books = Book.objects.all()
    response += f"<p>Books in database: {books.count()}</p>"
    for book in books:
        response += f"<p>Book: {book.title} - Cover: {book.cover_image if book.cover_image else 'None'}</p>"
    
    return HttpResponse(response)

def health_check(request):
    """Simple health check endpoint for monitoring"""
    from django.http import JsonResponse
    return JsonResponse({
        'status': 'healthy',
        'message': 'FreeWriter is running',
        'books_count': Book.objects.count(),
        'timestamp': timezone.now().isoformat()
    })
