from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Contact, Category, Service, Package
from django.db.models import Q
from django.core.paginator import Paginator
import uuid
import hmac
import hashlib
import base64
import json
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Review
from user_dashboard.models import Booking

# Create your views here.
def Home(request):
    return render(request, "PublicPages/index.html")

def ServicesList(request):
    query = request.GET.get('q', '')
    category_id = request.GET.get('category', '')
    page_number = request.GET.get('page', 1)
    categories = Category.objects.all()

    if query:
        # Search — return all matches, no pagination
        services = Service.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
        return render(request, "PublicPages/services.html", {
            'services': services,
            'query': query,
            'is_search': True,
            'categories': categories,
            'selected_category': category_id,
        })
    elif category_id:
        # Category filter — return all matches, no pagination
        services = Service.objects.filter(category__id=category_id)
        return render(request, "PublicPages/services.html", {
            'services': services,
            'categories': categories,
            'selected_category': category_id,
            'is_search': False,
            'is_filtered': True,
        })
    else:
        # All services — paginated, 12 per page
        services_qs = Service.objects.all()
        paginator = Paginator(services_qs, 12)
        page_obj = paginator.get_page(page_number)
        return render(request, "PublicPages/services.html", {
            'page_obj': page_obj,
            'categories': categories,
            'selected_category': '',
            'is_search': False,
            'is_filtered': False,
        })

def CategoryServices(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    services = Service.objects.filter(category=category)
    return render(request, "PublicPages/category_services.html", {'category': category, 'services': services})

def PackagesList(request):
    packages = Package.objects.all()
    return render(request, "PublicPages/packages.html", {'packages': packages})

def PackageDetail(request, package_id):
    package = get_object_or_404(Package, id=package_id)
    has_active_booking = False
    
    if request.user.is_authenticated:
        from user_dashboard.models import Booking
        has_active_booking = Booking.objects.filter(user=request.user, package=package, status__in=['Pending', 'Confirmed']).exists()
        
    return render(request, "PublicPages/package_detail.html", {
        'package': package,
        'has_active_booking': has_active_booking
    })

def ServiceDetail(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    reviews = service.reviews.all().order_by('-created_at')
    
    avg_rating = 0
    if reviews.exists():
        avg_rating = sum(r.rating for r in reviews) / reviews.count()
        avg_rating = round(avg_rating, 1)

    has_booked = False
    has_active_booking = False
    if request.user.is_authenticated:
        from user_dashboard.models import Booking
        has_booked = Booking.objects.filter(user=request.user, service=service).exists()
        has_active_booking = Booking.objects.filter(user=request.user, service=service, status__in=['Pending', 'Confirmed']).exists()

    return render(request, "PublicPages/service_details.html", {
        'service': service,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'has_booked': has_booked,
        'has_active_booking': has_active_booking
    })



@login_required
def SubmitReview(request, service_id):
    if request.method == 'POST':
        service = get_object_or_404(Service, id=service_id)
        
        from user_dashboard.models import Booking
        if not Booking.objects.filter(user=request.user, service=service).exists():
            messages.error(request, "You can only review services that you have booked.")
            return redirect('service_detail', service_id=service_id)
            
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        
        if rating and comment:
            existing_review = Review.objects.filter(user=request.user, service=service).first()
            if existing_review:
                existing_review.rating = rating
                existing_review.comment = comment
                existing_review.save()
                messages.success(request, "Your review has been updated.")
            else:
                Review.objects.create(
                    user=request.user,
                    service=service,
                    rating=rating,
                    comment=comment
                )
                messages.success(request, "Thank you for your review!")
        else:
            messages.error(request, "Please provide both a rating and a comment.")
            
    next_url = request.POST.get('next') or request.GET.get('next')
    if next_url:
        return redirect(next_url)
    return redirect('service_detail', service_id=service_id)



@login_required
def BookService(request, service_id):
    if request.user.is_staff or request.user.is_superuser:
        messages.error(request, "Admin accounts cannot book services.")
        return redirect('service_detail', service_id=service_id)
        
    service = get_object_or_404(Service, id=service_id)
    if Booking.objects.filter(user=request.user, service=service, status__in=['Pending', 'Confirmed']).exists():
        messages.error(request, "You already have an active booking for this service.")
        return redirect('service_detail', service_id=service_id)
        
    if request.method == "POST":
        date = request.POST.get('date')
        time = request.POST.get('time')
        
        booking = Booking.objects.create(
            user=request.user,
            service=service,
            date=date,
            time=time,
            status='Pending'
        )
        messages.success(request, f"Successfully booked {service.name}! Please complete your payment below.")
        return redirect('user_dashboard')
    return redirect('service_detail', service_id=service_id)

@login_required
def BookPackage(request, package_id):
    if request.user.is_staff or request.user.is_superuser:
        messages.error(request, "Admin accounts cannot book service packages.")
        return redirect('package_detail', package_id=package_id)
        
    package = get_object_or_404(Package, id=package_id)
    if Booking.objects.filter(user=request.user, package=package, status__in=['Pending', 'Confirmed']).exists():
        messages.error(request, "You already have an active booking for this package.")
        return redirect('package_detail', package_id=package_id)
        
    if request.method == "POST":
        date = request.POST.get('date')
        time = request.POST.get('time')
        
        booking = Booking.objects.create(
            user=request.user,
            package=package,
            date=date,
            time=time,
            status='Pending'
        )
        messages.success(request, f"Successfully booked {package.name}! Please complete your payment below.")
        return redirect('user_dashboard')
    return redirect('package_detail', package_id=package_id)



@login_required
def EsewaRequestView(request, booking_id):
    Booking.auto_cancel_expired()
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    if booking.status != 'Pending':
        messages.error(request, "This booking has expired or is no longer pending, and cannot be paid for.")
        return redirect('user_dashboard')
    
    if booking.service:
        amount = str(booking.service.price)
    else:
        amount = str(booking.package.combo_price)
        
    tax_amount = "0"
    total_amount = amount
    transaction_uuid = f"{booking.id}-{uuid.uuid4().hex[:8]}"
    product_code = "EPAYTEST"
    secret_key = "8gBm/:&EnhH.1/q"
    signed_field_names = "total_amount,transaction_uuid,product_code"
    
    # Format message for HMAC: total_amount,transaction_uuid,product_code
    message = f"total_amount={total_amount},transaction_uuid={transaction_uuid},product_code={product_code}"
    
    # Generate HMAC SHA256 signature (correct Python hmac usage)
    hash_value = hmac.new(
        key=secret_key.encode('utf-8'),
        msg=message.encode('utf-8'),
        digestmod=hashlib.sha256
    ).digest()
    
    signature = base64.b64encode(hash_value).decode('utf-8')
    domain = request.build_absolute_uri('/').rstrip('/')
    
    context = {
        'booking': booking,
        'amount': amount,
        'tax_amount': tax_amount,
        'total_amount': total_amount,
        'transaction_uuid': transaction_uuid,
        'product_code': product_code,
        'signed_field_names': signed_field_names,
        'signature': signature,
        'success_url': f"{domain}{reverse('esewa_verify', args=[booking.id])}",
        'failure_url': f"{domain}{reverse('user_dashboard')}",
    }
    
    return render(request, "PublicPages/esewa_request.html", context)

@login_required
def EsewaVerifyView(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    data = request.GET.get('data')
    
    if data:
        try:
            decoded_data = base64.b64decode(data).decode('utf-8')
            json_data = json.loads(decoded_data)
            
            # --- Verify eSewa's response signature ---
            secret_key = "8gBm/:&EnhH.1/q"
            signed_field_names = json_data.get('signed_field_names', '')
            fields = [f.strip() for f in signed_field_names.split(',')]
            message = ','.join([f"{field}={json_data.get(field, '')}" for field in fields])
            
            expected_hash = hmac.new(
                key=secret_key.encode('utf-8'),
                msg=message.encode('utf-8'),
                digestmod=hashlib.sha256
            ).digest()
            expected_signature = base64.b64encode(expected_hash).decode('utf-8')
            received_signature = json_data.get('signature', '')
            
            # Use constant-time comparison to prevent timing attacks
            if not hmac.compare_digest(expected_signature, received_signature):
                messages.error(request, "Payment verification failed: invalid signature.")
                return redirect('user_dashboard')
            
            
            if json_data.get('status') == 'COMPLETE':
                from user_dashboard.models import Payment
                booking.status = 'Confirmed'
                booking.save()
                
                # Record the transaction
                Payment.objects.create(
                    booking=booking,
                    transaction_id=json_data.get('transaction_code'),
                    amount=json_data.get('total_amount'),
                    status='COMPLETE',
                    payment_method='eSewa'
                )
                
                item_name = booking.service.name if booking.service else booking.package.name
                messages.success(request, f"Payment via eSewa successful! Your booking for {item_name} is confirmed.")
            else:
                messages.error(request, "Payment could not be confirmed by eSewa.")
        except Exception as e:
            messages.error(request, f"Error processing eSewa payment response: {str(e)}")
    else:
        messages.error(request, "Invalid payment response from eSewa.")
        
    return redirect('user_dashboard')

def About(request):
    return render(request, "PublicPages/about.html")

def ContactUs(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Save the contact message to the database
        Contact.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )
        messages.success(request, "Your message has been sent successfully. We will get back to you soon!")
        return redirect('contact_us')

    return render(request, "PublicPages/contact_us.html")