# Generated by Django 4.0 on 2021-12-27 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('covidtracker', '0005_remove_lecture_hour_lecture_endinghour_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lecture',
            name='endingHour',
            field=models.TimeField(),
        ),
        migrations.AlterField(
            model_name='lecture',
            name='startingHour',
            field=models.TimeField(),
        ),
    ]