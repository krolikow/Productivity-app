from django import forms
from . models import Data

class DataForm(forms.ModelForm):
    class Meta:
        model = Data
        fields = [    amount ,
    date ,
    description,
    created_at ]
        widgets = {
            'category': forms.TextInput(attrs={'class': 'form-control'}),
            'num_of_products': forms.TextInput(attrs={'class': 'form-control'}),
        }