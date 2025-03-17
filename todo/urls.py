
from django.contrib import admin
from django.urls import path

from todo import views

urlpatterns = [
    path('', views.home, name='home'),
]
