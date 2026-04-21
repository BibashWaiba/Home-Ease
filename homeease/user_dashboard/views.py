from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from .models import Booking
from accounts.models import CustomUser
from publicpages.models import Service, Review

@login_required
def user_dashboard(request):
    Booking.auto_cancel_expired()
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    
    pending_bookings = bookings.filter(status='Pending')
    confirmed_bookings = bookings.filter(status='Confirmed')
    completed_bookings = bookings.filter(status='Completed')
    cancelled_bookings = bookings.filter(status='Cancelled')
    
    context = {
        'pending_bookings': pending_bookings,
        'confirmed_bookings': confirmed_bookings,
        'completed_bookings': completed_bookings,
        'cancelled_bookings': cancelled_bookings,
        'bookings': bookings,
    }
    return render(request, 'UserDashboard/dashboard.html', context)

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    if booking.status == 'Pending':
        booking.status = 'Cancelled'
        booking.save()
        messages.success(request, "Booking has been cancelled successfully.")
    else:
        messages.error(request, "Only pending bookings can be cancelled.")
        
    return redirect('user_dashboard')

@login_required
def complete_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    if booking.status == 'Confirmed':
        booking.status = 'Completed'
        booking.save()
        messages.success(request, "Job marked as completed! Hope you enjoyed the service.")
    else:
        messages.error(request, "Only confirmed bookings can be marked as completed.")
        
    return redirect('user_dashboard')

@login_required
def user_profile(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone_numberr')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        
        user = request.user
        user.first_name = first_name
        user.last_name = last_name
        user.phone_numberr = phone
        user.address = address
        user.gender = gender
        user.save()
        
        messages.success(request, "Profile updated successfully!")
        return redirect('profile')
        
    return render(request, 'UserDashboard/profile.html')

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Keeps the user logged in
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'UserDashboard/change_password.html', {'form': form})

@login_required
def leave_review(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    # Review is only for services currently as per model structure
    if not booking.service:
        messages.error(request, "Reviews are currently only available for individual services.")
        return redirect('user_dashboard')
        
    if booking.status != 'Completed':
        messages.error(request, "You can only review services that have been marked as completed.")
        return redirect('user_dashboard')

    existing_review = Review.objects.filter(user=request.user, service=booking.service).first()

    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        
        if rating and comment:
            if existing_review:
                existing_review.rating = rating
                existing_review.comment = comment
                existing_review.save()
                messages.success(request, "Your review has been updated!")
            else:
                Review.objects.create(
                    user=request.user,
                    service=booking.service,
                    rating=rating,
                    comment=comment
                )
                messages.success(request, "Thank you for your review!")
            return redirect('user_dashboard')
        else:
            messages.error(request, "Please provide both a rating and a comment.")

    context = {
        'booking': booking,
        'existing_review': existing_review
    }
    return render(request, 'UserDashboard/leave_review.html', context)