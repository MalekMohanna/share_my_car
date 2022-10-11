from distutils.log import error
from lib2to3.pgen2 import driver
from multiprocessing import context
from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages


def index(request):

    return render(request,'index.html')

def success(request):
    if "user_id" not in request.session:
        return redirect("/")
    return redirect('/wall')

def proc_login(request):
    if request.method != "POST":
        return redirect("/")
    valid = User.objects.login_validator(request.POST)
    if len (valid["errors"]) > 0:
        for key, value in valid["errors"].items():
            messages.error(request,value)
        return redirect("/")
    else:
        request.session["user_id"] = valid["user"].id
        return redirect ("/success")
    

def registration(request):

    return render(request,'registration.html')

def regist_proc(request):
    errors={}
    errors=User.objects.new_validator(request.POST)
    if not errors:
        id = add_user(request.POST)
        return redirect("/")
    else:
        for key, value in errors.items():
            messages.error(request,value)
        return redirect("/registration")


def wall(request):
    context={
        'my_trip':Trip.objects.all(),
        'my_user':User.objects.get(id=request.session['user_id']),
    }
    return render(request,'wall.html',context)

def make_trip(request):
    return render(request,'add_trip.html')

def trip_process(request):
    errors ={}
    errors = Trip.objects.trip_validation(request.POST)
    if not errors:
        phone = request.POST['phone-num']
        car = request.POST['car-name']
        seats = request.POST['seats-num']
        from1 = request.POST['city-from']
        to = request.POST['city-to']
        date1 = request.POST['date_from']
        desc = request.POST['desc']
        x=Trip.objects.create(phone_num=phone,car=car,seats_num=seats,from_where=from1,to_where=to,descreption=desc,when=date1,driver=User.objects.get(id=request.session['user_id']))
        x.save()
        return redirect('/wall')
    else:
        for key, value in errors.items():
            messages.error(request,value)
    return redirect('/make_trip')