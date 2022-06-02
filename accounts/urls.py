from django.urls import path
from . import views

from rest_framework_simplejwt import views as jwt_views


app_name = 'accounts'
urlpatterns = [
    path('login/', views.login, name='login'),
    path('user-accounts/', views.user_accounts, name='user_accounts'),
    path('user-accounts/<uuid:user_id>/', views.edit_user_accounts, name='edit_user_accounts'),
    path('admin-accounts/', views.admin_accounts, name='admin_accounts'),
    path('admin-accounts/<uuid:user_id>/', views.edit_admin_accounts, name='edit_admin_accounts'),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]
