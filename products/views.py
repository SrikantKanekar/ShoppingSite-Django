from django.shortcuts import render, redirect, HttpResponseRedirect
from .models import Category, Product, Profile, Comment, Admin, Notification
from django.contrib.auth import authenticate, login
from .forms import UserLoginForm, UsersRegisterForm, UserForm
from .forms import ProfileForm, CommentForm, AddressForm, CheckoutForm, ProfilePicForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils import timezone
from django.template.loader import render_to_string
from django.http import JsonResponse


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
            return render(request, 'template/product_detail.html',
                          {'product': product, 'profile': profile, 'comment_form': comment_form, 'comments': comments,
                           'comment_count': comment_count, 'off': off})
    else:
        comments = Comment.objects.filter(product=product)
        comment_count = comments.count()
        return render(request, 'template/product_detail.html',
                      {'product': product, 'comments': comments, 'comment_count': comment_count, 'off': off})


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


@login_required
def user(request):
    profile = Profile.objects.get(user=request.user)
    return render(request, 'template/user/user.html', {'profile': profile})


def update_profile(request):
    data = dict()
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            profile = Profile.objects.get(user=request.user)
            request.user.first_name = profile.first_name
            request.user.last_name = profile.last_name
            request.user.email = profile.email
            request.user.save()
            data['profile'] = render_to_string('template/user/profile_name.html', {'profile': profile})
        else:
            data['form_is_valid'] = False
    else:
        form = ProfileForm(instance=request.user.profile)
    data['html_form'] = render_to_string('template/user/update_profile.html',
                                         {'profile_form': form}, request=request)
    return JsonResponse(data)


def update_profile_pic(request):
    if request.method == 'POST':
        profile_pic_form = ProfilePicForm(request.POST, request.FILES, instance=request.user.profile)
        if profile_pic_form.is_valid():
            profile_pic_form.save()
            messages.success(request, 'Profile updated!')
            return redirect('/user/')
        else:
            messages.error(request, 'Error')
    else:
        profile_pic_form = ProfilePicForm(instance=request.user.profile)
        return render(request, 'template/user/update_profile_pic.html', {
            'profile_pic_form': profile_pic_form
        })


def update_address(request):
    data = dict()
    if request.method == 'POST':
        form = AddressForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            profile = Profile.objects.get(user=request.user)
            data['profile'] = render_to_string('template/user/profile_name.html', {'profile': profile})
        else:
            data['form_is_valid'] = False
    else:
        form = AddressForm(instance=request.user.profile)
    data['html_form'] = render_to_string('template/user/update_address.html',
                                         {'profile_form': form}, request=request)
    return JsonResponse(data)


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
        return render(request, 'template/wishlist.html', {'profile': profile})
    else:
        return render(request, 'template/wishlist.html')


def wishlist_update(request, product_id):
    product_obj = Product.objects.get(id=product_id)
    profile = Profile.objects.get(user=request.user)
    if product_obj in profile.wishlist_products.all():
        profile.wishlist_products.remove(product_obj)
        messages.error(request, 'Removed from Wishlist')
    else:
        profile.wishlist_products.add(product_obj)
        messages.success(request, 'Added to Wishlist')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def cart(request):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
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
        return render(request, 'template/Cart.html', {'profile': profile, 'discount': discount})
    else:
        return render(request, 'template/Cart.html')


def cart_update(request, product_id):
    product_obj = Product.objects.get(id=product_id)
    profile = Profile.objects.get(user=request.user)
    if product_obj in profile.cart_products.all():
        profile.cart_products.remove(product_obj)
        messages.error(request, 'Removed from Cart')
    else:
        profile.cart_products.add(product_obj)
        messages.success(request, 'Added to Cart')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def checkout(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        checkout_form = CheckoutForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and checkout_form.is_valid():
            user_form.save()
            checkout_form.save()
            messages.success(request, 'Order placed!')
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
        return render(request, 'template/order_history.html', {'orders': orders})
    else:
        return render(request, 'template/order_history.html')


def order_history_update(request):
    profile = Profile.objects.get(user=request.user)
    for ordered_products in profile.cart_products.all():
        admin = Admin.objects.create(ordered_product=ordered_products, customer=profile.user)
        Notification.objects.create(order=admin, user=profile.user)
        profile.cart_products.remove(ordered_products)
    return redirect('/order_history/')


def track_order(request, order_id):
    order = Admin.objects.get(id=order_id)
    delivery_list1 = [0, 1, 2, 3, 4, 5]
    delivery_list = {0: {'Order Placed': order.order_placed_date},
                     1: {'Order Confirmed': order.order_confirmed_date},
                     2: {'Packing': order.packing_date},
                     3: {'Shipped': order.shipped_date},
                     4: {'Out for Delivery': order.out_for_delivery_date},
                     5: {'Delivered': order.delivered_date},
                     }
    cancel_list = [0, 1, 2]
    return_list1 = [7, 8, 9, 10, 11]
    return_list = {7: {'Return Request Placed': order.return_request_placed_date},
                   8: {'Return Request Acknowledged': order.return_request_acknowledged_date},
                   9: {'Courier Service Informed': order.courier_service_informed_date},
                   10: {'Return Product Verified': order.return_product_verified_date},
                   11: {'Refund Completed': order.refund_completed_date}
                   }
    return render(request, 'template/track_order.html', {'order': order,
                                                         'delivery_list1': delivery_list1,
                                                         'delivery_list': delivery_list,
                                                         'cancel_list': cancel_list,
                                                         'return_list1': return_list1,
                                                         'return_list': return_list,
                                                         })


def admin_page(request):
    orders = Admin.objects.all()
    return render(request, 'template/admin_page.html', {'orders': orders})


def admin_product_page(request, order_id):
    order = Admin.objects.get(id=order_id)
    return render(request, 'template/admin_product_page.html', {'order': order})


def admin_status_update(request, order_id, status):
    order = Admin.objects.get(id=order_id)
    notification = Notification.objects.get(id=order_id)
    if int(status) == 1:
        order.order_confirmed_date = timezone.now()
    elif int(status) == 2:
        order.packing_date = timezone.now()
    elif int(status) == 3:
        order.shipped_date = timezone.now()
    elif int(status) == 4:
        order.out_for_delivery_date = timezone.now()
    elif int(status) == 5:
        order.delivered_date = timezone.now()
        order.delivered = True
    elif int(status) == 7:
        order.return_request_placed_date = timezone.now()
    elif int(status) == 8:
        order.return_request_acknowledged_date = timezone.now()
    elif int(status) == 9:
        order.courier_service_informed_date = timezone.now()
    elif int(status) == 10:
        order.return_product_verified_date = timezone.now()
    elif int(status) == 11:
        order.refund_completed_date = timezone.now()
    order.status = status
    notification.text = status
    notification.close = False
    notification.seen = False
    order.save()
    notification.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def notification(request):
    notifications = Notification.objects.all()
    return render(request, 'template/notification/notification.html', {'notifications': notifications})


def notification_info(request, notification_id):
    notification = Notification.objects.get(id=notification_id)
    notification.seen = True
    notification.save()
    return render(request, 'template/notification/notification_info.html', {'notification': notification})


def notification_close(request, pk):
    data = dict()
    notification = Notification.objects.get(id=pk)
    notification.close = True
    notification.seen = True
    notification.save()
    notifications = Notification.objects.all()
    notification_count = Notification.objects.filter(user=request.user, close=False).count()
    notification_new_count = Notification.objects.filter(user=request.user, seen=False).count()
    data['notification_list'] = render_to_string('template/notification/notification_list.html',
                                                 {'notifications': notifications})
    data['notification_new_count'] = notification_new_count
    if notification_count == 0:
        data['notification_count'] = True
    return JsonResponse(data)
