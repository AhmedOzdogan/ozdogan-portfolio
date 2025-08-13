from django.urls import path, include
from .views import index, menu, menu_item

app_name = 'main'

urlpatterns = [
    path('', index, name='index'),
    path('menu/', menu, name='menu'),
    path('menu/<int:item_id>/', menu_item, name='menu_item'),
]
