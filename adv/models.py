from django.db import models, transaction
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from polymorphic.models import PolymorphicModel
from uuid import uuid4

# Create your models here.


class Item(PolymorphicModel):
    name = models.CharField(max_length=50, default="Useful Item")
    description = models.CharField(max_length=128, default="This does everything")
    value = models.DecimalField(max_digits=7, decimal_places=2, default=0)

    class Meta:
        ordering = ("id",)


class Weapon(Item):
    damage = models.IntegerField(default=8)


class Armor(Item):
    armor_value = models.IntegerField(default=1)


class Room(models.Model):
    title = models.CharField(max_length=50, default="DEFAULT TITLE")
    description = models.CharField(max_length=500, default="DEFAULT DESCRIPTION")
    n_to = models.IntegerField(default=0)
    s_to = models.IntegerField(default=0)
    e_to = models.IntegerField(default=0)
    w_to = models.IntegerField(default=0)

    items = models.ManyToManyField(Item)

    class Meta:
        ordering = ("id",)

    # Take in a room and direction to establish connection
    def connect_room(self, destination, direction):
        id = destination.id
        try:
            destination = Room.objects.get(id=id)
        except Room.DoesNotExist:
            print("That room does not exist")
        else:
            setattr(self, f"{direction}_to", id)
            self.save()


class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    currentRoom = models.IntegerField(default=1)
    uuid = models.UUIDField(default=uuid4, primary_key=True, editable=False)

    items = models.ManyToManyField(Item)

    def get_room(self):
        return Room.objects.get(id=self.currentRoom)


@receiver(post_save, sender=User)
def create_user_player(sender, instance, created, **kwargs):
    if created:
        Player.objects.create(user=instance)
        Token.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_player(sender, instance, **kwargs):
    instance.player.save()
