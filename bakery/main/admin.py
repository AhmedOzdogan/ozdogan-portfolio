from django.contrib import admin
from .models import Category, Product, Address

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "created_at", "updated_at")
    search_fields = ("name", "slug", "description")
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("name",)
    readonly_fields = ("created_at", "updated_at")

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "stock", "created_at", "updated_at")
    list_filter = ("category", "created_at")
    search_fields = ("name", "slug", "description")
    autocomplete_fields = ("category",)
    prepopulated_fields = {"slug": ("name",)}
    list_editable = ("price", "stock")
    ordering = ("category__name", "name")
    readonly_fields = ("created_at", "updated_at")
    list_select_related = ("category",)
    
@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("user", "full_name", "city", "country", "is_default", "created_at")
    list_filter = ("country", "is_default", "created_at")
    search_fields = ("full_name", "line1", "city", "postal_code", "user__username", "user__email")
    autocomplete_fields = ("user",)
    readonly_fields = ("created_at", "updated_at")

