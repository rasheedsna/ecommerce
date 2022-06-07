from django.urls import path
from . import views

from rest_framework_simplejwt import views as jwt_views


app_name = 'accounts'
urlpatterns = [
    path('user-accounts/', views.UserAccounts.as_view(), name='user_accounts'),
    path('user-accounts/<uuid:user_id>/', views.EditUserAccounts.as_view(), name='edit_user_accounts'),
    path('admin-accounts/', views.AdminAccounts.as_view(), name='admin_accounts'),
    path('admin-accounts/<uuid:user_id>/', views.EditAdminUserAccounts.as_view(), name='edit_admin_accounts'),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]
