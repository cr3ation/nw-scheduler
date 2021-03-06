# Generated by Django 4.0.1 on 2022-02-02 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nordicwellness', '0006_remove_activity_color'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='bookingid',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='activity',
            name='description',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='activity',
            name='message',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
