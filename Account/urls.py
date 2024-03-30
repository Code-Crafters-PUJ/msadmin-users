from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import RegisterAccountView, LoginAccountView, getAccountInfoview


app_name = 'Account'
urlpatterns = [
    path('register', RegisterAccountView.as_view(),
         name='user_create'),
    path('login', LoginAccountView.as_view(),
         name='pqr_get'),
    path('<int:pk>', getAccountInfoview.as_view(), name='pqr_get'),


]


