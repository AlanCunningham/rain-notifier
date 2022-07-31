import settings
import apprise
import requests
import time
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def get_weather():
    """
    Fetches the weather from an API
    """
    latitude = settings.latitude
    longitude = settings.longitude
    weather_endpoint = settings.endpoint
    api_key = settings.api_key
    request_url = f"{weather_endpoint}/{api_key}/{latitude},{longitude}"
    payload = {"units": settings.units}
    weather_data = requests.get(request_url, params=payload).json()
    return weather_data


def main():
    # Create an Apprise instance
    app = apprise.Apprise()

    for service in settings.apprise_services:
        app.add(service)

    check_for_weather = True
    # The threshold to decide whether rain is forecast
    rain_chance_threshold = 0.25
    # Prevent notifications if it's still raining
    is_still_raining = False

    while check_for_weather:
        # Sleep for 10 minutes between each check
        interval_secs = 600
        is_rain_forecast = False
        # Retrieve weather for the next 10 minutes
        minutely_weather = get_weather()["minutely"]
        minutely_weather_data = minutely_weather["data"]
        next_ten_minutes = minutely_weather_data[:10]

        # Find out when rain is starting
        for index, minute in enumerate(next_ten_minutes):
            print(minute)

            # If debugging is True, force rain to start in 5 minutes
            if settings.debug:
                if index == 5:
                    minute["precipProbability"] = 0.7

            if minute["precipProbability"] > rain_chance_threshold:
                is_rain_forecast = True
                rain_starting_index = index
                break

        if not is_rain_forecast:
            # Reset the is_still_raining variable so we notify next time
            # it starts raining
            is_still_raining = False
        else:
            # Check if it's still raining - if it is, don't resend the
            # notification
            if is_still_raining:
                print("It's still raining - don't send another notification")
            else:
                # Create the minutely rain graph
                minute_list = []
                rain_chance_list = []
                number_of_minutes = 60
                for index, minute in enumerate(minutely_weather_data):
                    if index == number_of_minutes:
                        break
                    minute_list.append(index)
                    rain_chance_list.append(minute["precipProbability"] * 100)

                # Plot the graph
                plt.figure()
                plt.grid()
                plt.ylim(0, 100)
                plt.xlim(0, number_of_minutes)
                plt.plot(minute_list, rain_chance_list, linewidth=3.0)
                plt.savefig("rain_graph.png")

                # Find out when the rain is stopping
                # Default rain_stopping_index - if this remains unchanged, then
                # assume it's going to rain for the hour
                rain_stopping_index = len(minutely_weather_data) - 1
                for index, minute in enumerate(
                    minutely_weather_data[rain_starting_index:]
                ):

                    # If debugging is True, force rain to stop in 15 minutes
                    if settings.debug:
                        if index < 20:
                            minute["precipProbability"] = 0.7
                        else:
                            minute["precipProbability"] = 0.3

                    if minute["precipProbability"] < rain_chance_threshold:
                        rain_stopping_index = index
                        break

                rain_starting = minutely_weather_data[rain_starting_index]
                rain_starting_datetime = datetime.fromtimestamp(rain_starting["time"])
                rain_starting_time_difference = rain_starting_datetime - datetime.now()
                rain_starting_time_difference_mins = int(
                    rain_starting_time_difference.total_seconds() // 60
                )

                rain_stopping = minutely_weather_data[rain_stopping_index]
                rain_stopping_datetime = datetime.fromtimestamp(rain_stopping["time"])
                rain_stopping_time_difference = (
                    rain_stopping_datetime - rain_starting_datetime
                )
                rain_stopping_time_difference_mins = int(
                    rain_stopping_time_difference.total_seconds() // 60
                )

                # Set the probability to a readable percentage
                rain_probability = int(rain_starting["precipProbability"] * 100)

                # precipType isn't always provided from DarkSky. Default to "rain"
                # if it's not in the response.
                if "precipType" in rain_starting:
                    precipitation_type = rain_starting["precipType"].title()
                else:
                    precipitation_type = "Rain"

                # Build the message
                app_title = f"{precipitation_type} starting in {rain_starting_time_difference_mins} minutes"
                app_message_lines = [
                    f"Duration: {rain_stopping_time_difference_mins} minutes",
                    f"Probabiity: {rain_probability}%",
                    f"{minutely_weather['summary']}",
                ]
                app_message = "\n".join(app_message_lines)
                print(f"{app_title}\n{app_message}")

                # Send the message to the Apprise services
                app.notify(body=app_message, title=app_title, attach="rain_graph.png")

                # Set so we don't send duplicate notification for every 10
                # minutes
                is_still_raining = True

        # Go to sleep for 10 minutes
        interval_secs = 600
        interval_mins = interval_secs // 60
        print(f"Sleeping for {interval_secs} seconds ({interval_mins} minutes)")
        time.sleep(interval_secs)


if __name__ == "__main__":
    main()
