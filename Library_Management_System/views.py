from django.shortcuts import render
from book.models import Book
from category.models import Category

def home(request,category_slug = None):
    data = Book.objects.all()
    if category_slug is not None:
        category = Category.objects.get(slug = category_slug)
        data = Book.objects.filter(category = category)
    categories = Category.objects.all()
    return render(request, 'home.html', {'book' : data, 'category' : categories})