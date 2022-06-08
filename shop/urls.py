from django.urls import path
from . import views


app_name = 'shop'
urlpatterns = [
    path('products/', views.AllProducts.as_view(), name='products'),
    path('categories/', views.AllCategories.as_view(), name='categories'),
    path('products/<uuid:product_id>/', views.EditProduct.as_view(), name='edit_product'),
    path('categories/<uuid:category_id>/', views.EditCategory.as_view(), name='edit_category'),
]
