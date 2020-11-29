from django.contrib import admin
from django.db import models
from django.forms import Textarea
from django.utils.safestring import mark_safe
from django.urls import reverse

from .models import (Song, Guest, Group)

class SongAdmin(admin.ModelAdmin):
   fields = ["title", "artist", "image_uri"]
   list_display = ["title", "artist", "image"]

   def image(self, obj):
      return mark_safe('<a target="_blank" href="%s">%s</a>' % (obj.image_uri, obj.image_uri))
      
   def get_fieldsets(self, request, obj=None):
      return [(None, {'fields': ['title', 'artist', 'image_uri']})]

class GuestInLine(admin.TabularInline):
   model = Guest
   fields = ["name"]
   extra = 1

class GuestAdmin(admin.ModelAdmin):
   fields = ["name", "attending", "song", "group", "dietary_restrictions", "dietary_notes"]
   list_display = ["name", "attending", "song", "group"]
   formfield_overrides = {
      models.CharField: {'widget': Textarea(attrs={'rows': 1, 'cols': 60})},
      models.TextField: {'widget': Textarea(attrs={'rows': 6, 'cols': 60})}
   }

   def group(self, guest):
      url = reverse("admin:rsvp_group_change", args=[guest.group.id])
      link = '<a href="%s">%s</a>' % (url, guest.group)
      return mark_safe(link)

class GroupAdmin(admin.ModelAdmin):
   list_display = ["group", "guests", "rsvp"]
   inlines = [GuestInLine]

   def group(self, group):
      url = reverse("admin:rsvp_group_change", args=[group.id])
      link = '<a href="%s">%s</a>' % (url, group)
      return mark_safe(link)

   def guests(self, group):
      guest_list = list(map(str, Guest.objects.filter(group=group)))
      return ", ".join(guest_list)

   # Hide RSVP Field When Creating Group
   def get_form(self, request, obj=None, **kwargs):
      if obj is None:
         self.exclude = ["rsvp"]
      form = super(GroupAdmin, self).get_form(request, obj, **kwargs)
      return form

admin.site.register(Song, SongAdmin)
admin.site.register(Guest, GuestAdmin)
admin.site.register(Group, GroupAdmin)