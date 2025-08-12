
from django import forms
from .models import BookSearch, Book, Category
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class BookSearchForm(forms.ModelForm):
	name_of_book = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
		'class': 'search-input', 'placeholder': 'Search for books...'
		}))
	class Meta:
		model = BookSearch
		fields = ['name_of_book']


class BookUploadForm(forms.ModelForm):
	title = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
		'class': 'form-control', 'placeholder': 'Enter book title'
	}))
	author = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
		'class': 'form-control', 'placeholder': 'Enter author name'
	}))
	summary = forms.CharField(widget=forms.Textarea(attrs={
		'class': 'form-control', 'rows': 4, 'placeholder': 'Enter book summary'
	}))
	cover_image = forms.ImageField(required=False, widget=forms.FileInput(attrs={
		'class': 'form-control'
	}))
	pdf = forms.FileField(required=False, widget=forms.FileInput(attrs={
		'class': 'form-control', 'accept': '.pdf'
	}))
	category = forms.ModelMultipleChoiceField(
		queryset=Category.objects.all(),
		widget=forms.CheckboxSelectMultiple(attrs={
			'class': 'form-check-input'
		})
	)
	
	class Meta:
		model = Book
		fields = ['title', 'author', 'summary', 'cover_image', 'pdf', 'category']


class CreateUserForm(UserCreationForm):
	username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
		'class': 'form-input', 'placeholder': 'Enter your username'
		}))
	email = forms.CharField(max_length=100, widget=forms.EmailInput(attrs={
		'class': 'form-input', 'placeholder': 'Enter your email address'
		}))
	password1 = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={
		'class': 'form-input', 'placeholder': 'At least eight characters'
		}))
	password2 = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={
		'class': 'form-input', 'placeholder': 'Confirm your password'
		}))

	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']



