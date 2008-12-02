from django import forms
from django.contrib.localflavor.us.forms import USPhoneNumberField, USZipCodeField
from django.contrib.localflavor.us.us_states import STATE_CHOICES

class ApplicationForm(forms.Form):
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
    