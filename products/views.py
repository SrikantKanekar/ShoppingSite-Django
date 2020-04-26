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


def faq(request):
    return render(request, 'template/faq.html')


def contact_us(request):
    return render(request, 'template/Contact us.html')


def Cart(request):
    return render(request, 'template/Cart.html')


def order_track(request):
    return render(request, 'template/Order track.html')


def about_us(request):
    return render(request, 'template/About us.html')


def services(request):
    return render(request, 'template/services.html')
