from django.db import models
from django.conf import settings

class Amphitheater(models.Model):
    name=models.CharField(max_length=40,verbose_name='Ονομα')
    capacity=models.IntegerField(verbose_name='Χωρητικότητα')
    floor=models.IntegerField(verbose_name='Οροφος')

    class Meta:
        verbose_name='Αμφιθέατρο'
        verbose_name_plural='Αμφιθέατρα'

    def __str__(self):
        return self.name

class Course(models.Model):
    startingHour=models.TimeField(verbose_name="Ωρα έναρξης")
    endingHour=models.TimeField(verbose_name="Ωρα λήξης")
    professor=models.CharField(max_length=40,verbose_name='Καθηγητής')
    lesson=models.CharField(max_length=40,verbose_name='Μάθημα')
    lessonType=models.CharField(verbose_name='Τύπος μαθήματος',
      choices=(('Υποχρεωτικό','Υποχρεωτικό'),('Επιλογής','Επιλογής')),max_length=30)
    amphitheater=models.ForeignKey(Amphitheater,on_delete=models.CASCADE,verbose_name='Αμφιθέατρο')

    class Meta:
        verbose_name='Στοιχεία διάλεξης (χωρίς ημερομηνία)'
        verbose_name_plural='Στοιχεία διαλέξεων (χωρίς ημερομηνία)'

    def __str__(self):
        return self.lesson

class Lecture(models.Model):
    date=models.DateField(verbose_name='Ημερομηνία')
    course=models.ForeignKey(Course,on_delete=models.CASCADE,verbose_name='Μάθημα')

    class Meta:
        verbose_name='Ημερομηνία διάλεξης'
        verbose_name_plural='Ημερομηνία διαλέξεων'

    def __str__(self):
        return 'Μάθημα: '+self.course.lesson+' Ημερομηνία:'+str(self.date)

class Position(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,verbose_name='Αριθμός μητρώου')
    lecture=models.ForeignKey(Lecture,on_delete=models.CASCADE,verbose_name='Στοιχεία διάλεξης')
    positionNumber=models.CharField(max_length=40,verbose_name='Αριθμός θέσης')

    class Meta:
        verbose_name='Θέση φοιτητή'
        verbose_name_plural='Θέσεις φοιτητών'

    def __str__(self) -> str:
        return 'Στοιχεία διάλεξης: '+str(self.lecture)+' ΑΜ:'+self.user.username+' Θέση:'+str(self.positionNumber)

class CovidCase(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,verbose_name='Αριθμός μητρώου')
    date=models.DateField(verbose_name='Ημερομηνία')

    class Meta:
        verbose_name='Κρούσμα'
        verbose_name_plural='Κρούσματα'

    def __str__(self):
        return 'Αριθμός μητρώου: '+str(self.user.username)+' Ημερομηνία διάγνωσης: '+str(self.date)