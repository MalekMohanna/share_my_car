from multiprocessing import context
from django.shortcuts import render,redirect

def index(request):
    
    return render(request,'index.html')