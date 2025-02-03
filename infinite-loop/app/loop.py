from datetime import datetime, timezone
import requests
import time

api_url = "http://app:8000/scheduled"
fetch_api_url = "http://app:8000/fetch"
last_fetch_time = time.time()

# Nice looking output
def print_message(message):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")  # Use "%Y-%m-%d %H:%M:%S" to include date
    print(f"[{current_time}] {message}")


# Wait for other services to start
time.sleep(10)

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

    # Fetch new data from Nordic Wellness every 30 minutes
    if time.time() - last_fetch_time >= 1800:
        try:
            fetch_response = requests.get(fetch_api_url)
            fetch_response.raise_for_status()
            print_message(f"Fetched data from {fetch_api_url}: {fetch_response.text}")
            last_fetch_time = time.time()
        except requests.exceptions.RequestException as err:
            print_message(f"An error occurred while connecting to {fetch_api_url}: {err}. Retry in 30 min.")
        except ValueError as err:
            print_message(f"Failed to parse response data from {fetch_api_url}: {err}. Retry in 30 min.")

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

            # Check if now is less than 10 minutes until booking starts
            if (booking - datetime.now()).total_seconds() <= 600:
                print_message("Less than 10 minutes until booking starts. Checking every second if the booking has opened...")
                # Check every second if booking is opened for 10 minutes
                for i in range(600):
                    now = datetime.now()
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
            else:
                time.sleep(600)
                continue
    except Exception as err:
        print(f"An exception was thrown! {err}... Data: {data}")
        time.sleep(600)
