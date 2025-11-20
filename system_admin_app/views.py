from django.shortcuts import render
from django.http import HttpResponse

def dashboard(request):
    return render(request, 'system_admin/dashboard.html')

def index(request):
    return HttpResponse("Hello system")