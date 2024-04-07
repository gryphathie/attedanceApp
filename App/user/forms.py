from django.forms import formset_factory
from django import forms
from .models import *

TEAM = [("BFS", "BFS"),
        ("DEVS", "DEVS")]

LEAVES = [("WFH", "WFH"),
          ("SL", "Sick"),
          ("VL", "Vacations"),
          ("BL", "Bereavement"),
          ("ML", "Maternity"),
          ("PL", "Paternity"),
          ("CL", "Compensatory")
          ]

class EmployeeCreationForm(forms.ModelForm):
    name = forms.CharField(label="Name of Employee:", required=True, max_length=500)
    ace = forms.CharField(label="ACE Number:", required=True, max_length=30)
    card_number1 = forms.CharField(label="Card Number 1:", required=True, max_length=20)
    card_number2 = forms.CharField(label="Card Number 2:", required=False, max_length=20)
    card_number3 = forms.CharField(label="Card Number 3:", required=False, max_length=20)
    team = forms.ChoiceField(label="Team:", choices=TEAM, required=True)

    class Meta:
        model = Employee
        fields = '__all__'


class GuestCreationForm(forms.ModelForm):
    employee = forms.ModelChoiceField(label="Select an Employee", queryset=Employee.objects.all(), required=True)
    card_number = forms.CharField(label="Card Number:", required=True, max_length=20)
    start_date = forms.DateField(widget=forms.TextInput(attrs={'type':'date'}), required=True)
    end_date = forms.DateField(widget=forms.TextInput(attrs={'type':'date'}), required=False)

    class Meta:
        model = Guest
        fields = '__all__'


class LeaveCreationForm(forms.ModelForm):
    employee = forms.ModelChoiceField(label="Select an Employee", queryset=Employee.objects.all(), required=True)    
    start_date = forms.DateField(widget=forms.TextInput(attrs={'type':'date'}), required=True)
    end_date = forms.DateField(widget=forms.TextInput(attrs={'type':'date'}), required=False)
    leave_type = forms.ChoiceField(label="Type:", choices=LEAVES, required=True)

    class Meta:
        model = Leave
        fields = '__all__'
        

EmployeeCreationFormSet = formset_factory(EmployeeCreationForm, extra=1)