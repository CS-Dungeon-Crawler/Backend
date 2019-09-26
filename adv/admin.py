from django.contrib import admin
from .models import Room, Player, Item, Armor, Weapon

# Register your models here.


class PlayerItemInLine(admin.TabularInline):
    model = Player.items.through


class RoomItemInLine(admin.TabularInline):
    model = Room.items.through


class PlayerAdmin(admin.ModelAdmin):
    # model = Player
    # filter_horizontal = ("items",)
    inlines = [PlayerItemInLine]
    exclude = ("items",)


class RoomAdmin(admin.ModelAdmin):
    inlines = [RoomItemInLine]
    exclude = ("items",)


admin.site.register(Room, RoomAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(Item)
admin.site.register(Armor)
admin.site.register(Weapon)
