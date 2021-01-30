from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt

def index(request):
    return render(request, 'index.html')

def register(request):
    errors = User.objects.register_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        )
    request.session['user_id'] = user.id 
    request.session['greeting'] = user.first_name
    return redirect('/travels')

def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user = User.objects.get(email=request.POST['login_email'])
        request.session['user_id'] = user.id
        request.session['greeting'] = user.first_name
        return redirect('/travels')

def travels(request):
    if 'user_id' not in request.session:
        return redirect('/')
    else:
        context = {
            'trips': Trip.objects.all(),
            'this_user': User.objects.get(id=request.session['user_id'])
        }
        return render(request, 'travels.html', context)

def new(request):
    return render(request, 'create.html')

def create(request):
    errors = Trip.objects.trip_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/new')
    else:
        user = User.objects.get(id=request.session['user_id'])
        trip = Trip.objects.create(
            destination = request.POST['destination'],
            description = request.POST['description'],
            start_date = request.POST['start_date'],
            end_date = request.POST['end_date'],
            planned_by = user
        )
        user.joined.add(trip)

        return redirect('/travels')

def views(request, trip_id):
    context = {
        'trip': Trip.objects.get(id=trip_id),
        'current_user': User.objects.get(id=request.session['user_id'])
    }
    return render(request, 'view.html', context)

def cancel(request, trip_id):
    user = User.objects.get(id=request.session['user_id'])
    trip = Trip.objects.get(id=trip_id)
    user.joined.remove(trip)

    return redirect('/travels')

def join(request, trip_id):
    user = User.objects.get(id=request.session['user_id'])
    trip = Trip.objects.get(id=trip_id)
    user.joined.add(trip)

    return redirect('/travels')

def delete(request, trip_id):
    trip = Trip.objects.get(id=trip_id)
    trip = delete()

    return redirect('/travels')

def logout(request):
    request.session.flush()
    return redirect('/')

# Create your views here.
