from django.shortcuts import render
from rest_framework import viewsets
from .models import Item, Room
from .serializers import RoomSerializer, ItemPolymorphicSerializer

# Create your views here.


class ItemViewSet(viewsets.ModelViewSet):
    serializer_class = ItemPolymorphicSerializer
    queryset = Item.objects.all()


class RoomViewSet(viewsets.ModelViewSet):
    serializer_class = RoomSerializer
    queryset = Room.objects.all().order_by("id")
