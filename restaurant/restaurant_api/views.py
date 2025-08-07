from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from main.models import Menu
from .serializers import MenuSerializer

class MenuListAPIView(APIView):
    def get(self, request):
        menu_items = Menu.objects.filter(available=True)
        serializer = MenuSerializer(menu_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class MenuItemAPIView(APIView):
    def get(self, request, slug):
        menu_item = Menu.objects.filter(slug=slug, available=True).first()
        if menu_item:
            serializer = MenuSerializer(menu_item)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"detail": "Menu item not found."}, status=status.HTTP_404_NOT_FOUND)