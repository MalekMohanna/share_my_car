from django.urls import path 
from . import views

urlpatterns = [
    path('', views.index), 
    path('proce-login',views.proc_login) ,
    path('success',views.success),
    path('registration/',views.registration ),
    path('wall',views.wall),
    path('trips/', views.show_detials_trip),
    path('my-trips/', views.my_trip),
]