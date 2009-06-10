from datetime import datetime

from django import forms
from django.contrib.localflavor.us.forms import USPhoneNumberField, USZipCodeField
from applyform.lib.us.us_states import STATE_CHOICES
from applyform.models import *
from applyform.lib.widgets import NullBooleanDashedSelect

from tinymce.widgets import TinyMCE


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
    is_grad_student = forms.NullBooleanField(
        required=False,
        label="I am a Graduate Student",
        widget=NullBooleanDashedSelect(),
    )
    is_enrolled_in_ubus311 = forms.NullBooleanField(
        required=False,
        label="I am enrolled in or have completed UBUS 311",
        widget=NullBooleanDashedSelect(),
    )
    is_honors_student = forms.NullBooleanField(
        required=False,
        label="I am an honors Student",
        widget=NullBooleanDashedSelect(),
    )
    
class ProjectSelectForm(forms.Form):
    project = forms.IntegerField(
        required=False,
        widget=forms.HiddenInput(),
    )
    project_name = forms.CharField(
        required=False,
        widget=forms.HiddenInput(),
    )
    is_interested = forms.NullBooleanField(
        label="Interested in this project",
        widget=NullBooleanDashedSelect(),
    )
    
class ResumeForm(forms.Form):
    resume = forms.CharField(
        widget=TinyMCE(
            attrs={'cols': 130, 'rows': 30},
            mce_attrs={
                'mode': "textareas",
                'theme': "advanced",
                'language': "en",
                'theme_advanced_toolbar_location': "top",
                'theme_advanced_toolbar_align': "left",
                'theme_advanced_statusbar_location': "",
                'theme_advanced_buttons1': (
                    "save,cancel,|,fullscreen,|,image,preview,|,cut,copy,"
                    "paste,|,undo,redo,|,bold,italic,underline,|,"
                    "bullist,numlist,|,sub,sup,|,justifyleft,justifycenter,"
                    "justifyright,justifyfull,|,outdent,indent,|,link,unlink"
                ),
                'theme_advanced_buttons2': (
                    "formatselect,|,forecolor,backcolor,|,table,delete_col,"
                    "delete_row,col_after,col_before,row_after,row_before,"
                    "row_after,row_before,split_cells,merge_cells"
                ),
                'theme_advanced_buttons3': "",
                'theme_advanced_path': 'false',
                'theme_advanced_blockformats': "p,h1,h2,h3",
                'width': '100%',
                'height': '100%',
                'content_css': "/media/css/style.css",
                'plugins': "advimage,advlink,fullscreen,table,preview,save",
                'advimage_update_dimensions_onchange': 'true',
                'relative_urls': 'false'
            },
        )
    )

class ReferenceCheckForm(forms.Form):
    email = forms.EmailField(
        label='Reference Email',
        required=True,
    )
    
class ReferenceRatingForm(forms.Form):
    department = forms.CharField(
        label=()
    )
    q_how_known = forms.CharField(
        label="In what capacity have you known the student?",
        required=True,
    )
    q_strengths = forms.CharField(
        label=("What strengths of the student would contribute to a "
            "successful project outcome?"),
        required=True,
    )
    q_strength_example = forms.CharField(
        label=("Please give an example of a situation when the "
            "student has demonstrated one or more of these strengths"),
        required=True,
    )
    q_weakness = forms.CharField(
        label="What is an area of weakness for the student?",
        required=True,
    )
    q_weakness_improve = forms.CharField(
        label=("How will being a member of an ELC team help the "
            "student address this weakness?"),
        required=True,
    )
    ability_rating = forms.ComboField(
        label=("On a scale from 1-10 (10 being the highest), "
            "please rate the ability of this student to work in a "
            "self-directed, team focused project."),
        required=True,
    )
