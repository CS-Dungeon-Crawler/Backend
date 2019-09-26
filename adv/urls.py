from django.conf.urls import url
from . import api

urlpatterns = [
    url("init", api.initialize),
    url("move", api.move),
    url("take", api.take),
    url("drop", api.drop),
    url("genworld", api.gen_world),
    url("test", api.test),
]

