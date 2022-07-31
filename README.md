# Rain Notifier

Frequently checks the weather and sends a notification to your favourite
services [(using Apprise](https://github.com/caronc/apprise)) when it's about to start
raining.

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
over the next 10 minutes.  If no rain is detected in this window, or the
probability of rain is below a given threshold (e.g. 40%), it goes to sleep for
10 minutes and repeats forever.

If rain is detected, a notification is sent to the list of Apprise services.
It'll look something like this:
> **Rain starting in 6 minutes**
>
> Duration: 40 minutes
>
> Probability: 55% chance

It'll then check when the rain is expected to stop, and go to sleep until then.
For example, if rain is starting in 6 minutes and expected to stop 40 minutes
later, the program will stop checking for rain for 40 minutes.
