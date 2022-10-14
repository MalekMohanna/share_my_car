from django.urls import path 
from . import views

urlpatterns = [
    path('',views.index),
    path('login/', views.login), 
    path('proce-login',views.proc_login) ,
    path('success',views.success),
    path('registration/',views.registration ),
    path('regist_proc',views.regist_proc),
    path('wall/',views.wall),
    path('search',views.search),
    path('make_trip/',views.make_trip),
    path('trip_process',views.trip_process),
    path('logout',views.logout),
    path('account/',views.account),
    path('details/<int:id>',views.trip_details),
    path('join_trip/<int:id>',views.join_trip),
    path('update/<int:id>',views.update),
    path('delete_trip/<int:id>',views.delete),
    path('about/',views.about),
    path('login/check',views.check,name="check"),

]