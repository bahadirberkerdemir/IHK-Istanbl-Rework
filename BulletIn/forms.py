from django import forms
from django.forms import ModelForm
from django import forms
from persons.models import Hakem,Gozlemci

class HakemForm(forms.ModelForm):
    class Meta:
        model = Hakem
        fields = '__all__'
        widgets = {
            'alan_adi': forms.TextInput(attrs={'class': 'Hakem'}),
        }

class GozlemciForm(forms.ModelForm):
    class Meta:
        model = Gozlemci
        fields = '__all__'
        widgets = {
            'alan_adi': forms.TextInput(attrs={'class': 'Gozlemci'}),
        }