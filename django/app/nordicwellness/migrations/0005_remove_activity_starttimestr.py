# Generated by Django 4.0.1 on 2022-01-30 17:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nordicwellness', '0004_activity_bookingstartatstr'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activity',
            name='starttimestr',
        ),
    ]