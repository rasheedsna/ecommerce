from django.urls import path
from . import views


app_name = 'shop'
urlpatterns = [
    path('products/', views.all_products, name='products'),
    path('categories/', views.all_categories, name='categories'),
]
