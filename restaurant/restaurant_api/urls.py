from django.urls import path
from .views import MenuListAPIView, MenuItemAPIView, ReservationAPIView, ReservationCheckAPIView

app_name = 'restaurant_api'

urlpatterns = [
    path('menu/', MenuListAPIView.as_view(), name='menu-list'),
    path('menu/<slug:slug>/', MenuItemAPIView.as_view(), name='menu-item-detail'),
    path('reservations/', ReservationAPIView.as_view(), name='reservation-list'),
    path('reservations/check/', ReservationCheckAPIView.as_view(), name='reservation-check'),
]
