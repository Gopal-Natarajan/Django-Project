from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path,include
from . import views

urlpatterns = [
    path('login/', obtain_auth_token, name="login"),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_user, name='logout'),
]

 