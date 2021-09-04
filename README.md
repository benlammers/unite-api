
# Unite API

**Table of Contents**
- [Purpose](#purpose)
- [Description](#description)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [Challenges](#challenges)
- [Possible Improvements](#possible-improvements)

## Purpose
This Django app provides a REST API with endpoints for wedding RSVP's and an admin dashboard to input guests names.

## Description
The Unite API supplies a client application with a wedding RSVP system. It does this by exposing endpoints for the client to search potential guests and submit and update guests RSVP information such as whether they will be attending, meal choice, song request, etc. It also provides an admin dashboard where the administrator can input guests names and view the updated information. It also emails the administrator upon each submission of an RSVP with the inputted data.

### Get Spotify Token
**`GET /api/spotify-token/`**

Response
```
{ token: string }
```

### Search RSVP Groups by Guest Name
**`GET /api/groups/search/`**

Request Params
```
name: string
```

Response
```
{[
    {
        id: number,
        name: string,
        song: 
        attending: boolean,
        dietary_restrictions: string[],
        dietary_notes: string,
        group: {
            id: number,
            rsvp: boolean
        }
    },
    ... more guests in group
]}
```

### Update Group
`PUT /api/groups/update/`

Request Body
```
{[
    {
        id: number,
        name: string,
        song: 
        attending: boolean,
        dietary_restrictions: string[],
        dietary_notes: string,
        group: {
            id: number,
            rsvp: boolean
        }
    },
    ... more guests in group
]}
```

Response
```
"Update Success"
```

## Tech Stack
- [Django](https://docs.djangoproject.com/en/3.2/)
- [PostgreSQL](https://www.postgresql.org/docs/)

## Getting Started
To run the API locally, clone the repo then run `pip install -r requirements.txt` to install the Python dependencies. 

Add an .env with the following values: SECRET_KEY, DEBUG_VALUE, DATABASE_ENGINE, DATABASE_HOST, DATABASE_NAME, DATABASE_USER, DATABASE_PASSWORD, EMAIL_BACKEND, EMAIL_HOST, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD and EMAIL_PORT. For context for these values look in /unite/unite/settings.py as well as documentation for [database settings](https://docs.djangoproject.com/en/3.1/ref/settings/#databases) and [email settings](https://docs.djangoproject.com/en/3.1/ref/settings/#email-backend).

When you first connect your database and whenever you update your models `cd` into /unite then run `python manage.py makemigrations` then `python manage.py migrate`.
To run the app run `python manage.py runserver` also in /unite.

**Deployment**
- Procfile is a gunicorn configuration file for the Heroku deployment

## Challenges
One of the biggest challenges I faced when developing this API was hosting it. I decided to go through Heroku as it provides free tier options. It was not the plug and play set up I was used to with hosting front end applications on the likes of Vercel and Netlify. It took me a while to get the correct files uploaded for configuration and took me a frustratingly long time to realize Heroku ignoring my database settings and was pointing the API at a free database it created and hosted for me rather than my PostgreSQL database on AWS.

## Possible Improvements

### Add Testing
As RSVP information can be critical to the planning process of a wedding it would be quite problematic if it were to fail or misrepresent the submitted RSVPs. Therefore, a very important addition to this API would be to add thorough testing and error handling.
