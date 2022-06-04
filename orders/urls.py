from django.urls import path
from . import views


app_name = 'orders'
urlpatterns = [
    path('orders/', views.all_orders, name='orders'),
    path('orders/<uuid:order_id>/', views.edit_order, name='edit_order')
]
