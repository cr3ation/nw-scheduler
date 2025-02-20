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
        elif "ATTACK" in activity.name.upper():
            activity.imageurl = "/static/images/activities/attack_960x540.jpg"
        elif "DANCE" in activity.name.upper():
            activity.imageurl = "/static/images/activities/dance_960x540.jpg"
        elif "BODYBALANCE" in activity.name.upper():
            activity.imageurl = "/static/images/activities/bodybalance_960x540.jpg"
        elif "BODYPUMP" in activity.name.upper():
            activity.imageurl = "/static/images/activities/bodypump_960x540.jpg"
        elif "CORE" in activity.name.upper():
            activity.imageurl = "/static/images/activities/core-960x540.jpg"
        elif "CROSSCHALLENGE" in activity.name.upper():
            activity.imageurl = "/static/images/activities/crosschallenge_950x540.jpg"
        elif "GRIT" in activity.name.upper():
            activity.imageurl = "/static/images/activities/grit_960x540.jpg"
        elif "PILATES" in activity.name.upper():
            activity.imageurl = "/static/images/activities/pilates_960x540.jpg"
        elif "RPM" in activity.name.upper():
            activity.imageurl = "/static/images/activities/rpm_960x540.jpg"
        elif "SENIOR" in activity.name.upper():
            activity.imageurl = "/static/images/activities/senior_960x540.jpg"
        elif "SHAPES" in activity.name.upper():
            activity.imageurl = "/static/images/activities/shapes_960x540.jpg"
        elif "SPRINT" in activity.name.upper():
            activity.imageurl = "/static/images/activities/sprint_960x540.jpg"
        elif "STRENGTH DEVELOPMENT" in activity.name.upper():
            activity.imageurl = "/static/images/activities/strength-development_960x540.jpg"
        elif "THE TRIP" in activity.name.upper():
            activity.imageurl = "/static/images/activities/the_trip_960x540.jpg"
        elif "YOGA" in activity.name.upper():
            activity.imageurl = "/static/images/activities/yoga_960x540.jpg"
        elif "ZUMBA" in activity.name.upper():
            activity.imageurl = "/static/images/activities/zumba_960x540.jpg"
        else:
            activity.imageurl = "/static/images/activities/unicorn-dress-up-girls.jpg"
        activity.save()
