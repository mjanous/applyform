from datetime import datetime

from django import forms
from django.contrib.localflavor.us.forms import USPhoneNumberField, USZipCodeField
from django.contrib.localflavor.us.us_states import STATE_CHOICES
from applyform.models import Semester
from applyform.lib.widgets import NullBooleanDashedSelect

class BasicInfoForm(forms.Form):
    # Personal Info
    first_name = forms.CharField(
        max_length=40,
        required=False,
        widget=forms.TextInput(attrs={'class': 'text_field'}),
    )
    last_name = forms.CharField(
        max_length=40,
        required=False,
        widget=forms.TextInput(attrs={'class': 'text_field'}),
    )
    dob = forms.DateField(
        label='Date of Birth',
        required=False,
        widget=forms.TextInput(attrs={'class': 'text_field'}),
    )
    
    # Local Address Info
    address1 = forms.CharField(
        label='Address',
        max_length=40,
        required=False,
        widget=forms.TextInput(attrs={'class': 'text_field'}),
    )
    address2 = forms.CharField(
        label='Address 2',
        max_length=40,
        required=False,
        widget=forms.TextInput(attrs={'class': 'text_field'}),
    )
    city = forms.CharField(
        max_length=40,
        required=False,
        widget=forms.TextInput(attrs={'class': 'text_field'}),
    )
    state = forms.ChoiceField(
        required=False,
        choices=STATE_CHOICES,
        widget=forms.Select(attrs={'class': 'text_field'})
    )
    zipcode = USZipCodeField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'text_field'})
    )
    
    # Contact Info
    email = forms.EmailField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'text_field'}),
    )
    mobile_phone = USPhoneNumberField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'text_field'}),
    )
    home_phone = USPhoneNumberField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'text_field'}),
    )
    
    # Academic (student) Info
    grad_date = forms.ModelChoiceField(
        required=False,
        label="Anticipated Graduation Semester",
        queryset=Semester.objects.filter(end_date__gte=datetime.now()),
    )
    grad_status = forms.NullBooleanField(
        required=False,
        label="I am a Graduate Student",
        widget=NullBooleanDashedSelect(),
    )
    enrollment_status = forms.NullBooleanField(
        required=False,
        label="I am enrolled in or have completed UBUS 311",
        widget=NullBooleanDashedSelect(),
    )
    honors_status = forms.NullBooleanField(
        required=False,
        label="I am an honors Student",
        widget=NullBooleanDashedSelect(),
    )
    
