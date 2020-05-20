from django.shortcuts import render, redirect, HttpResponseRedirect
from .models import Category, Product, Profile, Comment, Admin
from django.contrib.auth import authenticate, login
from .forms import UserLoginForm, UsersRegisterForm
from .forms import ProfileForm, UserForm, CommentForm, AddressForm, CheckoutForm, ProfilePicForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q


def homepage(request):
    category = Category.objects.filter(level=0)
    return render(request, 'template/homepage.html', {'category': category})


def show_category(request, slug):
    parent = Category.objects.get(slug=slug)
    product = Product.objects.filter(category=parent)
    return render(request, 'template/categories.html', {'sub': parent, 'product': product})


def product_detail(request, slug):
    product = Product.objects.get(slug=slug)
    off = round((product.original_price - product.offer_price) / product.original_price * 100)
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        comments = Comment.objects.filter(product=product)
        comment_count = comments.count()
        if request.method == "POST":
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.product = product
                comment.user = request.user
                comment.save()
                return redirect('product_detail', slug=product.slug)
        else:
            comment_form = CommentForm()
            return render(request, 'template/product_detail.html', {'product': product, 'profile': profile, 'comment_form': comment_form, 'comments': comments, 'comment_count': comment_count, 'off': off})
    else:
        comments = Comment.objects.filter(product=product)
        comment_count = comments.count()
        return render(request, 'template/product_detail.html', {'product': product, 'comments': comments, 'comment_count': comment_count, 'off': off})


def faq(request):
    return render(request, 'template/faq.html')


def contact_us(request):
    return render(request, 'template/Contact us.html')


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


def user(request):
    profile = Profile.objects.get(user=request.user)
    return render(request, 'template/user.html', {'profile': profile})


@login_required
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('/user/')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'registration/update_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


@login_required
def update_profile_pic(request):
    if request.method == 'POST':
        profile_pic_form = ProfilePicForm(request.POST, request.FILES, instance=request.user.profile)
        if profile_pic_form.is_valid():
            profile_pic_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('/user/')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        profile_pic_form = ProfilePicForm(instance=request.user.profile)
        return render(request, 'registration/update_profile_pic.html', {
            'profile_pic_form': profile_pic_form
        })


@login_required
def update_address(request):
    if request.method == 'POST':
        profile_form = AddressForm(request.POST, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('/user/')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        profile_form = AddressForm(instance=request.user.profile)
    return render(request, 'registration/update_address.html', {
        'profile_form': profile_form
    })


def search(request):
    if request.method == 'GET':
        query = request.GET.get('q')
        submitbutton = request.GET.get('submit')
        if query is not None:
            lookups = Q(title__icontains=query)
            results = Product.objects.filter(lookups).distinct()
            context = {'results': results,
                       'submitbutton': submitbutton}
            return render(request, 'template/search.html', context)
        else:
            return render(request, 'template/search.html')
    else:
        return render(request, 'template/search.html')


def wishlist(request):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        count = profile.wishlist_products.all().count()
        return render(request, 'template/wishlist.html', {'profile': profile, 'count': count})
    else:
        return render(request, 'template/wishlist.html')


def wishlist_update(request, product_id):
    product_obj = Product.objects.get(id=product_id)
    profile = Profile.objects.get(user=request.user)
    if product_obj in profile.wishlist_products.all():
        profile.wishlist_products.remove(product_obj)
    else:
        profile.wishlist_products.add(product_obj)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def cart(request):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        count = profile.cart_products.all().count()
        products = profile.cart_products.all()
        total_offer = 0
        total_original = 0
        for x in products:
            total_original += x.original_price
            total_offer += x.offer_price
        profile.total_offer = total_offer
        profile.total_original = total_original
        profile.total = 250 + total_offer
        profile.save()
        discount = total_original - total_offer
        return render(request, 'template/Cart.html', {'profile': profile, 'count': count, 'discount': discount})
    else:
        return render(request, 'template/Cart.html')


def cart_update(request, product_id):
    product_obj = Product.objects.get(id=product_id)
    profile = Profile.objects.get(user=request.user)
    if product_obj in profile.cart_products.all():
        profile.cart_products.remove(product_obj)
    else:
        profile.cart_products.add(product_obj)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def checkout(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        checkout_form = CheckoutForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and checkout_form.is_valid():
            user_form.save()
            checkout_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('/order_history_update/')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        user_form = UserForm(instance=request.user)
        checkout_form = CheckoutForm(instance=request.user.profile)
        profile = Profile.objects.get(user=request.user)
        count = profile.cart_products.all().count()
        products = profile.cart_products.all()
        total_offer = 0
        for x in products:
            total_offer += x.offer_price
        profile.total = 250 + total_offer
        profile.save()
        return render(request, 'template/checkout.html', {
            'user_form': user_form,
            'checkout_form': checkout_form,
            'profile': profile,
            'count': count
        })


def order_history(request):
    if request.user.is_authenticated:
        orders = Admin.objects.filter(customer=request.user)
        count = orders.count()
        return render(request, 'template/order_history.html', {'orders': orders, 'count': count})
    else:
        return render(request, 'template/order_history.html')


def order_history_update(request):
    profile = Profile.objects.get(user=request.user)
    for ordered_products in profile.cart_products.all():
        Admin.objects.create(ordered_product=ordered_products, customer=profile.user)
        profile.cart_products.remove(ordered_products)
    return redirect('/order_history/')


def track_order(request, order_id):
    order = Admin.objects.get(id=order_id)
    return render(request, 'template/track_order.html', {'order': order})


def admin_page(request):
    orders = Admin.objects.all()
    count = orders.count()
    return render(request, 'template/admin_page.html', {'orders': orders,
                                                        'count': count})


def admin_product_page(request, order_id):
    order = Admin.objects.get(id=order_id)
    return render(request, 'template/admin_product_page.html', {'order': order})


def admin_status_update(request, order_id, status):
    order = Admin.objects.get(id=order_id)
    order.status = status
    order.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
