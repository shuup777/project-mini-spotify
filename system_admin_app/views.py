from django.shortcuts import render

def dashboard(request):
    return render(request, 'system_admin/dashboard.html')