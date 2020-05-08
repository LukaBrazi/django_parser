from django import forms
from .models import Car


class CarForm(forms.ModelForm):
    title = forms.CharField()

