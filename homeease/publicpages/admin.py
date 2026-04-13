from django.contrib import admin
from .models import Contact, Category, Service, Package
# Register your models here.
admin.site.register(Contact)
admin.site.register(Category)
admin.site.register(Service)

@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ('name', 'combo_price')
    filter_horizontal = ('services',)