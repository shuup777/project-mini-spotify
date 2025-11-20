from django import forms
from .models import Song

class SongUploadForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ["title", "audio_file", "cover_image", "price"]
        widgets = {
            "price": forms.NumberInput(attrs={"step": "0.01", "min": "0"}),
        }

class SongEditForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ["title", "cover_image", "price"]
