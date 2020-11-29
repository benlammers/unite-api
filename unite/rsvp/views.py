from rest_framework import generics

from .serializers import (SongSerializer, GuestSerializer,
                          GuestUpdateSerializer, GroupUpdateSerializer,
                          GroupSerializer)
from .models import (Song, Guest, Group)

from django.core.mail import EmailMessage
from django.http import (HttpResponse, JsonResponse)

import os
import requests

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

def index(self):
    return HttpResponse("Unite API")


def get_spotify_token(request):
    spotify_url = "https://accounts.spotify.com/api/token"
    data = {"grant_type": "client_credentials"}
    headers = {"Authorization": os.environ.get('SPOTIFY_TOKEN')}
    response = requests.post(spotify_url, data=data, headers=headers)
    return JsonResponse({"token": response.json()['access_token']})


class SongView(generics.ListAPIView):
    ''' Retrieve List of All Songs '''
    queryset = Song.objects.all().order_by('title')
    serializer_class = SongSerializer


class GuestView(generics.ListAPIView):
    ''' Retrieve List of All Guests '''
    queryset = Guest.objects.all().order_by('name')
    serializer_class = GuestSerializer


class GroupView(generics.ListAPIView):
    ''' Retrieve List of All Groups '''
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class GroupSearchView(generics.ListAPIView):
    ''' Retrieve Group that Contains Guest Name '''
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

    def filter_queryset(self, queryset):
        params = self.request.GET
        # Return all Guests that are part of a Group containing a Guest with the given name
        return queryset.filter(group__in=Group.objects.filter(guest__isnull=False, guest__name__iexact=params['name']))


def getFormattedGuestData(guests):
    guestEmailData = []

    for guest in guests:
        guestString = '''Name: {name}<br/>'''.format(name=guest['name'])
        # Attending
        if (guest['attending'] == False):
            guestString += "Attending: No<br/>"
        else: 
            guestString += "Attending: Yes<br/>"
        # Dietary Info
        if (len(guest['dietary_restrictions']) > 0):
            guestString += '''
                Dietary Restrictions: {restrictions}<br/>
                Dietary Notes: {notes}<br/>
            '''.format(restrictions=", ".join(guest['dietary_restrictions']), notes=guest['dietary_notes'] )
        else:
            guestString += "Dietary Restrictions: None<br/>"
        # Song Info
        if (guest['song'] != None):
            guestString += '''
                Song Title: {title}<br/>
                Song Artist: {artist}<br/>
            '''.format(title=guest['song']['title'], artist=guest['song']['artist'])
        else:
            guestString += "Song: None<br/>" 
        guestEmailData.append(guestString)

    return guestEmailData


def sendConfirmationEmail(guests):
    guestEmailData = getFormattedGuestData(guests)

    subject = 'Wedding RSVP Confirmation'
    html = """{guestsInfo}""".format(guestsInfo="<br/>".join(guestEmailData))

    email = EmailMessage(subject, html, to=['21benlammers@gmail.com'])
    # Set email content to HTML
    email.content_subtype = "html"
    # Send email message
    email.send()
    

class GroupUpdateView(generics.UpdateAPIView):
    ''' Update Group using RSVP Info '''

    def update(self, request, *args, **kwargs):
        guests = request.data["guests"]
        sendConfirmationEmail(guests)

        for guestData in guests:
            guest = Guest.objects.get(id=guestData["id"])
            serializer = GuestUpdateSerializer(guest, guestData)
            serializer.update(guest, guestData)

        group = Group.objects.get(id=guests[0]['group']['id'])
        serializer = GroupUpdateSerializer(group, { "rsvp": True })
        serializer.update(group, { "rsvp": True })
        
        return HttpResponse("Update Success")
