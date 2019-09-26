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
from .models import Room, Player, Item, Armor, Weapon
from .serializers import ItemPolymorphicSerializer, RoomSerializer
import json

from util.create_world import create_world, generate_rooms
from util.text_generation import room_description


@api_view(["GET"])
def test(request):
    pass


@api_view(["GET"])
def initialize(request):
    player = request.user.player
    room = player.get_room()
    all_players = Player.objects.filter(currentRoom=room.id)
    player_ids = [pl.user.username for pl in all_players if pl.uuid != player.uuid]
    treasure = ItemPolymorphicSerializer(room.items, many=True)
    inventory = ItemPolymorphicSerializer(player.items, many=True)

    return Response(
        {
            "uuid": player.uuid,
            "name": request.user.username,
            "room_id": room.id,
            "title": room.title,
            "description": room.description,
            "players": player_ids,
            "inventory": inventory.data,
            "treasure": treasure.data,
        }
    )


@api_view(["POST"])
def move(request):
    player = request.user.player
    current_room_id = player.currentRoom

    current_room = Room.objects.get(id=current_room_id)

    data = json.loads(request.body)
    direction = data["direction"]

    new_room_id = getattr(current_room, f"{direction}_to")
    if new_room_id == 0:
        return Response({"message": "There is no room in that direction"})
    else:
        player.currentRoom = new_room_id
        player.save()
        new_room = Room.objects.get(id=new_room_id)
        serializer = RoomSerializer(new_room)
        return Response({"message": "You moved to a new room", "room": serializer.data})


@api_view(["POST"])
def take(request):
    player = request.user.player
    current_room_id = player.currentRoom
    current_room = Room.objects.get(id=current_room_id)

    data = json.loads(request.body)
    id = data["id"]

    loot = current_room.items.get(id=id)
    current_room.items.remove(loot)
    player.items.add(loot)
    player.save()

    return Response({"message": f"You looted {loot.name}"})


@api_view(["POST"])
def drop(request):
    player = request.user.player
    current_room_id = player.currentRoom
    current_room = Room.objects.get(id=current_room_id)

    data = json.loads(request.body)
    id = data["id"]

    loot = player.items.get(id=id)
    player.items.remove(loot)
    current_room.items.add(loot)
    current_room.save()

    return Response({"message": f"You dropped {loot.name}"})


@api_view(["POST"])
@permission_classes((IsAdminUser,))
def gen_world(request):

    # Delete Rooms in Database and reset ID sequence
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

