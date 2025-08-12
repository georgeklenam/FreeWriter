from .models import Category
from .forms import BookSearchForm
from .utils import get_category_icon

def category_links(request):
    categories = Category.objects.all()
    # Add icons to each category
    for category in categories:
        category.icon = get_category_icon(category.name)
    return {'categories': categories}

def book_search(request):
    search_form = BookSearchForm()
    return {'search_form': search_form}