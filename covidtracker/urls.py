from django.urls import path
from . import views

urlpatterns=[
    path('',views.home),
    path('login',views.login),
    path('logout',views.logout),
    path('index.html',views.home),
    path('show',views.show),
    path('lectures/<int:id>/',views.lecture),
    path('lectures/<int:id>/add',views.add),
    path('covid',views.covid),
    path('covidAdd',views.covidAdd),
]