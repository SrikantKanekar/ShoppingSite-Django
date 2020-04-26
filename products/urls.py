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
    path('order_track/', views.order_track, name='order_track'),
]
