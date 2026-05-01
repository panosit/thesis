from django.urls import path
from . import views

urlpatterns=[
    path('',views.home,name='home'),
    path('login',views.login_view,name='login'),
    path('logout',views.logout_view,name='logout'),
    path('index.html',views.home,name='legacy_home'),
    path('show',views.show,name='show'),
    path('lectures/<int:id>/',views.lecture_detail,name='lecture_detail'),
    path('lectures/<int:id>/add',views.add_position,name='add_position'),
    path('covid',views.covid,name='covid'),
    path('covidAdd',views.covid_add,name='covid_add'),
]
