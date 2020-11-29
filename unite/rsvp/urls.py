from django.urls import path

from . import views
from .views import (GroupSearchView, GroupUpdateView)

app_name = 'rsvp'

urlpatterns = [
    path("", views.index, name="index"),
    path("spotify-token/", views.get_spotify_token, name="spotify"),
    path("groups/search", GroupSearchView.as_view(), name="groups_search"),
    path("groups/update", GroupUpdateView.as_view(), name="groups_update"),
]
