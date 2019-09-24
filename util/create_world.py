from django.contrib.auth.models import User
from adv.models import Room, Player
import math
import random

room_list = [
    "Room",
    "Chamber",
    "Hall",
    "Passage",
    "Cavity",
    "Hollow",
    "Cell",
    "Auditorium",
    "Antechamer",
    "Alcove",
]

adjective_list = [
    "Dusty",
    "Moldy",
    "Scary",
    "Dark",
    "Bright",
    "Small",
    "Large",
    "Quiet",
    "Simple",
    "Musty",
]


def generate_rooms(size):
    for i in range(size * size):
        title = f"{random.choice(adjective_list)} {random.choice(room_list)}"
        r = Room.objects.create(title=title, description="Generic")
        r.save()


def create_world(size):
    n = size
    generate_rooms(size)
    rooms = Room.objects.all().order_by("id")

    direction_list = ["n_to", "s_to", "e_to", "w_to"]
    opposite = {"n": "s", "s": "n", "e": "w", "w": "e"}
    direction_dict = {"n_to": -n, "s_to": n, "w_to": -1, "e_to": 1}
    for i, room in enumerate(rooms):
        temp = direction_list[:]
        del_list = []
        if i == 0 or i == n - 1 or i == n * (n - 1) or i == n * n - 1:
            max_connections = 2
            if i == 0:
                del_list = ["n_to", "w_to"]
            elif i == n - 1:
                del_list = ["n_to", "e_to"]
            elif i == n * (n - 1):
                del_list = ["s_to", "w_to"]
            else:
                del_list = ["s_to", "e_to"]

        elif (
            math.floor(i / n) == 0
            or i % n == 0
            or i % n == n - 1
            or math.ceil(i / n) == n
        ):
            max_connections = 3
            if i % n == n - 1:
                del_list = ["e_to"]
            elif i % n == 0:
                del_list = ["w_to"]
            elif math.floor(i / n) == 0:
                del_list = ["n_to"]
            else:
                del_list = ["s_to"]
        else:
            max_connections = 4

        for dr in del_list:
            temp.remove(dr)

        connections = random.randint(0, max_connections)

        while connections > 0:
            random_direction = random.choice(temp)
            if getattr(room, random_direction) == 0:
                new_index = i + direction_dict[random_direction]
                room.connect_room(rooms[new_index], random_direction[0])
                rooms[new_index].connect_room(room, opposite[random_direction[0]])
            connections -= 1
            temp.remove(random_direction)


# create_world(3)
# grid = create_world(3)
# for row in grid:
#     print(row)
