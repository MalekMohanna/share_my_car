from multiprocessing import context
from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages


def index(request):
    
    return render(request,'add_trip.html')

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
    context = {

    }
    return render(request,'wall.html',context)

def show_detials_trip(request):

    return render(request,'trip_details.html')
    
def my_trip(request):
    return render(request,'mytrips.html')