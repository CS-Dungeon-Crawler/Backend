from .text_lists import adjective_list, room_list, description_list
import random


def room_description():
    title = f"{random.choice(adjective_list)} {random.choice(room_list)}"
    description = random.choice(description_list)

    return {"title": title, "description": description}
