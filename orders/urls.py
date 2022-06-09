from django.urls import path
from . import views


app_name = 'orders'
urlpatterns = [
    path('', views.AllOrders.as_view(), name='orders'),
    path('<uuid:order_id>/', views.EditOrder.as_view(), name='edit_order')
]
