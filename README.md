# Unite Rest API

A simple Django application to provide a REST
API to the Unite application.

The entire application is contained within the /unite folder.

`Procfile` is a gunicorn configuration file for the Heroku deployment.

`requirements.txt` contains a list of the required Python packages.

## Install

    pip install -r requirements.txt

## Run the App

    cd unite/
    python manage.py runserver

# REST API

The REST API to the Unite app is described below.

## Get Spotify Auth Token

### Request

`GET /api/spotify-token/`

### Response

  {
    token: ACCESS_TOKEN
  }
  
## Search Groups by Guest Name

### Request

`GET /api/groups/search/`

### Response

  {
    
  }
    
## Update Guests RSVP Info by Group

### Request

`GET /api/groups/update/`

### Response

  {
    
  }
