from django.contrib import admin
from .models import Category, Book, BookSearch
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'book_count')
    list_filter = ('name',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('name',)
    
    def book_count(self, obj):
        return obj.books.count()
    book_count.short_description = 'Number of Books'

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'get_categories', 'recommended_books', 'fiction_books', 'business_books', 'has_pdf', 'has_image')
    list_filter = ('recommended_books', 'fiction_books', 'business_books', 'category')
    search_fields = ('title', 'author', 'summary')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('category',)
    readonly_fields = ('pdf_url',)
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'author', 'summary')
        }),
        ('Categories', {
            'fields': ('category',)
        }),
        ('Flags', {
            'fields': ('recommended_books', 'fiction_books', 'business_books'),
            'classes': ('collapse',)
        }),
        ('Files', {
            'fields': ('cover_image', 'pdf', 'pdf_url'),
            'classes': ('collapse',)
        }),
    )
    
    def get_categories(self, obj):
        return ", ".join([cat.name for cat in obj.category.all()])
    get_categories.short_description = 'Categories'
    
    def has_pdf(self, obj):
        return bool(obj.pdf)
    has_pdf.boolean = True
    has_pdf.short_description = 'Has PDF'
    
    def has_image(self, obj):
        return bool(obj.cover_image)
    has_image.boolean = True
    has_image.short_description = 'Has Image'

class BookSearchAdmin(admin.ModelAdmin):
    list_display = ('name_of_book', 'created_at')
    search_fields = ('name_of_book',)
    readonly_fields = ('created_at',)
    
    def created_at(self, obj):
        return obj.id  # Since BookSearch doesn't have timestamps, using ID as proxy
    created_at.short_description = 'Search ID'

# Register models with enhanced admin
admin.site.register(Category, CategoryAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(BookSearch, BookSearchAdmin)

# Customize admin site
admin.site.site_header = "FreeWriter Administration"
admin.site.site_title = "FreeWriter Admin Portal"
admin.site.index_title = "Welcome to FreeWriter Admin Portal"
