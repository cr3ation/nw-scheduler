from workers import task
from datetime import datetime, timedelta
from django.utils import timezone
from nordicwellness.models import Activity
import nordicwellness.nw

@task(schedule=60*20)
def check_new_activitites():
    update_database()

def update_database():
    """Fetch data from Nordic Wellness and adds/updates the local database"""

    # Try 10 times due to epic bad API
    for x in range(10):
        nw_activities = nordicwellness.nw.get_activities()["groupActivities"]
        if len(nw_activities) > 0:
            break

    for nw_activity in nw_activities:
        activity = None

        # Skip virtual activities. No one goes there anyway.
        if "Virtuell" in nw_activity["Instructor"]:
            continue

        if Activity.objects.filter(id=nw_activity["Id"]).exists():
            # at least one object satisfying query exists
            activity = Activity.objects.get(id=nw_activity["Id"])
        else:
            # no object satisfying query exists
            activity = Activity()
            activity.id = nw_activity["Id"]

        activity.bookingid = nw_activity["BookingId"]
        activity.description = nw_activity["Description"]
        activity.dropin = nw_activity["Dropin"]
        activity.dropsamount = nw_activity["DropsAmount"]
        activity.endtime = timezone.make_aware(
            datetime.strptime(nw_activity["EndTime"], "%Y-%m-%dT%H:%M:%S")
        )
        activity.freeslots = nw_activity["FreeSlots"]
        activity.instructor = nw_activity["Instructor"]
        activity.instructorid = nw_activity["InstructorId"]
        activity.imageurl = nw_activity["ImageUrl"]
        activity.location = nw_activity["Location"]
        activity.name = nw_activity["Name"]
        activity.message = nw_activity["Message"]
        activity.starttime = timezone.make_aware(
            datetime.strptime(nw_activity["StartTime"], "%Y-%m-%dT%H:%M:%S")
        )
        activity.status = nw_activity["Status"]
        activity.bookingstartsat = (
            timezone.make_aware(
                datetime.strptime(nw_activity["EndTime"], "%Y-%m-%dT%H:%M:%S")
                - timedelta(days=7)
                + timedelta(minutes=30)
            )
        )
        activity.bookingstartatstr = activity.bookingstartsat.strftime("%a %d %b. kl. %H.%M")
        activity.save()

        # Image
        if activity.imageurl:
            activity.imageurl = activity.imageurl
        elif "ATTACK" in activity.name:
            activity.imageurl = "https://lmimirror3pvr.azureedge.net/static/media/12222/131cbbdf-c082-4f2d-af26-a8a45c6737fc/bodycombat_960x540.jpg"
        elif "BODYPUMP" in activity.name:
            activity.imageurl = "https://lmimirror3pvr.azureedge.net/static/media/25639/0bed8d8f-43c5-4d22-95ae-2f4c2f93b8ca/bp-front-squat_960x540px.jpg"
        elif "BODYBALANCE" in activity.name:
            activity.imageurl = "https://henrikengstrom.com/images/nw-scheduler/bodybalance.jpeg"
        elif "CORE" in activity.name:
            activity.imageurl = "https://lesmillslegacypriv.blob.core.windows.net/media/1030/erin-maw-bicycle-crunch-960x540.jpg?width=500&height=281.25"
        elif "CROSSCHALLENGE" in activity.name:
            activity.imageurl = "https://henrikengstrom.com/images/nw-scheduler/crosschallenge.jpeg"
        elif "GRIT" in activity.name:
            activity.imageurl = "https://lmimirror3pvr.azureedge.net/static/media/10902/5bc08000-7331-4420-9b20-28f61222e3d2/grit-research-landing-page-960x540.jpg"
        elif "SPRINT" in activity.name:
            activity.imageurl = "https://lmimirror3pvr.azureedge.net/static/media/13934/2b5bde16-dc62-4728-93c9-92a36b048de2/all-you-need-to-know-about-sprint-960x540.jpg"
        elif "THE TRIP" in activity.name.upper():
            activity.imageurl = "https://www.traena.com/media/2027/the-trip-_960x540.jpg"
        elif "RPM" in activity.name.upper():
            activity.imageurl = "https://lmimirror3pvr.azureedge.net/static/media/12229/97637a47-286f-4e1f-85a8-f32596a73b35/rpm_960x540.jpg"
        elif "YOGA" in activity.name.upper():
            activity.imageurl = "https://media.sporthalsa.se/uploads/2018/03/yoga_meditation.jpg"
        elif "SENIOR" in activity.name.upper():
            activity.imageurl = "https://solvesborg.se/images/18.19ee726a174ba2ded9ad44/1600929634682/DSC09899-klar.jpg"
        elif "STRENGTH DEVELOPMENT" in activity.name.upper():
            activity.imageurl = "https://lmimirroralphapvr.azureedge.net/static/media/30679/19c59d47-c968-494b-984e-3840dabe50e2/erin-strength-development-960x540.jpg"
        elif "ZUMBA" in activity.name.upper():
            activity.imageurl = "https://henrikengstrom.com/images/nw-scheduler/zumba.jpeg"
        else:
            activity.imageurl = "https://henrikengstrom.com/images/unicorn-dress-up-girls.jpeg"
        activity.save()
