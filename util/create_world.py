from django.contrib.auth.models import User
from adv.models import Room, Player


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
    print(grid[2][0])


# create_world(3)
# grid = create_world(3)
# for row in grid:
#     print(row)
