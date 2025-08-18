from django.contrib import admin

from .models import Order, OrderItem, Cart, CartItem


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "created_at")
    list_filter = ("created_at", "user")
    search_fields = ("user__username", "id")

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("id", "cart", "product", "quantity", "unit_price")
    list_filter = ("cart__created_at", "product")
    search_fields = ("cart__user__username", "product_name")

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "shipping_address", "total", "created_at")
    list_filter = ("created_at", "user")
    search_fields = ("user__username", "id")    

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "product_name", "quantity", "line_total")
    list_filter = ("order__created_at", "product_name")
    search_fields = ("order__user__username", "product_name")
    

