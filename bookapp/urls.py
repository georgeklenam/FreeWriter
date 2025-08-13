from django.urls import path
from . import views

urlpatterns = [
	path('all/', views.all_books, name = 'all_books'),
	path('genre/<str:slug>/', views.category_detail, name = 'category_detail'),
	path('book/<str:slug>/', views.book_detail, name = 'book_detail'),
	path('book/<str:slug>/review/', views.add_review, name = 'add_review'),
	path('search/', views.search_book, name = 'book_search'),
	path('upload/', views.upload_book, name = 'upload_book'),
	path('register/', views.register_page, name = 'register'),
	path('login/', views.login_page, name = 'login'),
	path('logout/', views.logout_user, name = 'logout'),
	path('health/', views.health_check, name = 'health_check'),
	path('newsletter/subscribe/', views.newsletter_subscribe, name = 'newsletter_subscribe'),
	path('about/', views.about, name = 'about'),
]
