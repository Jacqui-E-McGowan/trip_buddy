from django.urls import path     
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('travels', views.travels),
    path('new', views.new),
    path('create', views.create),
    path('view/<int:trip_id>', views.views),
    path('travels/<int:trip_id>/cancel', views.cancel),
    path('travels/<int:trip_id>/join', views.join),
    path('travels/<int:trip_id>/delete', views.delete),
    path('logout', views.logout),   
]