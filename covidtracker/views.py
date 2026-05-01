from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
import datetime

from .models import CovidCase, Lecture, Position

def home(request):
    if request.user.is_authenticated:
        lecture=Lecture.objects.filter(date=datetime.date.today()).select_related('course__amphitheater')
        return render(request,'dashboard.html',{"page":"home","lecture":lecture})
    return render(request,'login.html')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('home')
        messages.error(request,'Invalid username or password.')

    return render(request,'login.html')

@login_required
def logout_view(request):
    auth.logout(request)
    return redirect('home')

@login_required
def show(request):
    position=Position.objects.filter(user=request.user).select_related('lecture__course__amphitheater')
    return render(request,'dashboard.html',{"page":"show",'position':position})

@login_required    
def lecture_detail(request,id):
    lecture=get_object_or_404(Lecture.objects.select_related('course__amphitheater'),id=id)
    return render(request,'dashboard.html',{"page":"position","lecture":[lecture],"lecture_obj":lecture})

@login_required
def add_position(request,id):
    lecture=get_object_or_404(Lecture.objects.select_related('course__amphitheater'),id=id)
    if request.method!='POST':
        return redirect('home')

    position_number=request.POST.get('positionNumber','').strip()
    if not position_number.isdigit():
        messages.error(request,'Ο αριθμός θέσης πρέπει να είναι θετικός αριθμός.')
        return redirect('lecture_detail',id=lecture.id)

    position_number=str(int(position_number))
    if int(position_number)>lecture.course.amphitheater.capacity:
        messages.error(request,'Η θέση είναι εκτός χωρητικότητας αίθουσας.')
        return redirect('lecture_detail',id=lecture.id)

    if Position.objects.filter(user=request.user,lecture=lecture).exists():
        messages.error(request,'Εχετε ήδη δηλώσει την θέση σας.')
        return redirect('lecture_detail',id=lecture.id)

    if Position.objects.filter(lecture=lecture,positionNumber=position_number).exists():
        messages.error(request,'Η θέση είναι πιασμένη.')
        return redirect('lecture_detail',id=lecture.id)

    Position.objects.create(user=request.user,lecture=lecture,positionNumber=position_number)
    messages.success(request,'Η θέση σας δηλώθηκε επιτυχώς.')
    return redirect('home')

@login_required
def covid(request):
    return render(request,'dashboard.html',{"page":"covid"})

@login_required
def covid_add(request):
    if request.method!='POST':
        return redirect('home')

    date=request.POST['date']
    if CovidCase.objects.filter(user=request.user,date=date).exists():
        messages.error(request,'Εχετε ήδη δηλώσει κρούσμα για αυτή την ημερομηνία.')
        return redirect('covid')

    CovidCase.objects.create(user=request.user,date=date)
    messages.success(request,'Το κρούσμα δηλώθηκε επιτυχώς.')
    return redirect('home')
