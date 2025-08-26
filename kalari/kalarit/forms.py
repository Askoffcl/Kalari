from sched import Event
from django import forms
from .models import *
from django.core.exceptions import ValidationError
import re
from datetime import date
from django.utils import timezone

class ClassR(forms.ModelForm):
    class Meta:
        model = Class
        fields = ['name', 'date', 'amount','duration', 'image', 'desc']
        widgets = {
            'name': forms.TextInput(attrs={
                'id': 'username', 'name': 'username', 'class': 'form-control'
            }),
            'date': forms.DateTimeInput(attrs={
                'type': 'datetime-local', 'class': 'form-control', 'id': 'date', 'name': 'date'
            }),
            'duration': forms.NumberInput(attrs={
                'id': 'duration', 'name': 'duration', 'class': 'form-control'
            }),
            'image': forms.FileInput(attrs={'id': 'image', 'name': 'image'}),
            'desc': forms.Textarea(attrs={
                'class': 'form-control', 'id': 'bio', 'name': 'bio', 'placeholder': 'Brief description of class'
            }),
             'amount': forms.NumberInput(attrs={
                'id': 'amount', 'name': 'amount', 'class': 'form-control'
            }),
        }
        labels = {
            'name': 'Class Name',
            'date': 'Schedule',
            'duration': 'Duration (min)',
            'image': 'Image',
            'desc': 'Description',
            'amount':'Fees'
        }

    def clean_date(self):
        start_date = self.cleaned_data.get('date')
        if start_date and (not self.instance.pk or start_date != self.instance.date):
            if start_date < timezone.now():   # ✅ for DateTimeField
                raise ValidationError("Schedule cannot be in the past.")
        return start_date
    
    def clean_amount(self):
        target = self.cleaned_data.get('amount')
        if target is None or target <= 0:
            raise ValidationError(" amount must be greater than zero.")
        return target


class EventR(forms.ModelForm):
    class Meta:
        model = Events
        fields = ['name', 'date', 'amount','loc', 'image', 'desc','amount']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'name', 'placeholder': 'Enter event name'
            }),
            'date': forms.DateInput(attrs={
                'type': 'date', 'class': 'form-control', 'id': 'date'
            }),
            'loc': forms.Textarea(attrs={
                'class': 'form-control', 'id': 'loc', 'rows': 3, 'placeholder': 'Enter location'
            }),
            'image': forms.FileInput(attrs={'id': 'image', 'name': 'image'}),
            'desc': forms.Textarea(attrs={
                'class': 'form-control', 'id': 'bio', 'name': 'bio', 'placeholder': 'Brief description of event'
            }),
             'amount': forms.NumberInput(attrs={
                'id': 'amount', 'name': 'amount', 'class': 'form-control'
            }),
        }
        labels = {
            'name': 'Event Name',
            'date': 'Event Date',
            'loc': 'Location',
            'image': 'Image',
            'desc': 'Description',
            'amount':'Fees'
        }

    def clean_date(self):
        start_date = self.cleaned_data.get('date')
        if start_date and (not self.instance.pk or start_date != self.instance.date):
            if start_date < date.today():   # ✅ for DateField
                raise ValidationError("Event date cannot be in the past.")
        return start_date
    def clean_amount(self):
        target = self.cleaned_data.get('amount')
        if target is None or target <= 0:
            raise ValidationError(" amount must be greater than zero.")
        return target    

class TrainingForm(forms.ModelForm):
    class Meta:
        model = Training
        fields = ['title', 'desc', 'file']

        widgets = {
            'title': forms.TextInput(
                attrs={'class': 'form-control', 'id': 'title', 'placeholder': 'Enter title name'}
            ),
            'desc': forms.Textarea(
                attrs={ 'class': 'form-control', 'id': 'desc'}
            ),
            'file': forms.FileInput(
                attrs={'class': 'form-control', 'id': 'file'}
            ),
        }
        label = {
            'title':'Title',
            'desc' :'Description',
            'file':'Upload File'
        }


