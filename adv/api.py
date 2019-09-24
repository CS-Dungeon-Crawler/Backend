from rest_framework import serializers, viewsets
from rest_framework.response import Response
import asyncio
import random

from rest_framework.permissions import IsAdminUser
from django.db import connection
from django.core.management.color import no_style
from django.http import JsonResponse
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from .models import Room, Player
import json

from util.create_world import create_world, generate_grid, generate_rooms


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


@api_view(["GET", "POST"])
def connect(request):
    Room.objects.all().delete()
    sequence_sql = connection.ops.sequence_reset_sql(no_style(), [Room])
    with connection.cursor() as cursor:
        for sql in sequence_sql:
            cursor.execute(sql)
    generate_rooms(4)
    grid = generate_grid(4)
    rooms = Room.objects.all()
    room_index = 0
    for y in range(len(grid)):
        for x in range(len(grid)):
            grid[y][x] = rooms[room_index]
            room_index += 1
    i = 0
    while i < 4:
        grid[0][i].connect_room(grid[1][i], "n")
        i += 1
    serializer = RoomSerializer(rooms, many=True)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes((IsAdminUser,))
def gen_world(request):
    Room.objects.all().delete()
    sequence_sql = connection.ops.sequence_reset_sql(no_style(), [Room])
    with connection.cursor() as cursor:
        for sql in sequence_sql:
            cursor.execute(sql)

    data = json.loads(request.body)
    size = data["size"]
    create_world(size)

    rooms = Room.objects.all().order_by("id")
    serializer = RoomSerializer(rooms, many=True)
    return Response(serializer.data)

