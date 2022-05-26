from django.urls import path
from . import views


app_name = 'accounts'
urlpatterns = [
    path('user-accounts/', views.user_accounts, name='user_accounts'),
]
