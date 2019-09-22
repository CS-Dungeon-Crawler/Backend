from django.conf.urls import url
from . import api

urlpatterns = [url("init", api.initialize), url("genrooms", api.gen_rooms)]

