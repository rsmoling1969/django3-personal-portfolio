from django.forms import ModelForm
from .models import CoblentzNumbers

class ShiftForm(ModelForm):
    class Meta:
        model = CoblentzNumbers
        fields = ['date', 'shift']

class ShiftDetailForm(ModelForm):
    class Meta:
        model = CoblentzNumbers
        fields = ['shift', 'date', 'numbers']