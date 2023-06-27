from datetime import datetime, timezone
import requests
import time

api_url = "http://app:8000/scheduled"

# Nice looking output
def print_message(message):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")  # Use "%Y-%m-%d %H:%M:%S" to include date
    print(f"[{current_time}] {message}")


# Wait for other services to start
time.sleep(5)

print("")
print("The next booking will be fetched every 10 min")
print("Booking request will occur the same second as a booking opens")
print("Once a booking is completed, the next upcoming booking will be fetched immediately")
print("")

while True:
    data = None

    # Fetch data
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an exception for non-2xx response status codes
        data = response.json()
    except requests.exceptions.RequestException as err:
        print_message(f"An error occurred while connecting to {api_url}: {err}. Retry in 10 sec.")
        time.sleep(10)
        continue
    except ValueError as err:
        print_message(f"Failed to parse response data from {api_url}: {err}. Retry in 10 sec.")
        time.sleep(10)
        continue

    try:
        # Wait and retry if no data returned
        if not data:
            print_message(f"{api_url} did not return any data. Retry in 10 sec.")
            time.sleep(10)
            continue

        # Wait and retry if no scheduled bookings
        elif "No scheduled bookings" in data["message"]:
            print_message("No scheduled bookings. Refresh in 10 min...")
            time.sleep(600)
            continue

        # Upcoming bookings exist
        elif data["upcoming"]:
            # Parse the booking datetime string and make it offset-naive
            booking = datetime.strptime(data["upcoming"]["BookingStartsAt"], "%Y-%m-%dT%H:%M:%S%z").replace(tzinfo=None)
            print_message(f"Upcoming: {data['upcoming']['Name']} ({data['upcoming']['Instructor']}). Booking starts at: {booking}.")

            # Check every second if booking is opened
            for i in range(600):
                # Get the current time as an offset-naive datetime
                now = datetime.now()
                # print_message(f"Now: {now}   |   Booking start: {booking}")

                # Opened!
                if now > booking:
                    try:
                        response = requests.get(api_url)
                        response.raise_for_status()  # Raise an exception for non-2xx response status codes
                        data = response.text
                        print_message(data)
                        if "Booked" in data:
                            break
                    except requests.exceptions.RequestException as err:
                        print_message(f"An error occurred while connecting to {api_url}: {err}. Retry in 10 sec.")
                        time.sleep(10)
                        break
                    except ValueError as err:
                        print_message(f"Failed to parse response data from {api_url}: {err}. Retry in 10 sec.")
                        time.sleep(10)
                        break
                time.sleep(1)
    except Exception as err:
        print(f"An exception was thrown! {err}... Data: {data}")
        time.sleep(600)
