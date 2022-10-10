# Rain Notifier

Frequently checks the weather and sends a notification to your favourite
services [(using Apprise](https://github.com/caronc/apprise)) when it's about to start
raining.

![rain_1](https://user-images.githubusercontent.com/9663408/194845544-17292f9b-a71f-4780-9ee6-ae1fc97f36df.jpg)

☔ **This project requires a Dark Sky developer account.  Dark Sky will be
shutting down at some point and they aren't accepting new sign ups. When that
happens, I'll probably port this project to another weather source.**

## Hardware
- Personally, I have this running on a Raspberry Pi (any model should do)

## Installation
- Create a python3 virtual environment and install the project's requirements:
```
$ python3 -m venv rain_notifier_venv
$ source rain_notifier_venv/bin/activate
(rain_notifier_venv) $ pip install -r requirements.txt
```
- Open settings.py and enter your:
  - Your Dark Sky API key
  - Latitude
  - Longitude
  - Preferred units of measurement

Units of measurement options, from https://darksky.net/dev/docs:
``` 
auto: automatically select units based on geographic location
ca: same as si, except that windSpeed is in kilometers per hour
uk2: same as si, except that nearestStormDistance and visibility are in miles and windSpeed is in miles per hour
us: Imperial units (the default)
si: SI units
```
- Also in settings.py, enter where you want your notifications to be sent. See
[Apprise's github page](https://github.com/caronc/apprise) for examples. An
example for Telegram and Discord would look something like this:
```
# The list of services to notify
apprise_services = [
    "tgram://bottoken/ChatID",
    "discord://webhook_id/webhook_token",
]
```
- You should now be able to start the program:
```
(rain_notifier_venv) $ python main.py
```

# Checking for rain
By default, the program checks for rain every 10 minutes, looking at each minute
over the next 10 minutes.

If rain is detected in this window, a notification is sent to the list of Apprise services.
It'll look something like this:
> **Rain starting in 11 minutes**
>
> Duration: 8 minutes
>
> Probability: 27% chance
>
> ![rain_2](https://user-images.githubusercontent.com/9663408/194845711-3d8f5795-de5b-47f1-91ef-3b5280b94127.jpg)

You might notice the first notification doesn't always match the DarkSky summary in the graph.  While it's mostly similar, the DarkSky summary is likely to be more accurate.
