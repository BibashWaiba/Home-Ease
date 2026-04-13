from django.urls import path
from .views  import *

urlpatterns = [
    path('', Home, name='home'),
    path('services/', ServicesList, name='services'),
    path('services/category/<int:category_id>/', CategoryServices, name='category_services'),
    path('services/detail/<int:service_id>/', ServiceDetail, name='service_detail'),
    path('services/<int:service_id>/review/', SubmitReview, name='submit_review'),
    path('services/book/<int:service_id>/', BookService, name='book_service'),
    path('packages/', PackagesList, name='packages'),
    path('packages/<int:package_id>/', PackageDetail, name='package_detail'),
    path('packages/book/<int:package_id>/', BookPackage, name='book_package'),
    path('services/payment/esewa/<int:booking_id>/', EsewaRequestView, name='payment'),
    path('services/payment/esewa/verify/<int:booking_id>/', EsewaVerifyView, name='esewa_verify'),
    path('about/', About, name='about'),
    path('contact-us/', ContactUs, name='contact_us'),
]