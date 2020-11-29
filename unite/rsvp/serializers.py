from rest_framework import serializers

from .models import (Song, Guest, Group)

class GuestSerializer(serializers.ModelSerializer):
   class Meta: 
      model = Guest
      fields = ["id", "name", "song", "attending", "dietary_restrictions", "dietary_notes", "group"]
      depth = 1

class GuestUpdateSerializer(serializers.ModelSerializer):
   class Meta:
      model = Guest 
      fields = ["song", "attending", "dietary_restrictions", "dietary_notes"]

   def update(self, instance, validated_data):
      instance.attending = validated_data["attending"]
      instance.dietary_notes = validated_data["dietary_notes"]
      instance.dietary_restrictions = validated_data["dietary_restrictions"]
      # Handle Song
      try:
         song_title = validated_data["song"]["title"]
         song_artist = validated_data["song"]["artist"]
         song_image_uri = validated_data["song"]["image_uri"]
         try: 
            song = Song.objects.get(title=song_title, artist=song_artist)
            instance.song = song
         except Song.DoesNotExist:
            song = Song(title=song_title, artist=song_artist, image_uri=song_image_uri)
            song.save()
            instance.song = song
      except TypeError:
         pass
      instance.save()
      return instance

class GroupUpdateSerializer(serializers.ModelSerializer):
   class Meta:
      model = Group
      field = ["rsvp"]

   def update(self, instance, validated_data):
      instance.rsvp = validated_data["rsvp"]
      instance.save()
      return instance