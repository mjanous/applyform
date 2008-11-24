from django import forms
from django.contrib.localflavor.us.forms import USPhoneNumberField
from django.contrib.localflavor.us.us_states import STATE_CHOICES

class ApplicationForm(forms.Form):
    # Personal Info
    first_name = forms.CharField(max_length=40, required=False)
    last_name = forms.CharField(max_length=40, required=False)
    dob = forms.DateField(
        label='Date of Birth (YYYY-MM-DD)',
        required=False,
        widget=forms.TextInput({'size': 10}),
    )
    
    # Local Address Info
    address1 = forms.CharField(
        label='Address',
        max_length=40,
        required=False,
    )
    address2 = forms.CharField(
        label='Address 2',
        max_length=40,
        required=False,
    )
    city = forms.CharField(max_length=40, required=False)
    state = forms.ChoiceField(
        required=False,
        choices=STATE_CHOICES,
    )
    
    # Contact Info
    email = forms.EmailField(required=False)
    mobile_phone = USPhoneNumberField(required=False)
    home_phone = USPhoneNumberField(required=False)
    