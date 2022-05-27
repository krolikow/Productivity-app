from django import forms
from . models import Data
from django import forms
from django.forms import ModelForm


class DateInput(forms.DateInput):
    input_type = 'date'


class DataForm(ModelForm):
    # def clean_data(self):
    #     cleaned_data = self.clean()
    #     data = cleaned_data.get('data')
#         if not 
# modelName.objects.filter(pk='id').exists()
    class Meta:
        model = Data
        fields = ['tracker','title','date','amount','description']
        widgets = {
            'date': DateInput(),
        }       