#!/usr/bin/python3

import requests
import json
import pendulum
import os

# GLOBAL SETTINGS
token_file = 'strava_tokens.json'
secret_file = 'secrets.json'
auth_url = 'https://www.strava.com/api/v3/oauth/token'


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

    total_km = 0
    total_mtime = 0

    # list activities from this week only
    for day in range(6):
        day_act = [a for a in activities if
                   pendulum.parse(a['start_date']) > sow.add(days=day) and
                   pendulum.parse(a['start_date']) < sow.add(days=day+1)]

        day_name = sow.add(days=day).format('ddd DD/MM')

        day_mtime = round(sum([int(act['moving_time'])/60 for act in day_act]))
        day_km = round(sum([int(act['distance'])/1000 for act in day_act]), 1)
        print(f"{day_name:9} → {day_mtime:3} min → {day_km:5} km")

        total_mtime += day_mtime
        total_km += day_km

    print('-' * 30)
    print(f"{'TOTAL':^9} → {total_mtime:>3} min → {total_km:>5} km")


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
    refresh_token(secrets, token)
    with open('strava_tokens.json') as check:
        token = json.load(check)

# print my activities from the current week
get_my_activities(token)
