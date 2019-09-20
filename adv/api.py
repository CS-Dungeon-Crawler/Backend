from rest_framework import serializers, viewsets
from rest_framework.response import Response

# from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from .models import Room, Player
import json


class RoomSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Room
        fields = ("title", "description")


class RoomViewSet(viewsets.ModelViewSet):
    serializer_class = RoomSerializer
    queryset = Room.objects.all()


@api_view(["GET"])
def something(request):
    print(request.user.player.uuid)
    return Response(request.method)
