from django.urls import path, include
from .views import AddOnView,AddOnByCategoryView, ProductListCreateView,ProductDetailView

urlpatterns = [
    path("products/", ProductListCreateView.as_view(), name="product-list"),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="product-detail"),
    path("addons/", AddOnView.as_view(), name="addon-list"),
    path("addons/category/<int:category_id>/", AddOnByCategoryView.as_view(), name="addon-category-list"),
]