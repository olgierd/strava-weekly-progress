# Your last week on Strava in Python3

It is a simple `python3` script to fetch a list of your recent activities from your Strava account using API. I'm planning to use it with some kind of microcontroller, to show my progress in a weekly training plan.

## Usage

Assuming you have correctly created an API application in your Strava profile, you need to visit:

`https://www.strava.com/oauth/authorize?client_id=12345&response_type=code&redirect_uri=http://localhost/&approval_prompt=force&scope=activity:read_all`

replacing `12345` with your actual Cient ID. You will be redirected to a similar URL:

`http://localhost/?state=&code=0123abcd&scope=read,activity:read_all`

Save the `code` parameter for later.

Copy `secrets.json_sample` file to `secrets.json` and modify it. `client_id` and `client_secret` are displayed on API application webpage, `code` is the one you obtained from URL above.

Now, just run `./strava.py` and it should list all of your activities form the last week. Feel free to use the data in whatever way you like.
