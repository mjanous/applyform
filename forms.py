from django import forms

class ApplicationForm(forms.Form):
    first_name = forms.CharField(max_length=40, required=False)
    last_name = forms.CharField(max_length=40, required=False)
    dob = forms.DateField(required=False)
    address1 = forms.CharField(max_length=40, required=False)
    address2 = forms.CharField(max_length=40, required=False)
    city = forms.CharField(max_length=40, required=False)