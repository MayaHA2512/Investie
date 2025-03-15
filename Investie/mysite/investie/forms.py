from . import models
from django import forms

class EntryForm(forms.Form):
    entry = forms.ModelChoiceField(queryset=models.Stock.objects.all(), empty_label='Select an entry', to_field_name='ticker')