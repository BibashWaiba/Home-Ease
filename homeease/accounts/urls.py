from django.urls import path
from .  import views

urlpatterns = [
    path('register/', views.RegisterPage, name='register'),
    path('login/', views.LoginPage, name='login'),
    # path('logout/', views.LogoutPage, name='logout'),
    
]