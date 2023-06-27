from unicodedata import name
from datetime import datetime, timedelta
from django import views
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from nordicwellness.models import Activity
from nordicwellness.tasks import check_new_activitites, update_database
import nordicwellness.config.settings as conf
import nordicwellness.nw
import nordicwellness.pushover as pushover


def get_activities():
    now = timezone.now()
    activities = Activity.objects.filter(starttime__gte = now).order_by("-starttime").exclude(name__contains="Virtual")
    #activities = Activity.objects.filter(starttime__gte = now).order_by("starttime")
    return activities


# Create your views here.
def index(request):
    # check_new_activitites()
    activities = get_activities()
    return render(request, "index.html", context={"activities": activities})


def command(request, id, cmd):
    activities = get_activities()
    for activity in activities:
        if id == activity.id:
            if cmd == "book":
                res = nordicwellness.nw.book_groupactivitiy(activity)
                if "Booked" in res:
                    activity.status = "Booked"
                    activity.save()
                    pushover.send(activity)
            if cmd == "schedule" or cmd == "unschedule":
                # DO STUFF
                activity.scheduledbooking = not activity.scheduledbooking
                activity.save()
    return redirect("/")


def scheduled(request):
    # Find scheduled bookings
    now = timezone.make_aware(datetime.now())
    activity = Activity.objects.filter(scheduledbooking=True, bookingstartsat__lt = now).order_by("starttime").exclude(status="Booked").first()

    # Nothing to do
    if not activity:
        activity = Activity.objects.filter(scheduledbooking=True).order_by("starttime").exclude(status="Booked").first()
        if activity:
            return JsonResponse({'message' : 'Nothing to do', 
                                'upcoming': { 
                                    'Name': activity.name, 
                                    'Instructor': activity.instructor, 
                                    'BookingStartsAt' : activity.bookingstartsat.astimezone(timezone.get_current_timezone()).isoformat() } 
                                })
        else:
            return JsonResponse({'message' : 'No scheduled bookings'})

    # Book activity
    if now > activity.bookingstartsat:
        res = nordicwellness.nw.book_groupactivitiy(activity)
        if "Booked" in res:
            activity.status = "Booked"
            activity.scheduledbooking = False
            activity.save()
            pushover.send(activity)
        return JsonResponse({'Name': activity.name , 'Response' : res })
    return JsonResponse({'message': 'Something went wrong with scheduled booking.' })


def fetch(request):
    """Update local database with new data from Nordic Wellness API"""
    update_database()
    return redirect("/")
    