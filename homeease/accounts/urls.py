from django.urls import path
from .  import views

urlpatterns = [
    path('', views.Home, name='home'),
    path('register/', views.RegisterPage, name='register'),
    path('login/', views.LoginPage, name='login'),
    # path('logout/', views.LogoutPage, name='logout'),
    
]