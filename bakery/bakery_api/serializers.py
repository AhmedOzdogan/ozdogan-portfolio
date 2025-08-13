from main.models import Product, Category, AddOn
from rest_framework import serializers

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    picture = serializers.SerializerMethodField()
    
    def get_picture(self, obj):
        if not obj.picture:
            return None
        request = self.context.get("request")
        return request.build_absolute_uri(obj.picture.url) if request else obj.picture.url
    
    def get_addons(self, obj):
        qs = AddOn.objects.filter(category=obj.category, is_active=True).order_by("name")
        return AddOnSerializer(qs, many=True).data

    class Meta:
        model = Product
        fields = ["id", "name", "slug", "description", "price", "picture", "stock", "category"]
        
class AddOnSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddOn
        fields = ["id", "name", "category", "price", "is_active"]
