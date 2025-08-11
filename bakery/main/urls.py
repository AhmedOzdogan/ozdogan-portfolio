from django.urls import path, include
from .views import index, menu

app_name = 'main'

urlpatterns = [
    path('', index, name='index'),
    path('menu/', menu, name='menu'),
]
