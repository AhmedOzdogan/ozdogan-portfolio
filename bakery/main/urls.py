from django.urls import path, include
from .views import index, menu, menu_item, login, signup, logout, cart_snapshot, profile, add_address, edit_address, delete_address, address_list

app_name = 'main'

urlpatterns = [
    path('', index, name='index'),
    path('menu/', menu, name='menu'),
    path('menu/<int:item_id>/', menu_item, name='menu_item'),
    path('login/', login, name='login'),
    path('signup/', signup, name='signup'),
    path('logout/', logout, name='logout'),
    path('profile/', profile, name='profile'),
    path('cart/snapshot/', cart_snapshot, name='cart_snapshot'),
    path("addresses/", address_list, name="address_list"),
    path("addresses/add/", add_address, name="add_address"),
    path("addresses/edit/<int:address_id>/", edit_address, name="edit_address"),
    path("addresses/delete/<int:address_id>/", delete_address, name="delete_address"),
    
]
