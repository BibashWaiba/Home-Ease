from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.db.models import Q
from accounts.models import CustomUser
from publicpages.models import Service, Category, Package, Contact
from user_dashboard.models import Booking, Payment
from .forms import ServiceForm, CategoryForm, PackageForm, BookingForm, UserAccountForm

def admin_required(view_func):
    return user_passes_test(lambda u: u.is_staff or u.is_superuser)(view_func)

@admin_required
def admin_dashboard(request):
    """
    Overview of system stats.
    """
    context = {
        'total_users': CustomUser.objects.count(),
        'total_services': Service.objects.count(),
        'total_bookings': Booking.objects.count(),
        'total_packages': Package.objects.count(),
        'recent_bookings': Booking.objects.all().order_by('-created_at')[:5]
    }
    return render(request, 'AdminDashboard/dashboard.html', context)

# Users CRUD
@admin_required
def admin_users_list(request):
    items = CustomUser.objects.all().order_by('-id')
    return render(request, 'AdminDashboard/users/list.html', {'items': items})

@admin_required
def admin_users_create(request):
    if request.method == 'POST':
        form = UserAccountForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "User created successfully.")
            return redirect('admin_users_list')
    else:
        form = UserAccountForm()
    return render(request, 'AdminDashboard/users/form.html', {'form': form})

@admin_required
def admin_users_update(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    if request.method == 'POST':
        form = UserAccountForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "User updated successfully.")
            return redirect('admin_users_list')
    else:
        form = UserAccountForm(instance=user)
    return render(request, 'AdminDashboard/users/form.html', {'form': form})

@admin_required
def admin_users_delete(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    if request.method == 'POST':
        user.delete()
        messages.success(request, "User deleted successfully.")
        return redirect('admin_users_list')
    return render(request, 'AdminDashboard/users/confirm_delete.html', {'item': user})

# Services CRUD
@admin_required
def admin_services_list(request):
    items = Service.objects.all().order_by('-id')
    return render(request, 'AdminDashboard/services/list.html', {'items': items})

@admin_required
def admin_services_create(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Service created successfully.")
            return redirect('admin_services_list')
    else:
        form = ServiceForm()
    return render(request, 'AdminDashboard/services/form.html', {'form': form})

@admin_required
def admin_services_update(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES, instance=service)
        if form.is_valid():
            form.save()
            messages.success(request, "Service updated successfully.")
            return redirect('admin_services_list')
    else:
        form = ServiceForm(instance=service)
    return render(request, 'AdminDashboard/services/form.html', {'form': form})

@admin_required
def admin_services_delete(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        service.delete()
        messages.success(request, "Service deleted successfully.")
        return redirect('admin_services_list')
    return render(request, 'AdminDashboard/services/confirm_delete.html', {'item': service})

# Categories CRUD
@admin_required
def admin_categories_list(request):
    items = Category.objects.all().order_by('-id')
    return render(request, 'AdminDashboard/categories/list.html', {'items': items})

@admin_required
def admin_categories_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Category created successfully.")
            return redirect('admin_categories_list')
    else:
        form = CategoryForm()
    return render(request, 'AdminDashboard/categories/form.html', {'form': form})

@admin_required
def admin_categories_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "Category updated successfully.")
            return redirect('admin_categories_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'AdminDashboard/categories/form.html', {'form': form})

@admin_required
def admin_categories_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        messages.success(request, "Category deleted successfully.")
        return redirect('admin_categories_list')
    return render(request, 'AdminDashboard/categories/confirm_delete.html', {'item': category})

# Packages CRUD
@admin_required
def admin_packages_list(request):
    items = Package.objects.all().order_by('-id')
    return render(request, 'AdminDashboard/packages/list.html', {'items': items})

@admin_required
def admin_packages_create(request):
    if request.method == 'POST':
        form = PackageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Package created successfully.")
            return redirect('admin_packages_list')
    else:
        form = PackageForm()
    return render(request, 'AdminDashboard/packages/form.html', {'form': form})

@admin_required
def admin_packages_update(request, pk):
    package = get_object_or_404(Package, pk=pk)
    if request.method == 'POST':
        form = PackageForm(request.POST, request.FILES, instance=package)
        if form.is_valid():
            form.save()
            messages.success(request, "Package updated successfully.")
            return redirect('admin_packages_list')
    else:
        form = PackageForm(instance=package)
    return render(request, 'AdminDashboard/packages/form.html', {'form': form})

@admin_required
def admin_packages_delete(request, pk):
    package = get_object_or_404(Package, pk=pk)
    if request.method == 'POST':
        package.delete()
        messages.success(request, "Package deleted successfully.")
        return redirect('admin_packages_list')
    return render(request, 'AdminDashboard/packages/confirm_delete.html', {'item': package})

# Bookings CRUD
@admin_required
def admin_bookings_list(request):
    query = request.GET.get('q')
    items = Booking.objects.all().order_by('-id')
    if query:
        items = items.filter(
            Q(user__username__icontains=query) |
            Q(service__name__icontains=query) |
            Q(package__name__icontains=query)
        )
    return render(request, 'AdminDashboard/bookings/list.html', {'items': items, 'query': query})

@admin_required
def admin_bookings_create(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Booking created successfully.")
            return redirect('admin_bookings_list')
    else:
        form = BookingForm()
    return render(request, 'AdminDashboard/bookings/form.html', {'form': form})

@admin_required
def admin_bookings_update(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            messages.success(request, "Booking updated successfully.")
            return redirect('admin_bookings_list')
    else:
        form = BookingForm(instance=booking)
    return render(request, 'AdminDashboard/bookings/form.html', {'form': form})

@admin_required
def admin_bookings_delete(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    if request.method == 'POST':
        booking.delete()
        messages.success(request, "Booking deleted successfully.")
        return redirect('admin_bookings_list')
    return render(request, 'AdminDashboard/bookings/confirm_delete.html', {'item': booking})

# Contact Messages
@admin_required
def admin_contact_messages_list(request):
    items = Contact.objects.all().order_by('-id')
    return render(request, 'AdminDashboard/contact_messages/list.html', {'items': items})

@admin_required
def admin_contact_messages_delete(request, pk):
    message = get_object_or_404(Contact, pk=pk)
    if request.method == 'POST':
        message.delete()
        messages.success(request, "Contact message deleted successfully.")
        return redirect('admin_contact_messages_list')
    return render(request, 'AdminDashboard/contact_messages/confirm_delete.html', {'item': message})

# Payment History
@admin_required
def admin_payment_history(request):
    """
    View all financial transactions with customer and transaction details.
    """
    query = request.GET.get('q')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    items = Payment.objects.all().order_by('-created_at')
    
    if query:
        items = items.filter(
            Q(booking__user__username__icontains=query) |
            Q(booking__service__name__icontains=query) |
            Q(booking__package__name__icontains=query) |
            Q(status__icontains=query)
        )
    
    if start_date:
        items = items.filter(created_at__date__gte=start_date)
    if end_date:
        items = items.filter(created_at__date__lte=end_date)
    
    context = {
        'items': items,
        'query': query,
        'start_date': start_date,
        'end_date': end_date,
    }
    return render(request, 'AdminDashboard/payments/list.html', context)