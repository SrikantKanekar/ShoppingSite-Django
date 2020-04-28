from django.urls import path
from . import views


urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('Category/<slug:slug>/', views.show_category, name='category'),
    path('Category/<slug:slug>/', views.show_category, name='show_category'),
    path('Product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('faq/', views.faq, name='faq'),
    path('contact_us/', views.contact_us, name='contact_us'),
    path('cart/', views.Cart, name='cart'),
    path('about_us/', views.about_us, name='about_us'),
    path('checkout/', views.checkout, name='checkout'),
    path('track_order/', views.track_order, name='order_track'),
    path('services/', views.services, name='services'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('user/', views.user, name='user'),
    path('user/update_profile', views.update_profile, name='update_profile'),
]
