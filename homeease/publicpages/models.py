from django.db import models
from django.conf import settings

# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.TextField()

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='category_images/')
    def __str__(self):
        return self.name


class Service(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='service_images/')
    description = models.TextField()
    def __str__(self):
        return self.name

class Package(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    services = models.ManyToManyField(Service, related_name='packages')
    combo_price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='package_images/')
    
    def __str__(self):
        return self.name

class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.service.name} ({self.rating}/5)"