import re
from django.db import models
from django.conf import settings

class Amphitheater(models.Model):
    name=models.CharField(max_length=40)
    capacity=models.IntegerField()
    floor=models.IntegerField()

    def __str__(self):
        return self.name

class Course(models.Model):
    startingHour=models.TimeField(verbose_name="Starting Hour")
    endingHour=models.TimeField(verbose_name="Ending Hour")
    lesson=models.CharField(max_length=40)
    amphitheater=models.ForeignKey(Amphitheater,on_delete=models.CASCADE)

    def __str__(self):
        return self.lesson

class Lecture(models.Model):
    date=models.DateField()
    course=models.ForeignKey(Course,on_delete=models.CASCADE)

    def __str__(self):
        return self.course.lesson+' '+str(self.date)

class Position(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    lecture=models.ForeignKey(Lecture,on_delete=models.CASCADE)
    positionNumber=models.IntegerField()

class CovidCase(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    date=models.DateField()

    def __str__(self):
        return 'Αριθμός μητρώου φοιτητή: '+str(self.user.username)+' Ημερομηνία διάγνωσης: '+str(self.date)