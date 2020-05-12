from django.contrib import admin
from .models import Product, Category, Profile, Comment, Admin
from mptt.admin import MPTTModelAdmin

admin.site.register(Product)
admin.site.register(Category, MPTTModelAdmin)
admin.site.register(Profile)
admin.site.register(Comment)
admin.site.register(Admin)


