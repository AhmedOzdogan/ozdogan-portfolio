from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from main.models import Menu, Reservations
from .serializers import MenuSerializer, ReservationsSerializer

class MenuListAPIView(APIView):
    def get(self, request):
        menu_items = Menu.objects.filter(available=True)
        serializer = MenuSerializer(menu_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class MenuItemAPIView(APIView):
    def get(self, request, slug):
        menu_item = get_object_or_404(Menu, slug=slug, available=True)
        return Response(MenuSerializer(menu_item).data)
    
class ReservationAPIView(APIView):
    def post(self, request):
        serializer = ReservationsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ReservationCheckAPIView(APIView):
    def post(self, request):
        reservation_id = request.data.get("reservation_id")
        email = request.data.get("email")
        print(f"Received reservation_id: {reservation_id}, email: {email}")

        if not reservation_id or not email:
            return Response({"error": "Missing reservation ID or email."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            reservation = Reservations.objects.get(id=reservation_id, email=email)
        except Reservations.DoesNotExist:
            return Response({"error": "Reservation not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ReservationsSerializer(reservation)
        return Response(serializer.data)