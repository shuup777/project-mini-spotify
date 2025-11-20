from django.shortcuts import render
from django.http import HttpResponse

top_artists = [
    ("Artist A", 120),
    ("Artist B", 95),
    ("Artist C", 80),
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

    # Contoh logika rekomendasi sederhana
    if username:
        # Misal rekomendasi berdasarkan username (dummy)
        user_recommendations = [
            ("Artist X", 5),
            ("Artist Y", 3),
            ("Artist Z", 2)
        ]

    context = {
        "top_artists": top_artists,
        "recommendations": user_recommendations
    }
    return render(request, 'recommendation_admin.html', context)