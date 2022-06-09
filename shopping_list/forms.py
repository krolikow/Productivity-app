from django import forms
from . models import Item
from django import forms
from django.forms import ModelForm


class DateInput(forms.DateInput):
    input_type = 'date'


class ItemForm(ModelForm):

    def clean(self):
        cleaned_data = super(ItemForm,self).clean()
        return cleaned_data

    class Meta:
        model = Item
        fields = ['title','complete','shopping_list','amount','unit','category']