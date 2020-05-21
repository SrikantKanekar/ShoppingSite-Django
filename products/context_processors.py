from .models import Category, Product, Profile, Comment, Admin


def add_variable_to_context(request):
    wishlist_count = Profile.objects.get(user=request.user).wishlist_products.all().count()
    cart_count = Profile.objects.get(user=request.user).cart_products.all().count()
    order_count = Admin.objects.filter(customer=request.user).count()
    return {
        'order_count': order_count,
        'wishlist_count': wishlist_count,
        'cart_count': cart_count,
    }