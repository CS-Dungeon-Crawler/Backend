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
        fields = ("id", "title", "description", "n_to", "s_to", "e_to", "w_to")


class RoomViewSet(viewsets.ModelViewSet):
    serializer_class = RoomSerializer
    queryset = Room.objects.all()


@api_view(["GET"])
def initialize(request):
    player = request.user.player
    room = player.get_room()
    all_players = Player.objects.filter(currentRoom=room.id)
    player_ids = [pl.user.username for pl in all_players if pl.uuid != player.uuid]

    return Response(
        {
            "uuid": player.uuid,
            "name": request.user.username,
            "title": room.title,
            "description": room.description,
            "players": player_ids,
        }
    )
