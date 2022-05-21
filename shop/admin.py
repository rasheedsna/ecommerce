from django.contrib import admin
from . models import Product, Category, Type, SubCategory, Tag


admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Type)
admin.site.register(SubCategory)
admin.site.register(Tag)
