from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = "Categories"
    
    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    summary = models.TextField()
    cover_image = models.ImageField(upload_to='img/', blank=True, null=True)
    pdf = models.FileField(upload_to='pdf/', blank=True, null=True)
    pdf_url = models.URLField(blank=True, null=True, help_text='Welib.org link as fallback')
    category = models.ManyToManyField(Category)
    slug = models.SlugField(unique=True)
    recommended_books = models.BooleanField(default=False)
    fiction_books = models.BooleanField(default=False)
    business_books = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    def __str__(self):
        return self.title
    
    @property
    def average_rating(self):
        """Calculate average rating for the book"""
        ratings = self.ratings.all()
        if not ratings:
            return 0
        return sum(rating.rating for rating in ratings) / len(ratings)
    
    @property
    def rating_count(self):
        """Get total number of ratings"""
        return self.ratings.count()
    
    @property
    def review_count(self):
        """Get total number of reviews"""
        return self.reviews.count()

class BookSearch(models.Model):
    name_of_book = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name_of_book

class NewsletterSubscription(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True)
    
    class Meta:
        verbose_name = "Newsletter Subscription"
        verbose_name_plural = "Newsletter Subscriptions"
        ordering = ['-subscribed_at']
    
    def __str__(self):
        return self.email

class UserProfile(models.Model):
    USER_TYPE_CHOICES = [
        ('reader', 'Reader'),
        ('writer', 'Writer'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='reader')
    bio = models.TextField(blank=True, max_length=500)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"
    
    def __str__(self):
        return f"{self.user.username}'s Profile"

class BookRating(models.Model):
    RATING_CHOICES = [
        (1, '1 - Poor'),
        (2, '2 - Fair'),
        (3, '3 - Good'),
        (4, '4 - Very Good'),
        (5, '5 - Excellent'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='ratings')
    rating = models.IntegerField(choices=RATING_CHOICES)
    review = models.TextField(blank=True, max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['user', 'book']
        verbose_name = "Book Rating"
        verbose_name_plural = "Book Ratings"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} rated {self.book.title} {self.rating}/5"

class BookReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    title = models.CharField(max_length=200)
    content = models.TextField(max_length=2000)
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Book Review"
        verbose_name_plural = "Book Reviews"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username}'s review of {self.book.title}"