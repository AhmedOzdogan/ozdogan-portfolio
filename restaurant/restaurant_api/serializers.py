from rest_framework import serializers
from main.models import Menu, Category, Reservations

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class MenuSerializer(serializers.ModelSerializer):
    category = CategorySerializer()  # Nested category details

    class Meta:
        model = Menu
        fields = ['id', 'name', 'slug', 'description', 'price', 'available', 'category']

class ReservationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservations
        fields = ['id', 'name', 'email', 'reservation_date', 'number_of_guests']
