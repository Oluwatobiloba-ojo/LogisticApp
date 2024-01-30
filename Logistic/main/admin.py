from django.contrib import admin
from .models import Customer, Administrator, Rider
# Register your models here.

admin.site.register(Customer)
admin.site.register(Administrator)
admin.site.register(Rider)
