from django.db import models
from django.utils import timezone
from datetime import datetime, timedelta


# Create your models here.
class Activity(models.Model):
    id = models.IntegerField(primary_key=True)
    bookingid = models.IntegerField(null=True, blank=True)
    bookingstartsat = models.DateTimeField(null=True)
    bookingstartatstr = models.CharField(null=True, max_length=50)
    description = models.CharField(null=True, blank=True, max_length=500)
    dropin = models.IntegerField()
    dropsamount = models.IntegerField()
    endtime = models.DateTimeField()
    freeslots = models.BigIntegerField()
    instructor = models.CharField(max_length=100)
    instructorid = models.IntegerField()
    imageurl = models.CharField(null=True, blank=True, max_length=1024)
    location = models.CharField(max_length=50)
    message = models.CharField(null=True, blank=True, max_length=500)
    name = models.CharField(max_length=100)
    scheduledbooking = models.BooleanField(default=False) 
    status = models.CharField(max_length=50) # Status: Unavailable, Reserved, Booked, Bookable
    starttime = models.DateTimeField()

    def __str__(self):
        return self.name

    @property
    def color(self):
        # Color
        if "Reserved" in self.status:
            return "orange"
        elif "Booked" in self.status:
            return "green"
        elif self.freeslots <= 0:
            return "red"
        elif self.scheduledbooking:
            return "silver"
        else:
            return "white"

    @property
    def booking_started(self):
        """True if booking has started. Else False."""
        now = timezone.make_aware(datetime.now())
        # now = timezone.now()
        booking_opens = self.endtime.astimezone(timezone.get_current_timezone())
        booking_opens = booking_opens - timedelta(days=7) + timedelta(minutes=30)
        #booking_opens = timezone.make_aware(self.endtime) - timedelta(days=7) + timedelta(minutes=30)
        return now > booking_opens

    @property
    def start_time_str(self):
        starttime = self.starttime.astimezone(timezone.get_current_timezone())
        return starttime.strftime("%a %d %b. kl. %H.%M")
    #    return self.starttime.strftime("%a %d %b. kl. %H.%M")
    



# Status: Unavailable, Reserved, Booked, Bookable
