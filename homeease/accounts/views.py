from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from . models import CustomUser


def RegisterPage(request):
    """
    View for user registration with manual form handling
    """
    if request. method == 'POST':
        # Get data from POST request
        first_name = request.POST. get('first_name')
        last_name = request.POST. get('last_name')
        username = request.POST.get('username')
        email = request. POST.get('email')
        phone_numberr = request.POST.get('phone_numberr')
        address = request.POST. get('address')
        gender = request.POST.get('gender')
        password1 = request. POST.get('password1')
        password2 = request.POST.get('password2')
        
        # Validation
        errors = []
        
        # Check if passwords match
        if password1 != password2:
            errors.append("Passwords do not match!")
        
        # Check if username already exists
        if CustomUser.objects.filter(username=username).exists():
            errors.append("Username already exists!")
        
        # Check if email already exists
        if CustomUser.objects.filter(email=email).exists():
            errors.append("Email already exists!")
        
        # Check if phone number is valid
        try: 
            phone_numberr = int(phone_numberr)
        except (ValueError, TypeError):
            errors. append("Phone number must be a valid number!")
        
        # If there are errors, show them
        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, "account/register.html", {
                'form': {
                    'first_name':  {'value': first_name},
                    'last_name': {'value': last_name},
                    'username': {'value': username},
                    'email': {'value': email},
                    'phone_numberr': {'value':  phone_numberr},
                    'address': {'value': address},
                    'gender': {'value': gender},
                }
            })
        
        # Create user
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
            
            messages. success(request, f'Account created successfully!  Welcome {username}!')
            # Auto login after registration
            login(request, user)
            return redirect('home')
            
        except Exception as e: 
            messages.error(request, f'Error creating account: {str(e)}')
            return render(request, "account/register. html")
    
    return render(request, "account/register.html")


def LoginPage(request):
    """
    View for user login with role-based dashboard redirect
    """
    # # Redirect if already logged in
    # if request.user.is_authenticated:
    #     if request.user.is_staff or request.user.is_superuser:
    #         return redirect('admin_dashboard')  # URL name
    #     return redirect('user_dashboard')  # URL name
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Authenticate user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.get_full_name()}!')
            
            # Role-based redirect using URL names
            if user.is_staff or user.is_superuser:
                return redirect('admin_dashboard')  # URL name
            else:
                return redirect('user_dashboard')  # URL name
        else:
            messages.error(request, 'Invalid username or password!')
    
    return render(request, 'account/login.html')



def Home(request):
    """
    Home page view
    """
    return render(request, "index.html")