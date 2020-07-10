#!/usr/bin/python3

import requests
import json
import pendulum
import os

# GLOBAL SETTINGS
token_file = 'strava_tokens.json'
secret_file = 'secrets.json'
auth_url = 'https://www.strava.com/api/v3/oauth/token',


def get_token(secrets):
    response = requests.post(
        url=auth_url,
        data={
            'client_id': secrets['client_id'],
            'client_secret': secrets['client_secret'],
            'code': secrets['code'],
            'grant_type': 'authorization_code'
            }
        )

    strava_tokens = response.json()

    with open(token_file, 'w') as outfile:
        json.dump(strava_tokens, outfile)


def refresh_token(secrets, oldtoken):

    # refresh the token
    response = requests.post(
        url=auth_url,
        data={
            'client_id': secrets['client_id'],
            'client_secret': secrets['client_secret'],
            'refresh_token': oldtoken['refresh_token'],
            'grant_type': 'refresh_token'
            }
        )

    # update the old token
    for k, v in response.json().items():
        oldtoken[k] = v

    # Save tokens to file
    with open(token_file, 'w') as outfile:
        json.dump(oldtoken, outfile)


def get_my_activities(token):
    url = "https://www.strava.com/api/v3/activities"

    activities = requests.get(f"{url}?access_token={token['access_token']}").json()

    # get start of week
    sow = pendulum.now().start_of('week')

    # list activities from this week only
    for x in activities:
        if pendulum.parse(x['start_date']) > sow:
            print(f"{x['start_date']} {x['distance']} {x['type']}")


with open(secret_file) as s_file:
    secrets = json.load(s_file)

# get token, if it does not exist
if not os.path.exists(token_file):
    get_token(secrets)

# load the existing token
with open(token_file) as check:
    token = json.load(check)

# if it expired - get and load a new one
if pendulum.from_timestamp(token['expires_at']) < pendulum.now():
    print("Token expired!")
    refresh_token()
    with open('strava_tokens.json') as check:
        token = json.load(check)

# print my activities from the current week
get_my_activities(token)
