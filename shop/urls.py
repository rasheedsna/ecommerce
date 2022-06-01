from django.urls import path
from . import views


app_name = 'shop'
urlpatterns = [
    path('products/', views.all_products, name='products'),
    path('categories/', views.all_categories, name='categories'),
    path('products/<uuid:product_id>/', views.edit_products, name='edit_products'),
    path('categories/<uuid:category_id>/', views.edit_categories, name='edit_categories'),
]
