from django.contrib.auth.models import User
from adv.models import Room, Player, Item
import math
import random

from util.text_generation import room_description


# Add total number of rooms to the Database
def generate_rooms(size):
    items = Item.objects.all()
    for i in range(size * size):
        # title = f"{random.choice(adjective_list)} {random.choice(room_list)}"
        add_items = random.randint(0, 2)
        new_room = room_description()
        r = Room.objects.create(
            title=new_room["title"], description=new_room["description"]
        )

        while add_items > 0 and len(items) != 0:
            r.items.add(random.choice(items))
            add_items -= 1

        r.save()


# Randomly connect rooms in a grid layout to form the dungeon
def create_world(size):
    n = size
    generate_rooms(size)
    rooms = Room.objects.all().order_by("id")

    # To help manage directions in the grid
    direction_list = ["n_to", "s_to", "e_to", "w_to"]
    opposite = {"n": "s", "s": "n", "e": "w", "w": "e"}
    direction_dict = {"n_to": -n, "s_to": n, "w_to": -1, "e_to": 1}

    # Create a random continuous path from starting room to opposite corner
    index = 0
    while index < len(rooms) - 1:
        path_list = [1, n]
        if index % n == n - 1:
            next_step = n
        elif math.ceil(index / n) == n or index == n * (n - 1):
            next_step = 1
        else:
            next_step = random.choice(path_list)

        next_room = index + next_step
        next_direction = [
            key for key, val in direction_dict.items() if val == next_step
        ][0][0]

        rooms[index].connect_room(rooms[next_room], next_direction)
        rooms[next_room].connect_room(rooms[index], opposite[next_direction])

        index = next_room

    # Iterate through every room
    for i, room in enumerate(rooms):
        # Make a copy of the list as items will be deleted
        temp = direction_list[:]
        # Will be filled with directions that aren't possible for edges and corners
        del_list = []

        # Set ineligible directions for each corner of the grid
        if i == 0 or i == n - 1 or i == n * (n - 1) or i == n * n - 1:
            # max_connections = 2
            data_list = [1] * 3 + [2] * 2
            if i == 0:
                del_list = ["n_to", "w_to"]
            elif i == n - 1:
                del_list = ["n_to", "e_to"]
            elif i == n * (n - 1):
                del_list = ["s_to", "w_to"]
            else:
                del_list = ["s_to", "e_to"]

        # Set ineligible directions for the edges of the grid
        elif (
            math.floor(i / n) == 0
            or i % n == 0
            or i % n == n - 1
            or math.ceil(i / n) == n
        ):
            # max_connections = 3
            data_list = [0] + [1] * 5 + [2] * 2 + [3] * 2
            if i % n == n - 1:
                del_list = ["e_to"]
            elif i % n == 0:
                del_list = ["w_to"]
            elif math.floor(i / n) == 0:
                del_list = ["n_to"]
            else:
                del_list = ["s_to"]
        else:
            # max_connections = 4
            data_list = [1] * 2 + [2] * 6 + [3] * 4

        # Ammend list of directions
        for dr in del_list:
            temp.remove(dr)

        old_connections = 0
        for dr in direction_list:
            old_connections += 1 if getattr(room, dr) != 0 else 0

        # Set a random number of connections for current room
        connections = random.choice(data_list) - old_connections

        # Create each connection
        while connections > 0:
            random_direction = random.choice(temp)  # Pick a random choice from the list

            # If there is no room connected in that direction then make a new connection
            if getattr(room, random_direction) == 0:
                new_index = i + direction_dict[random_direction]

                # Connect current to new and then new back to current
                # Pulling off the first letter of random_direction cause the method only accepts 'n', 's', 'e' or 'w'
                room.connect_room(rooms[new_index], random_direction[0])
                rooms[new_index].connect_room(room, opposite[random_direction[0]])

            # Whether or not it was created, remove the direction and reduce the number of connections
            connections -= 1
            temp.remove(random_direction)
