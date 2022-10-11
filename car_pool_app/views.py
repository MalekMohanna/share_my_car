from multiprocessing import context
from django.shortcuts import render,redirect

def index(request):
    
    return render(request,'add_trip.html')

def show_detials_trip(request):

    return render(request,'trip_details.html')
    
def my_trip(request):
    return render(request,'mytrips.html')