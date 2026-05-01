from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('covidtracker', '0014_alter_position_positionnumber'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='position',
            constraint=models.UniqueConstraint(fields=('user', 'lecture'), name='unique_user_lecture_position'),
        ),
        migrations.AddConstraint(
            model_name='position',
            constraint=models.UniqueConstraint(fields=('lecture', 'positionNumber'), name='unique_lecture_position_number'),
        ),
        migrations.AddConstraint(
            model_name='covidcase',
            constraint=models.UniqueConstraint(fields=('user', 'date'), name='unique_user_covid_case_date'),
        ),
    ]
