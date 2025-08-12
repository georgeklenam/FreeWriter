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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

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