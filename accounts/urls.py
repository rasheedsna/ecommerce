from django.urls import path
from . import views


app_name = 'accounts'
urlpatterns = [
    path('user-accounts/', views.user_accounts, name='user_accounts'),
    path('user-accounts/<uuid:user_id>/', views.edit_user_accounts, name='edit_user_accounts'),
    path('admin-accounts/', views.admin_accounts, name='admin_accounts'),
    path('admin-accounts/<uuid:user_id>/', views.edit_admin_accounts, name='edit_admin_accounts'),
]
