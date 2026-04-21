from django import forms
from datetime import date
from accounts.models import CustomUser
from publicpages.models import Service, Category, Package
from user_dashboard.models import Booking

class UserAccountForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), required=False, help_text="Leave blank to keep current password.")
    confirm_password = forms.CharField(widget=forms.PasswordInput(), required=False, help_text="Confirm your new password.")

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'phone_numberr', 'address', 'gender', 'is_staff', 'is_active']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Enter username'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'Enter first name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Enter last name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter email address'}),
            'phone_numberr': forms.TextInput(attrs={'placeholder': 'Enter phone number'}),
            'address': forms.TextInput(attrs={'placeholder': 'Enter address'}),
            'gender': forms.Select(),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password or confirm_password:
            if password != confirm_password:
                raise forms.ValidationError("Passwords do not match!")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password")
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'price', 'category', 'image', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter service name'}),
            'price': forms.NumberInput(attrs={'placeholder': 'Enter price'}),
            'category': forms.Select(),
            'description': forms.Textarea(attrs={'placeholder': 'Enter service description', 'rows': 4}),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter category name'}),
            'description': forms.Textarea(attrs={'placeholder': 'Enter category description', 'rows': 3}),
        }

class PackageForm(forms.ModelForm):
    class Meta:
        model = Package
        fields = ['name', 'description', 'services', 'combo_price', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter package name'}),
            'description': forms.Textarea(attrs={'placeholder': 'Enter package description', 'rows': 4}),
            'services': forms.CheckboxSelectMultiple(),  # Multiple selection
            'combo_price': forms.NumberInput(attrs={'placeholder': 'Enter discounted combo price'}),
        }

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['user', 'service', 'package', 'date', 'time', 'status']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date'].widget.attrs['min'] = date.today().isoformat()
        
    def clean_date(self):
        booking_date = self.cleaned_data.get('date')
        if booking_date and booking_date < date.today():
            raise forms.ValidationError("You cannot select a past date.")
        return booking_date
    
    def clean(self):
        cleaned_data = super().clean()
        service = cleaned_data.get('service')
        package = cleaned_data.get('package')
        
        if service and package:
            raise forms.ValidationError("A booking cannot have both a service and a package.")
        
        if not service and not package:
            raise forms.ValidationError("You must select either a service or a package.")
            
        return cleaned_data
