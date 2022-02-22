# Generated by Django 4.0 on 2021-12-27 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('covidtracker', '0004_rename_endinghour_lecture_hour_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lecture',
            name='hour',
        ),
        migrations.AddField(
            model_name='lecture',
            name='endingHour',
            field=models.TimeField(default='00:00'),
        ),
        migrations.AddField(
            model_name='lecture',
            name='startingHour',
            field=models.TimeField(default='00:00'),
        ),
    ]