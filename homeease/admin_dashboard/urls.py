from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard'),
    
    # Users
    path('users/', views.admin_users_list, name='admin_users_list'),
    path('users/create/', views.admin_users_create, name='admin_users_create'),
    path('users/update/<int:pk>/', views.admin_users_update, name='admin_users_update'),
    path('users/delete/<int:pk>/', views.admin_users_delete, name='admin_users_delete'),
    
    # Services
    path('services/', views.admin_services_list, name='admin_services_list'),
    path('services/create/', views.admin_services_create, name='admin_services_create'),
    path('services/update/<int:pk>/', views.admin_services_update, name='admin_services_update'),
    path('services/delete/<int:pk>/', views.admin_services_delete, name='admin_services_delete'),
    
    # Categories
    path('categories/', views.admin_categories_list, name='admin_categories_list'),
    path('categories/create/', views.admin_categories_create, name='admin_categories_create'),
    path('categories/update/<int:pk>/', views.admin_categories_update, name='admin_categories_update'),
    path('categories/delete/<int:pk>/', views.admin_categories_delete, name='admin_categories_delete'),
    
    # Packages
    path('packages/', views.admin_packages_list, name='admin_packages_list'),
    path('packages/create/', views.admin_packages_create, name='admin_packages_create'),
    path('packages/update/<int:pk>/', views.admin_packages_update, name='admin_packages_update'),
    path('packages/delete/<int:pk>/', views.admin_packages_delete, name='admin_packages_delete'),
    
    # Bookings
    path('bookings/', views.admin_bookings_list, name='admin_bookings_list'),
    path('bookings/create/', views.admin_bookings_create, name='admin_bookings_create'),
    path('bookings/update/<int:pk>/', views.admin_bookings_update, name='admin_bookings_update'),
    path('bookings/delete/<int:pk>/', views.admin_bookings_delete, name='admin_bookings_delete'),
    
    # Contact Messages
    path('contact-messages/', views.admin_contact_messages_list, name='admin_contact_messages_list'),
    path('contact-messages/delete/<int:pk>/', views.admin_contact_messages_delete, name='admin_contact_messages_delete'),
]