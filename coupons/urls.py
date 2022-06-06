from django.urls import path
from . import views


app_name = 'coupons'
urlpatterns = [
    path('coupons/', views.coupons, name='coupons'),
    path('coupons/<uuid:coupon_id>/', views.edit_coupons, name='edit_coupons')
]
