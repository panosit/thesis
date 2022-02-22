# Generated by Django 4.0.2 on 2022-02-21 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('covidtracker', '0010_course_lessontype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='lessonType',
            field=models.CharField(choices=[('1', 'Υποχρεωτικό'), ('2', 'Επιλογής')], max_length=30, verbose_name='Τύπος μαθήματος'),
        ),
    ]