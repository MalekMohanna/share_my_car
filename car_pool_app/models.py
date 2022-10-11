from __future__ import unicode_literals
import re , bcrypt
from django.db import models
import datetime

# Create your models here.

class UserManager(models.Manager):
    def new_validator(self, postData):
        errors = {}    
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData["email"]):
            errors["email"] = "Invalid email address"
        if len(postData["first_name"]) < 2:
            errors["first_name"] = "First name should be at least 2 characters"
        if len(postData["last_name"]) < 2:
            errors["last_name"] = "Last name should be at least 2 characters"
        if len(postData["password"]) < 8:
            errors["password"] = "Password must be 8 characters or more"
        if (postData["password"] != postData["confirmed_password"]):
            errors ["password"] = "Passwords do not match"
        return errors
    
    def login_validator(self,postData):
        valid = {
            "errors" : {},
        }
        user = self.filter(email=postData["login_email"])
        if user:
            existing_user=user[0]
            if not bcrypt.checkpw(postData["login_password"].encode(),existing_user.password.encode()):
                valid["errors"]["login_password"] = "Password is incorrect"
            else:
                valid["user"] = existing_user
        else:
            valid["errors"]["login_email"] = "Email not found"
        return valid

class TripManager(models.Manager):
    def trip_validation(self,postdata):
        errors = {}  
        date_format = "%Y-%m-%d"  # %Y for year, %m for month and %d for day

        if len(postdata["phone-num"]) < 2:
            errors["phone-num"] = "Phone number should be at least 9 numbers"
        if len(postdata["car-name"]) < 3:
            errors["car-name"] = "Car name number should be at least 3 characters"
        if len(postdata["seats-num"]) < 1:
            errors["seats-num"] = "Seats number should be at least 1 numbers"
        if len(postdata["city-from"]) < 3:
            errors["city-from"] = "City name  should be at least 3 characters"
        if len(postdata["city-to"]) < 3:
            errors["city-to"] = "City name  should be at least 3 characters"
        if datetime.datetime.today() > datetime.datetime.strptime(postdata['date_from'],date_format) :
            errors['date_from'] = "Date must be in the Future"
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Trip(models.Model):
    phone_num= models.IntegerField()
    car = models.CharField(max_length = 255)
    seats_num = models.IntegerField()
    from_where = models.CharField(max_length=255)
    to_where = models.CharField(max_length=255)
    descreption = models.CharField(max_length=255)
    driver = models.ForeignKey(User, related_name="drivers", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TripManager()


class Passanger(models.Model):
    passanger = models.ForeignKey(User, related_name="passangers", on_delete = models.CASCADE)
    trip = models.ForeignKey(Trip, related_name="trips", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


def add_user(postdata):
    first_name = postdata.get('first_name')
    last_name =  postdata.get('last_name')
    pw = postdata.get('password')
    pw_hash = bcrypt.hashpw(pw.encode(), bcrypt.gensalt()).decode()
    print(pw_hash)
    email1 = postdata.get('email')
    User.objects.create(first_name=first_name,last_name=last_name,password=pw_hash,email=email1)
    last = User.objects.last()
    print('done')
    return last.id