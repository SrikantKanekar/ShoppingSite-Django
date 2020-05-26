from .models import Category, Product, Profile, Admin, Notification


def add_variable_to_context(request):
    if request.user.is_authenticated:
        wishlist_count = Profile.objects.get(user=request.user).wishlist_products.all().count()
        cart_count = Profile.objects.get(user=request.user).cart_products.all().count()
        order_count = Admin.objects.filter(customer=request.user).count()
        notification_count = Notification.objects.filter(user=request.user, close=False).count()
        notification_new_count = Notification.objects.filter(user=request.user, seen=False).count()
        return {
            'order_count': order_count,
            'wishlist_count': wishlist_count,
            'cart_count': cart_count,
            'notification_count': notification_count,
            'notification_new_count': notification_new_count,
        }
    else:
        return {}

