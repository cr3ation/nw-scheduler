from datetime import datetime
import requests
import time

api_url = "http://app:8000/scheduled"

# Nice looking output
def print_message(message):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S") # Use "%Y-%m-%d %H:%M:%S" to include date    
    print(f"[{current_time}] {message}")

# Wait for other services to start
time.sleep(5)

print("")
print("The next booking will be fetched every 10 min")
print("Booking request will occur same second as a booking opens")
print("Once a booking is completed, the next upcoming booking will be feched immediately")
print("")

while True:
    data = None

    # Fetch data
    try:
        response = requests.get(api_url)
        data = response.json()
    except Exception as err:
        print_message(f"Could not connect to {api_url} Retry in 10 sec.")
        time.sleep(10)

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
            booking = datetime.strptime(data["upcoming"]["BookingStartsAt"], "%Y-%m-%dT%H:%M:%SZ") #2022-02-05T10:00:00Z
            print_message(f"Upcoming: {data['upcoming']['Name']} ({data['upcoming']['Instructor']}). Booking starts at: {booking}.")
            # Check every second if booking is opened
            for i in range(600):
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
    except Exception as err:
        print(f"An exeption was thrown! {err}... Data: {data}")
        time.sleep(600)
