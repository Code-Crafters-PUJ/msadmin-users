from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import RegisterAccountView, LoginAccountView, getAccountInfoview

app_name = 'user'

urlpatterns = [
    path('register', RegisterAccountView.as_view(), name='user_register'),
    path('login', LoginAccountView.as_view(), name='user_login'),
    path('<int:pk>', getAccountInfoview.as_view(), name='account_info'),
]

