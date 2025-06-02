from django import forms
from .models import Concept

class ConceptForm(forms.ModelForm):
    class Meta:
        model = Concept
        fields = ['title', 'description']
