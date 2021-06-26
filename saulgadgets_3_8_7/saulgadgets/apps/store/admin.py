from django.contrib import admin

# Register your models here.
from .models import Category, Product
# Register your models here.
admin.site.register(Category)
admin.site.register(Product)