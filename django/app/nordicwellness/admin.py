from django.contrib import admin
from nordicwellness.models import Activity

# Register your models here.
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'status', 'freeslots', 'bookingid', 'scheduledbooking', 'starttime')
    ordering = ('-starttime',)


admin.site.register(Activity, ActivityAdmin)