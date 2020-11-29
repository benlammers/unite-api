from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from multiselectfield import MultiSelectField

class Group(models.Model):
    rsvp = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Group'
        verbose_name_plural = 'Groups'        

    def __str__(self):
        return "Group_" + str(self.id)

DIETARY_RESTRICTIONS = [
    ("VEGAN", "VEGAN"),
    ("VEGETARIAN", "VEGETARIAN"),
    ("GLUTEN-FREE", "GLUTEN-FREE"),
    ("DAIRY-FREE", "DAIRY-FREE"),
    ("OTHER", "OTHER")
]

class Guest(models.Model):
    name = models.CharField(max_length=60)
    attending = models.BooleanField(default=False)
    song = models.ForeignKey('Song', on_delete=models.PROTECT, blank=True, null=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, blank=True)
    dietary_restrictions = MultiSelectField(choices=DIETARY_RESTRICTIONS, blank=True)
    dietary_notes = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Guest'
        verbose_name_plural = 'Guests'

    def __str__(self):
        return self.name


class Song(models.Model):
    title = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    image_uri = models.CharField(max_length=200)

    class Meta:
        verbose_name = 'Song'
        verbose_name_plural = 'Songs'

    def __str__(self):
        return self.title



