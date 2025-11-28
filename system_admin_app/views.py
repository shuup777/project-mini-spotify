from django.shortcuts import render
from django.http import HttpResponse

top_artists = [
    ("Pamungkas", 120),
    ("Nadin Amizah", 95),
    ("Tulus", 80),
]

# Halaman dashboard /system/
def dashboard(request):
    context = {
        "top_artists": top_artists,
        "recommendations": None
    }
    return render(request, 'recommendation_admin.html', context)

# Halaman rekomendasi /system/recommendations/
def recommendations(request):
    username = request.GET.get('username')
    user_recommendations = []

    if username:
        user_recommendations = [
            ("Rizky Febian", 5),
            ("Isyana Sarasvati", 3),
            ("Fiersa Besari", 2)
        ]

    context = {
        "top_artists": top_artists,
        "recommendations": user_recommendations
    }
    return render(request, 'recommendation_admin.html', context)
