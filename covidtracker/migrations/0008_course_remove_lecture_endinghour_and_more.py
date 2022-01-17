# Generated by Django 4.0 on 2022-01-05 14:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('covidtracker', '0007_alter_lecture_endinghour_alter_lecture_startinghour'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('startingHour', models.TimeField(verbose_name='Starting Hour')),
                ('endingHour', models.TimeField(verbose_name='Ending Hour')),
                ('lesson', models.CharField(max_length=40)),
            ],
        ),
        migrations.RemoveField(
            model_name='lecture',
            name='endingHour',
        ),
        migrations.RemoveField(
            model_name='lecture',
            name='lesson',
        ),
        migrations.RemoveField(
            model_name='lecture',
            name='startingHour',
        ),
        migrations.AddField(
            model_name='lecture',
            name='course',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='covidtracker.course'),
            preserve_default=False,
        ),
    ]
