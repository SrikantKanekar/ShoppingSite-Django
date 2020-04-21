from django.shortcuts import render
from .models import Category, Product


def homepage(request):
    category = Category.objects.filter(level=0)
    return render(request, 'template/homepage.html', {'category': category})


def show_category(request, slug):
    parent = Category.objects.get(slug=slug)
    product = Product.objects.filter(category=parent)
    return render(request, 'template/categories.html', {'sub': parent, 'product': product})


def product_detail(request, slug):
    product = Product.objects.get(slug=slug)
    return render(request, 'template/product_detail.html', {'product': product})
