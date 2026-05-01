from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required
import covidtracker.models
import datetime


def home(request):
    user = request.user
    if user.is_authenticated is True:
        lecture = covidtracker.models.Lecture.objects.filter(date=datetime.date.today())
        position = covidtracker.models.Position.objects.filter(user=user)
        return render(
            request,
            'index.html',
            {
                'user': user.username,
                'lecture': lecture,
                'position': position,
                'view': 'home',
            },
        )
    return render(request, 'login.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        return render(request, 'login.html', {'result': 'Wrong Password or Username!'})

    user = request.user
    if user.is_authenticated is True:
        return redirect('/')
    return render(request, 'login.html')


@login_required
def logout(request):
    auth.logout(request)
    return redirect('/')


@login_required
def show(request):
    user = request.user
    lecture = covidtracker.models.Lecture.objects.filter(date=datetime.date.today())
    position = covidtracker.models.Position.objects.filter(user=user)
    return render(
        request,
        'index.html',
        {
            'user': user.username,
            'lecture': lecture,
            'position': position,
            'view': 'show',
        },
    )


@login_required
def lecture(request, id):
    user = request.user
    lecture = covidtracker.models.Lecture.objects.filter(date=datetime.date.today())
    selected_lecture = covidtracker.models.Lecture.objects.filter(id=id)
    position = covidtracker.models.Position.objects.filter(user=user)
    return render(
        request,
        'index.html',
        {
            'user': user.username,
            'lecture': lecture,
            'selected_lecture': selected_lecture,
            'position': position,
            'view': 'lecture',
        },
    )


@login_required
def add(request, id):
    lecture = covidtracker.models.Lecture.objects.get(id=id)
    if request.method == 'POST':
        positionNumber = request.POST['positionNumber']
        user = request.user
        if covidtracker.models.Position.objects.filter(user=user, lecture=lecture).exists():
            return _render_lecture_with_message(request, user, id, 'Εχετε ήδη δηλώσει την θέση σας')
        if covidtracker.models.Position.objects.filter(lecture=lecture, positionNumber=positionNumber).exists():
            return _render_lecture_with_message(request, user, id, 'Η θέση είναι πιασμένη')

        covidtracker.models.Position(user=user, lecture=lecture, positionNumber=positionNumber).save()
        return redirect('/')
    return redirect('/')


@login_required
def covid(request):
    user = request.user
    lecture = covidtracker.models.Lecture.objects.filter(date=datetime.date.today())
    position = covidtracker.models.Position.objects.filter(user=user)
    return render(
        request,
        'index.html',
        {
            'user': user.username,
            'lecture': lecture,
            'position': position,
            'view': 'covid',
        },
    )


@login_required
def covidAdd(request):
    user = request.user
    if request.method == 'POST':
        date = request.POST['date']
        covidtracker.models.CovidCase(user=user, date=date).save()
        return redirect('/')
    return redirect('/')


def _render_lecture_with_message(request, user, lecture_id, result):
    lecture = covidtracker.models.Lecture.objects.filter(date=datetime.date.today())
    selected_lecture = covidtracker.models.Lecture.objects.filter(id=lecture_id)
    position = covidtracker.models.Position.objects.filter(user=user)
    return render(
        request,
        'index.html',
        {
            'user': user.username,
            'lecture': lecture,
            'selected_lecture': selected_lecture,
            'position': position,
            'result': result,
            'view': 'lecture',
        },
    )
