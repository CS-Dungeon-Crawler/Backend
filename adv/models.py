from django.db import models, transaction
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from uuid import uuid4

# Create your models here.


class Room(models.Model):
    title = models.CharField(max_length=50, default="DEFAULT TITLE")
    description = models.CharField(max_length=500, default="DEFAULT DESCRIPTION")
    n_to = models.IntegerField(default=0)
    s_to = models.IntegerField(default=0)
    e_to = models.IntegerField(default=0)
    w_to = models.IntegerField(default=0)

    # Take in a room and direction to establish connection

    def connect_room(self, destination, direction):
        # opposite = {"n": "s", "s": "n", "e": "w", "w": "e"}
        # reverse = opposite[direction]
        id = destination.id
        # print("current room", self)
        try:
            destination = Room.objects.get(id=id)
        except Room.DoesNotExist:
            print("That room does not exist")
        else:
            setattr(self, f"{direction}_to", id)
            # setattr(destination, f"{reverse}_to", self.id)
            # print("connecting backwards", getattr(destination, f"{reverse}_to"))
            # something = [self, destination]
            # with transaction.atomic():
            #     for i in something:
            #         i.save()
            self.save()
            # destination.save()


class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    currentRoom = models.IntegerField(default=1)
    uuid = models.UUIDField(default=uuid4, primary_key=True, editable=False)

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
