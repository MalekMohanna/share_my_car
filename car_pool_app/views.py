from distutils.log import error
from lib2to3.pgen2 import driver
from multiprocessing import context
from tkinter import Y
from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages



def index(request):
    return render(request,'landing.html')

def login(request):
    return render(request,'login.html')

def proc_login(request):
    if request.method != "POST":
        return redirect("/login")
    valid = User.objects.login_validator(request.POST)
    if len (valid["errors"]) > 0:
        for key, value in valid["errors"].items():
            messages.error(request,value)
        return redirect("/login")
    else:
        request.session["user_id"] = valid["user"].id
        return redirect ("/success")
    

def success(request):
    if "user_id" not in request.session:
        return redirect("/")
    return redirect('/wall')

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

def logout(request):
    request.session.clear()
    return redirect ("/login")

def wall(request):
    if 'user_id' not in request.session:
        return redirect('/')
    else :
        context={
            'my_trip':Trip.objects.all(),
            'my_user':User.objects.get(id=request.session['user_id']),
        }
        return render(request,'wall.html',context)

def make_trip(request):
    if 'user_id' not in request.session:
        return redirect('/')
    else :
        context = {
            'my_user':User.objects.get(id=request.session['user_id']),
        }
        return render(request,'add_trip.html',context)

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

def account(request):
    if 'user_id' not in request.session:
        return redirect('/')
    else :
        context={
            'my_trip':Trip.objects.all(),
            'my_user':User.objects.get(id=request.session['user_id']),
            'my_passanger':Passanger.objects.all(),
        }
        return render(request,'account.html',context)

def trip_details(request,id):
    if 'user_id' not in request.session:
        return redirect('/')
    else :
        z = Passanger.objects.filter(trip_id=id)
        context = {
            'my_trip':Trip.objects.get(id=id),
            'my_user':User.objects.get(id=request.session['user_id']),
            'my_passangers':z,
        }
        return render(request,'trip_details.html',context)

def join_trip(request,id):
    user = User.objects.get(id=request.session['user_id'])
    trip = Trip.objects.get(id = id)
    y = Passanger.objects.filter(passanger_id=request.session['user_id'],trip_id=id)
    c = trip.id
    seats_availabe =trip.seats_num
    if seats_availabe > 0:
        if not y :
            y=trip.seats_num
            y-=1
            trip.seats_num=y
            trip.save()
            x = Passanger.objects.create(passanger = user,trip = trip)
            x.save()
    return redirect(f'/details/{c}')

def update(request,id):
    x= Trip.objects.get(id= id)
    print(x.car)
    phone = request.POST['phone-num']
    from1 = request.POST['city-from']
    to = request.POST['city-to']
    date1 = request.POST['date_from']
    desc = request.POST['desc']
    x.phone_num = phone
    x.from_where = from1
    x.to_where = to
    x.when = date1
    x.descreption = desc
    x.save()
    return redirect(f'/details/{id}')

def delete(request,id):
    x= Trip.objects.get(id= id)
    x.delete()
    return redirect('/wall')

def search(request):
    if 'user_id' not in request.session:
        return redirect('/')
    else :
        from1 = request.POST['from']
        to = request.POST['to']
        x = Trip.objects.filter(from_where = from1, to_where = to)
        context = {
            'my_trip': x,
            'my_user':User.objects.get(id=request.session['user_id']),
        }
        return render(request,'search.html',context)

def about(request):
    if 'user_id' not in request.session:
        return redirect('/')
    else :
        context = {
            'my_user':User.objects.get(id=request.session['user_id']),
        }
        return render(request,'about.html',context)