from django import forms
from .models import Resenha

class ResenhaForm(forms.ModelForm):

    class Meta:
        model = Resenha
        fields = ('texto',)

        widgets = {
            'texto': forms.Textarea(attrs={'class': 'form-control', 'row': '3'}),
        }
