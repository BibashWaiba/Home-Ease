from django.db import models
from django.conf import settings
from publicpages.models import Service, Package
from datetime import timedelta
from django.utils import timezone

class Booking(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True, blank=True)
    package = models.ForeignKey(Package, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        item = self.service.name if self.service else self.package.name
        return f"{self.user.username} - {item} ({self.status})"

    @staticmethod
    def auto_cancel_expired():
        """
        Cancels pending bookings that have either:
        1. Exceeded the 2-hour payment window after creation.
        2. Reached their scheduled booking date and time (using local time).
        """
        from django.db.models import Q
        now = timezone.now()
        local_now = timezone.localtime(now)
        current_date = local_now.date()
        current_time = local_now.time()
        
        # 2-hour window for payment
        expiry_limit = now - timedelta(hours=2)
        
        # Find bookings where:
        # (Created > 2h ago) OR (Date is in the past) OR (Date is Today and Time is in the past)
        Booking.objects.filter(
            status='Pending'
        ).filter(
            Q(created_at__lt=expiry_limit) |
            Q(date__lt=current_date) |
            Q(date=current_date, time__lt=current_time)
        ).update(status='Cancelled')

class Payment(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='payments')
    transaction_id = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20)
    payment_method = models.CharField(max_length=20, default='eSewa')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.transaction_id} - Rs. {self.amount}"
