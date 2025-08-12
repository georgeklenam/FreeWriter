from django.urls import path
from . import views

urlpatterns = [
	path('all/', views.all_books, name = 'all_books'),
	path('genre/<str:slug>/', views.category_detail, name = 'category_detail'),
	path('book/<str:slug>/', views.book_detail, name = 'book_detail'),
	path('search/', views.search_book, name = 'book_search'),
	path('upload/', views.upload_book, name = 'upload_book'),
	path('register/', views.register_page, name = 'register'),
	path('login/', views.login_page, name = 'login'),
	path('logout/', views.logout_user, name = 'logout'),
	path('health/', views.health_check, name = 'health_check'),
]
