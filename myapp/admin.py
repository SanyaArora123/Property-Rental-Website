from django.contrib import admin
from .models import Property, Seller

# Register your models here.
admin.site.register(Property)
admin.site.register(Seller)
admin.site.site_title = "Prime Rentals Admin"
admin.site.site_header = "Prime Rentals Admin"
admin.site.index_title = "Welcome to Prime Rentals Admin"