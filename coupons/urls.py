from django.urls import path
from . import views


app_name = 'coupons'
urlpatterns = [
    path('', views.AllCouponsView.as_view(), name='coupons'),
    path('<uuid:coupon_id>/', views.EditCoupons.as_view(), name='edit_coupons')
]
