from django.urls import path, include
from .views import index, menu, menu_item, reservations, about, contact
app_name = 'main'

urlpatterns = [
    path('', index, name='index'),
    path('menu/', menu, name='menu'),
    path('menu/<str:slug>/', menu_item, name='menu_item'),
    path('reservations/', reservations, name='reservations'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
]
