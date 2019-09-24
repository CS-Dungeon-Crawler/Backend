from django.contrib.auth.models import User
from adv.models import Room, Player
import asyncio
import random


def generate_rooms(size):
    # return size
    for i in range(size * size):
        r = Room.objects.create(title="Generic", description="Generic")
        r.save()


def generate_grid(size):
    grid = [None] * size
    for y in range(len(grid)):
        grid[y] = [None] * size
    return grid


def create_world(size):
    grid = generate_grid(size)
    generate_rooms(size)
    rooms = Room.objects.all().order_by("id")
    room_index = 0

    # Populate grid
    for y in range(len(grid)):
        for x in range(len(grid)):
            grid[y][x] = rooms[room_index]
            room_index += 1

    for y in range(len(grid)):
        print(grid[y])
    # Build a path to the opposite corner
    x = y = 0
    cardinal = ["e", "s"]
    opposite = {"n": "s", "s": "n", "e": "w", "w": "e"}
    while x <= size - 1 and y <= size - 1:
        direction = random.randint(0, 1)
        current_room = grid[y][x]
        if x == len(grid) - 1:
            y += 1
        elif y == len(grid) - 1:
            x += 1
        else:
            if direction == 0:
                x += 1
            else:
                y += 1

        if x == size - 1 and y == size - 1:
            current_room.connect_room(grid[y][x], cardinal[direction])
            grid[y][x].connect_room(current_room, opposite[cardinal[direction]])
            break

        current_room.connect_room(grid[y][x], cardinal[direction])
        grid[y][x].connect_room(current_room, opposite[cardinal[direction]])

    # Fill out connections to all rooms
    end = size - 1
    room_dir = ["n_to", "s_to", "e_to", "w_to"]
    attr_dict = {"n_to": -1, "s_to": 1, "e_to": 1, "w_to": -1}

    for y in range(0, size):
        for x in range(0, size):
            # print(f"curr is {y}, {x}")
            current_room = grid[y][x]
            old_connections = 0
            for dirc in room_dir:
                old_connections += 1 if getattr(grid[y][x], dirc) > 0 else 0

            max_connections = 1
            if (
                (y == 0 and x == 0)
                or (y == 0 and x == end)
                or (y == end and x == 0)
                or (y == end and x == end)
            ):
                # print("corner")
                max_connections = 2
            elif (x == 0 or x == end) or (y == 0 or y == end):
                # print(f"  edge: {y}, {x}")
                # print(grid[y][x])
                max_connections = 3
            else:
                max_connections = 4

            new_connections = random.randint(0, max_connections) - old_connections

            while new_connections > 0:
                temp = room_dir[:]
                for dr in room_dir:
                    if getattr(current_room, dr):
                        temp.remove(dr)
                # print("here")
                created = False
                while not created:
                    lat = lon = 0
                    random_direction = random.choice(temp)
                    # print("why", random_direction)
                    if random_direction == "n_to" or random_direction == "s_to":
                        lat = attr_dict[random_direction]
                    else:
                        lon = attr_dict[random_direction]
                    print(f"lat {lat}, lon {lon} connections left: {new_connections}")
                    new_x, new_y = x + lon, y + lat
                    print(f" old: ({y}, {x})  new: ({new_y}, {new_x})")

                    if (0 <= new_y <= end) and (0 <= new_x <= end):
                        next_room = grid[new_y][new_x]
                        # print(next_room, current_room)
                        current_room.connect_room(next_room, random_direction[0])
                        next_room.connect_room(
                            current_room, opposite[random_direction[0]]
                        )
                        # # print(
                        #     f"Connecting {current_room} to {next_room} by {random_direction[0]}"
                        # )
                        created = True

                    temp.remove(random_direction)
                    if len(temp) == 0:
                        print("not created")
                        created = True
                        break
                new_connections -= 1


# create_world(3)
# grid = create_world(3)
# for row in grid:
#     print(row)
