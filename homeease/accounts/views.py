from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from . models import CustomUser, PasswordResetOTP
import random
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

def RegisterPage(request):
    """
    View for user registration with manual form handling
    """
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone_numberr = request.POST.get('phone_numberr')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        errors = []
        if password1 != password2:
            errors.append("Passwords do not match!")
        if CustomUser.objects.filter(username=username).exists():
            errors.append("Username already exists!")
        if CustomUser.objects.filter(email=email).exists():
            errors.append("Email already exists!")
        
        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, "account/register.html")
        
        try:
            user = CustomUser.objects.create_user(
                username=username,
                email=email,
                password=password1,
                first_name=first_name,
                last_name=last_name,
                phone_numberr=phone_numberr,
                address=address,
                gender=gender
            )
            messages.success(request, f'Account created successfully! Welcome {username}!')
            login(request, user)
            return redirect('home')
        except Exception as e:
            messages.error(request, f'Error creating account: {str(e)}')
            return render(request, "account/register.html")
    
    return render(request, "account/register.html")

def LoginPage(request):
    """
    View for user login with role-based dashboard redirect
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.get_full_name()}!')
            if user.is_staff or user.is_superuser:
                return redirect('admin_dashboard')
            else:
                return redirect('user_dashboard')
        else:
            messages.error(request, 'Invalid username or password!')
    return render(request, 'account/login.html')

def LogoutPage(request):
    """
    View for user logout
    """
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('home')

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = CustomUser.objects.filter(email=email).first()
        
        if user:
            otp = str(random.randint(100000, 999999))
            PasswordResetOTP.objects.create(user=user, otp=otp)
            
            # Send Email
            subject = "Home-Ease Password Reset OTP"
            message = f"Your OTP for password reset is: {otp}. It is valid for 10 minutes."
            from_email = settings.DEFAULT_FROM_EMAIL
            
            try:
                send_mail(subject, message, from_email, [email])
                messages.success(request, "OTP has been sent to your email.")
                request.session['reset_email'] = email
                return redirect('verify_otp')
            except Exception as e:
                messages.error(request, f"Error sending email: {str(e)}. Use 123456 as test OTP.")
                # Fallback for dev/broken SMTP
                request.session['reset_email'] = email
                return redirect('verify_otp')
        else:
            messages.error(request, "User with this email does not exist.")
            
    return render(request, 'account/forgot_password.html')

def verify_otp(request):
    email = request.session.get('reset_email')
    if not email:
        return redirect('forgot_password')
        
    if request.method == 'POST':
        otp_entered = request.POST.get('otp')
        user = CustomUser.objects.filter(email=email).first()
        
        # Check for valid OTP (not used, within 10 mins)
        otp_obj = PasswordResetOTP.objects.filter(
            user=user, 
            otp=otp_entered, 
            is_used=False,
            created_at__gt=timezone.now() - timedelta(minutes=10)
        ).first()
        
        # Development fallback
        if not otp_obj and otp_entered == '123456':
             otp_obj = PasswordResetOTP.objects.filter(user=user, is_used=False).last()

        if otp_obj:
            otp_obj.is_used = True
            otp_obj.save()
            request.session['otp_verified'] = True
            return redirect('reset_password')
        else:
            messages.error(request, "Invalid or expired OTP.")
            
    return render(request, 'account/verify_otp.html')

def reset_password(request):
    if not request.session.get('otp_verified'):
        return redirect('forgot_password')
        
    email = request.session.get('reset_email')
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        if new_password == confirm_password:
            user = CustomUser.objects.filter(email=email).first()
            user.set_password(new_password)
            user.save()
            
            # Clear session
            del request.session['reset_email']
            del request.session['otp_verified']
            
            messages.success(request, "Password reset successfully. Please login.")
            return redirect('login')
        else:
            messages.error(request, "Passwords do not match.")
            
    return render(request, 'account/reset_password.html')
