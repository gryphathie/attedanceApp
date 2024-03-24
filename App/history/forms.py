from django import forms
from django.db.models.base import Model
from .models import Csv
from user.models import Employee
from django.forms import ModelChoiceField
from datetime import datetime


class CsvForm(forms.ModelForm):
    class Meta:
        model = Csv
        fields = ['file_name']


class MyUserChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name


class HistoryForm(forms.Form):
    name = MyUserChoiceField(queryset=Employee.objects.all().order_by("name"),required=False,to_field_name="name")
    card_number = forms.CharField(max_length=20, required=False)
    date_from = forms.DateField(required=True, widget=forms.TextInput(attrs={'type': 'date', 'value': datetime.now().strftime("%Y-%m-%d")}))
    date_to = forms.DateField(required=True, widget=forms.TextInput(attrs={'type': 'date', 'value': datetime.now().strftime("%Y-%m-%d")}))