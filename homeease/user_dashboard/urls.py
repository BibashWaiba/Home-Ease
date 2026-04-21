from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_dashboard, name='user_dashboard'),
    path('profile/', views.user_profile, name='profile'),
    path('change-password/', views.change_password, name='change_password'),
    path('cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('complete/<int:booking_id>/', views.complete_booking, name='complete_booking'),
    path('review/<int:booking_id>/', views.leave_review, name='leave_review'),
]