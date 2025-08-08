from django.contrib import admin
from .models import Category,Menu, Messages, Reservations

admin.site.register(Category)
admin.site.register(Menu)
admin.site.register(Messages)
admin.site.register(Reservations)
