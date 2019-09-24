from django.conf.urls import url
from . import api

urlpatterns = [
    url("init", api.initialize),
    url("genworld", api.gen_world),
    url("test", api.connect),
]

