from django.shortcuts import render,redirect
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required
import covidtracker.models
import datetime

def home(request):
    user=request.user
    if user.is_authenticated==True:
        lecture=covidtracker.models.Lecture.objects.filter(date=datetime.date.today())
        return render(request,'index.html',{"user":user.username,"lecture":lecture})
    else:
        return render(request,'login.html')

def login(request):
    if(request.method=='POST'):
       username=request.POST['username']
       password=request.POST['password']
       user=auth.authenticate(username=username,password=password)
       if(user is not None):
           auth.login(request,user)
           return redirect('/')
       else:
           return render(request,'login.html',{'result':"Wrong Password or Username!"})
    else:
        user=request.user
        if user.is_authenticated==True:
           return redirect('/')
        else:
           return render(request,'login.html')

@login_required
def logout(request):
    auth.logout(request)
    return redirect('/')

@login_required
def show(request):
    user=request.user
    position=covidtracker.models.Position.objects.filter(user=user)
    return render(request,'show.html',{'position':position})

@login_required    
def lecture(request,id):
    lecture=covidtracker.models.Lecture.objects.filter(id=id)
    return render(request,'position.html',{'lecture':lecture})

@login_required
def add(request,id):
    lecture=covidtracker.models.Lecture.objects.get(id=id)
    if(request.method=='POST'):
        positionNumber=request.POST['positionNumber']
        user=request.user
        if covidtracker.models.Position.objects.filter(user=user,lecture=lecture).exists():
            lecture=covidtracker.models.Lecture.objects.filter(id=id)
            return render(request,'position.html',{"user":user.username,"lecture":lecture,'result':'Εχετε ήδη δηλώσει την θέση σας'})
        elif covidtracker.models.Position.objects.filter(lecture=lecture,positionNumber=positionNumber).exists():
            lecture=covidtracker.models.Lecture.objects.filter(id=id)
            return render(request,'position.html',{"user":user.username,"lecture":lecture,'result':'Η θέση είναι πιασμένη'})    
        elif covidtracker.models.Position.objects.filter(lecture=lecture,positionNumber=positionNumber).exists()==False:  
            covidtracker.models.Position(user=user,lecture=lecture,positionNumber=positionNumber).save()
            return redirect('/') 
    else:
        return redirect('/')

@login_required
def covid(request):
    return render(request,'covid.html')

@login_required
def covidAdd(request):
    user=request.user
    if request.method=='POST':
        date=request.POST['date']
        covidtracker.models.CovidCase(user=user,date=date).save()
        return redirect('/')
    else:
        return redirect('/') 