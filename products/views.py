from django.shortcuts import render, redirect
from .models import Category, Product
from django.contrib.auth import authenticate, login
from .forms import UserLoginForm, UsersRegisterForm


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


def login_view(request):
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect("/")
    return render(request, "registration/login.html", {
        'form': form,
        'title': 'login',
    })


def register_view(request):
    form = UsersRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        password = form.cleaned_data.get("password")
        user.set_password(password)
        user.save()
        new_user = authenticate(username=user.username, password=password)
        login(request, new_user)
        return redirect("/")
    return render(request, "registration/login.html", {
        "title": "register",
        "form": form,
    })
