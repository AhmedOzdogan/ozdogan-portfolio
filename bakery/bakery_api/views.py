
# views.py
from rest_framework import generics, permissions
from main.models import Product, AddOn
from .serializers import ProductSerializer, AddOnSerializer

class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class AddOnView(generics.ListCreateAPIView):
    queryset = AddOn.objects.all()
    serializer_class = AddOnSerializer
    
class AddOnByCategoryView(generics.ListAPIView):
    serializer_class = AddOnSerializer

    def get_queryset(self):
        category_id = self.kwargs.get("category_id")  # e.g. /api/addons/category/3/
        return AddOn.objects.filter(category_id=category_id)