from datetime import datetime
import requests
import time

api_url = "http://app:8000/scheduled"

# Nice looking output
def print_message(message):
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{current_time}] {message}")

# Wait for other services to start
time.sleep(5)

while True:
    data = None

    # Fetch data
    try:
        response = requests.get(api_url)
        data = response.json()
    except Exception as err:
        print_message(f"Could not connect to {api_url} Retry in 10 sec.")
        time.sleep(10)

    # Wait and retry if no data returned
    if not data:
        print_message(f"{api_url} did not return any data. Retry in 10 sec.")
        time.sleep(10)
        continue

    # Wait and retry if no scheduled bookings
    elif "No scheduled bookings" in data["message"]:
        print_message("No scheduled bookings. Refresh in 5 min...")
        time.sleep(300)
        continue

    # Upcoming bookings exist
    elif data["upcoming"]:
        booking = datetime.strptime(data["upcoming"]["BookingStartsAt"], "%Y-%m-%dT%H:%M:%SZ") #2022-02-05T10:00:00Z
        print_message("Upcoming: {0} ({1}). Booking starts at: {2}. Refresh in 5 min...".format(data["upcoming"]["Name"], data["upcoming"]["Instructor"], booking))
        # Check every second if booking is opened
        for i in range(300):
            now = datetime.now()
            # Openened!
            if now > booking:
                response = requests.get(api_url)
                data = response.text
                print_message(data)
                # 
                if "Booked" in data:
                    break
            time.sleep(1)
