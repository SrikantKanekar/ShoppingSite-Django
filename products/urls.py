from django.urls import path
from . import views


urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('<slug:slug>/', views.show_category, name='category'),
    path('<slug:slug>/', views.show_category, name='show_category'),
    path('<slug:slug>', views.product_detail, name='product_detail'),
]
