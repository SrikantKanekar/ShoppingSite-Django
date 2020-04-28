from django.contrib import admin
from .models import Product, Category, Profile
from mptt.admin import MPTTModelAdmin

admin.site.register(Product)
admin.site.register(Category, MPTTModelAdmin)
admin.site.register(Profile)
