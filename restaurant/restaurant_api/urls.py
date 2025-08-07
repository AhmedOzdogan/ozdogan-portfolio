from django.urls import path
from .views import MenuListAPIView, MenuItemAPIView

app_name = 'restaurant_api'

urlpatterns = [
    path('menu/', MenuListAPIView.as_view(), name='menu-list'),
    path('menu/<slug:slug>/', MenuItemAPIView.as_view(), name='menu-item-detail'),
]
