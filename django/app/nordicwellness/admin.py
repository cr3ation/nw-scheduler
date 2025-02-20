from django.contrib import admin
from nordicwellness.models import Activity

# Register your models here.
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'status', 'freeslots', 'bookingid', 'scheduledbooking', 'starttime')
    ordering = ('-starttime',)


admin.site.site_header = "Nordic Wellness Scheduler Admin"
admin.site.site_title = "Nordic Wellness Scheduler Admin Portal"
admin.site.index_title = "Welcome to Nordic Wellness Scheduler Admin"
admin.site.register(Activity, ActivityAdmin)
