
from django.shortcuts import render, redirect, get_object_or_404
from .models import Book, Category, NewsletterSubscription, BookRating, BookReview, UserProfile
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm, BookUploadForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import os
import re
from django.utils import timezone
import json
from django.db import models

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
	book = get_object_or_404(Book, slug=slug)
	book_category = book.category.first()
	similar_books = Book.objects.filter(category__name__startswith = book_category)
	return render(request, 'book_detail.html', {'book': book, 'similar_books': similar_books})

@login_required(login_url='login')
def add_review(request, slug):
    """Add a review and rating for a book"""
    if request.method == 'POST':
        book = get_object_or_404(Book, slug=slug)
        rating = request.POST.get('rating')
        review_title = request.POST.get('review_title')
        review_content = request.POST.get('review_content')
        
        if rating and review_title and review_content:
            # Create or update rating
            rating_obj, created = BookRating.objects.get_or_create(
                user=request.user,
                book=book,
                defaults={'rating': rating}
            )
            if not created:
                rating_obj.rating = rating
                rating_obj.save()
            
            # Create review
            review = BookReview.objects.create(
                user=request.user,
                book=book,
                title=review_title,
                content=review_content
            )
            
            messages.success(request, 'Your review has been submitted successfully!')
        else:
            messages.error(request, 'Please fill in all fields.')
    
    return redirect('book_detail', slug=slug)

@login_required(login_url='login')
def read_book(request, slug):
    """Read a book on the platform"""
    book = get_object_or_404(Book, slug=slug)
    return render(request, 'read_book.html', {'book': book})

@login_required(login_url='login')
def dashboard(request):
    """User dashboard based on user type"""
    user = request.user
    
    if hasattr(user, 'profile') and user.profile.user_type == 'writer':
        # Writer dashboard
        uploaded_books = Book.objects.filter(author=user.username).order_by('-created_at')
        total_books = uploaded_books.count()
        total_ratings = sum(book.rating_count for book in uploaded_books)
        total_reviews = sum(book.review_count for book in uploaded_books)
        average_rating = uploaded_books.aggregate(avg_rating=models.Avg('ratings__rating'))['avg_rating'] or 0
        
        context = {
            'user_type': 'writer',
            'uploaded_books': uploaded_books,
            'total_books': total_books,
            'total_ratings': total_ratings,
            'total_reviews': total_reviews,
            'average_rating': round(average_rating, 1),
        }
    else:
        # Reader dashboard
        user_ratings = BookRating.objects.filter(user=user).order_by('-created_at')
        user_reviews = BookReview.objects.filter(user=user).order_by('-created_at')
        total_books_read = user_ratings.count()
        total_reviews_written = user_reviews.count()
        average_rating_given = user_ratings.aggregate(avg_rating=models.Avg('rating'))['avg_rating'] or 0
        
        # Get recently read books
        recently_read = Book.objects.filter(ratings__user=user).distinct().order_by('-ratings__created_at')[:5]
        
        context = {
            'user_type': 'reader',
            'user_ratings': user_ratings,
            'user_reviews': user_reviews,
            'total_books_read': total_books_read,
            'total_reviews_written': total_reviews_written,
            'average_rating_given': round(average_rating_given, 1),
            'recently_read': recently_read,
        }
    
    return render(request, 'dashboard.html', context)

def search_book(request):
    """Enhanced search with filters"""
    if request.method == 'POST':
        query = request.POST.get('name_of_book', '')
        category_filter = request.POST.get('category', '')
        author_filter = request.POST.get('author', '')
    else:
        # Handle GET requests for filter removal
        query = request.GET.get('name_of_book', '')
        category_filter = request.GET.get('category', '')
        author_filter = request.GET.get('author', '')
    
    # Start with all books
    books = Book.objects.all()
    
    # Apply search filters
    if query:
        books = books.filter(
            models.Q(title__icontains=query) |
            models.Q(author__icontains=query) |
            models.Q(summary__icontains=query)
        )
    
    if category_filter:
        books = books.filter(category__name__icontains=category_filter)
    
    if author_filter:
        books = books.filter(author__icontains=author_filter)
    
    # Get all categories for filter dropdown
    categories = Category.objects.all()
    
    # Get unique authors for filter dropdown
    authors = Book.objects.values_list('author', flat=True).distinct()
    
    context = {
        'searched_books': books,
        'query': query,
        'categories': categories,
        'authors': authors,
        'selected_category': category_filter,
        'selected_author': author_filter,
    }
    
    return render(request, 'search_book.html', context)

def register_page(request):
	register_form = CreateUserForm()
	if request.method == 'POST':
		register_form = CreateUserForm(request.POST)
		if register_form.is_valid():
			user = register_form.save()
			
			# Update user profile with user type
			user_type = register_form.cleaned_data.get('user_type', 'reader')
			if hasattr(user, 'profile'):
				user.profile.user_type = user_type
				user.profile.save()
			
			messages.info(request, f"Welcome to FreeWriter! You've joined as a {user_type.title()}.")
			return redirect('home')

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
    return JsonResponse({
        'status': 'healthy',
        'message': 'FreeWriter is running',
        'books_count': Book.objects.count(),
        'timestamp': timezone.now().isoformat()
    })

@csrf_exempt
@require_POST
def newsletter_subscribe(request):
    """Handle newsletter subscription"""
    try:
        data = json.loads(request.body)
        email = data.get('email', '').strip()
        
        if not email:
            return JsonResponse({'success': False, 'message': 'Email is required'}, status=400)
        
        # Basic email validation
        if '@' not in email or '.' not in email:
            return JsonResponse({'success': False, 'message': 'Please enter a valid email address'}, status=400)
        
        # Check if already subscribed
        if NewsletterSubscription.objects.filter(email=email, is_active=True).exists():
            return JsonResponse({'success': False, 'message': 'You are already subscribed to our newsletter!'}, status=400)
        
        # Create or reactivate subscription
        subscription, created = NewsletterSubscription.objects.get_or_create(
            email=email,
            defaults={
                'is_active': True,
                'ip_address': request.META.get('REMOTE_ADDR'),
                'user_agent': request.META.get('HTTP_USER_AGENT', '')
            }
        )
        
        if not created:
            subscription.is_active = True
            subscription.save()
        
        return JsonResponse({
            'success': True, 
            'message': 'Thank you for subscribing to our newsletter!'
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'Invalid request data'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'message': 'An error occurred. Please try again.'}, status=500)

def privacy_policy(request):
    """Privacy Policy page"""
    return render(request, 'privacy_policy.html')

def terms_of_service(request):
    """Terms of Service page"""
    return render(request, 'terms_of_service.html')

def cookie_policy(request):
    """Cookie Policy page"""
    return render(request, 'cookie_policy.html')

def about(request):
    """About page"""
    return render(request, 'about.html')
