from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, Mini Spotify!")

def home(request):
    return HttpResponse("Welcome to Mini Spotify!")