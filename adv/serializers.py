from rest_framework import serializers
from rest_polymorphic.serializers import PolymorphicSerializer
from .models import Item, Armor, Weapon, Room


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ("id", "name", "description", "value")


class ArmorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Armor
        fields = ("id", "name", "description", "value", "armor_value")


class WeaponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weapon
        fields = ("id", "name", "description", "value", "damage")


class ItemPolymorphicSerializer(PolymorphicSerializer):
    model_serializer_mapping = {
        Item: ItemSerializer,
        Armor: ArmorSerializer,
        Weapon: WeaponSerializer,
    }


class RoomSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Room
        fields = ("id", "title", "description", "n_to", "s_to", "e_to", "w_to")
