import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Amphitheater, Course, CovidCase, Lecture, Position


class TrackerWorkflowTests(TestCase):
    def setUp(self):
        self.user=get_user_model().objects.create_user(username='student',password='secret-pass')
        self.other_user=get_user_model().objects.create_user(username='other',password='secret-pass')
        self.amphitheater=Amphitheater.objects.create(name='A1',capacity=2,floor=1)
        self.course=Course.objects.create(
            startingHour=datetime.time(9,0),
            endingHour=datetime.time(11,0),
            professor='Professor',
            lesson='Django',
            lessonType='Υποχρεωτικό',
            amphitheater=self.amphitheater,
        )
        self.lecture=Lecture.objects.create(date=datetime.date.today(),course=self.course)

    def test_login_success_redirects_home(self):
        response=self.client.post(reverse('login'),{'username':'student','password':'secret-pass'})

        self.assertRedirects(response,reverse('home'))

    def test_login_failure_shows_generic_error(self):
        response=self.client.post(reverse('login'),{'username':'student','password':'wrong'},follow=True)

        self.assertContains(response,'Invalid username or password.')

    def test_user_can_book_valid_position(self):
        self.client.force_login(self.user)

        response=self.client.post(reverse('add_position',args=[self.lecture.id]),{'positionNumber':'1'})

        self.assertRedirects(response,reverse('home'))
        self.assertTrue(Position.objects.filter(user=self.user,lecture=self.lecture,positionNumber='1').exists())

    def test_user_cannot_book_same_lecture_twice(self):
        Position.objects.create(user=self.user,lecture=self.lecture,positionNumber='1')
        self.client.force_login(self.user)

        response=self.client.post(reverse('add_position',args=[self.lecture.id]),{'positionNumber':'2'},follow=True)

        self.assertContains(response,'Εχετε ήδη δηλώσει την θέση σας.')
        self.assertEqual(Position.objects.filter(user=self.user,lecture=self.lecture).count(),1)

    def test_user_cannot_book_taken_position(self):
        Position.objects.create(user=self.other_user,lecture=self.lecture,positionNumber='1')
        self.client.force_login(self.user)

        response=self.client.post(reverse('add_position',args=[self.lecture.id]),{'positionNumber':'1'},follow=True)

        self.assertContains(response,'Η θέση είναι πιασμένη.')
        self.assertFalse(Position.objects.filter(user=self.user,lecture=self.lecture).exists())

    def test_user_cannot_book_position_outside_capacity(self):
        self.client.force_login(self.user)

        response=self.client.post(reverse('add_position',args=[self.lecture.id]),{'positionNumber':'3'},follow=True)

        self.assertContains(response,'Η θέση είναι εκτός χωρητικότητας αίθουσας.')
        self.assertFalse(Position.objects.filter(user=self.user,lecture=self.lecture).exists())

    def test_user_cannot_book_non_numeric_position(self):
        self.client.force_login(self.user)

        response=self.client.post(reverse('add_position',args=[self.lecture.id]),{'positionNumber':'abc'},follow=True)

        self.assertContains(response,'Ο αριθμός θέσης πρέπει να είναι θετικός αριθμός.')
        self.assertFalse(Position.objects.filter(user=self.user,lecture=self.lecture).exists())

    def test_user_can_report_covid_case_once_per_date(self):
        self.client.force_login(self.user)
        date='2026-05-01'

        first_response=self.client.post(reverse('covid_add'),{'date':date})
        second_response=self.client.post(reverse('covid_add'),{'date':date},follow=True)

        self.assertRedirects(first_response,reverse('home'))
        self.assertContains(second_response,'Εχετε ήδη δηλώσει κρούσμα για αυτή την ημερομηνία.')
        self.assertEqual(CovidCase.objects.filter(user=self.user,date=date).count(),1)
