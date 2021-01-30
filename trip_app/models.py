from django.db import models
from datetime import datetime
import re, bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def register_validator(self, postData):
        errors = {}
        check = User.objects.filter(email=postData['email'])
        if len(postData['first_name']) < 2:
            errors['first_name'] = 'First name must be at least 2 characters long'
        if len(postData['last_name']) < 2:
            errors['last_name'] = 'Last name must be at least 2 characters long'
        if len(postData['password']) < 8:
            errors['password'] = 'Password cannot be less than 8 characters long'
        elif postData['password'] != postData['confirm_password']:
            errors['password'] = 'Passwords do not match'
        if len(postData['email']) < 1:
            errors['reg_email'] = 'Email address cannot be blank'
        elif not EMAIL_REGEX.match(postData['email']):
            errors['reg_email'] = 'Please enter a valid email address'
        elif check:
            errors['reg_email'] = 'Email address is already registered'
        return errors

    def login_validator(self, postData):
        errors = {}
        check = User.objects.filter(email=postData['login_email'])
        if not check:
            errors['login_email'] = 'Email has not been registered'
        else:
            if not bcrypt.checkpw(postData['login_password'].encode(), check[0].password.encode()):
                errors['login_email'] = 'Email and password do not match'
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateField(auto_now_add=True)
    update_at = models.DateField(auto_now=True)

    objects = UserManager()

class TripManager(models.Manager):
    def trip_validator(self, postData):
        errors = {}
        if len(postData['destination']) < 1:
            errors['destination'] = "Destination must not be blank"
        if len(postData['description']) < 1:
            errors['description'] = "Description must not be blank"
        if postData['start_date'] > postData['end_date']:
            errors['start_date'] = "Start date can not happen after end date"
        return errors

class Trip(models.Model):
    destination = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    planned_by = models.ForeignKey(User, related_name="planner", on_delete=models.CASCADE)
    user_join = models.ManyToManyField(User, related_name="joined")
    created_at = models.DateField(auto_now_add=True)
    update_at = models.DateField(auto_now=True)

    objects = TripManager()
# Create your models here.
