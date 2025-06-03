from django import forms
from .models import ActionLog

class ActionLogForm(forms.ModelForm):
    class Meta:
        model = ActionLog
        fields = ['parameter', 'description']
