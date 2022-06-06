from django import forms
from . models import Data
from django import forms
from django.forms import ModelForm


class DateInput(forms.DateInput):
    input_type = 'date'


class DataForm(ModelForm):

    def clean(self):
        cleaned_data = super(DataForm,self).clean()
        return cleaned_data

    class Meta:
        model = Data
        fields = ['tracker','date','amount','description']
        widgets = {
            'date': DateInput(),
        }       