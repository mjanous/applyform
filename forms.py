from datetime import datetime

from django import forms
from django.contrib.localflavor.us.forms import USPhoneNumberField, USZipCodeField
from applyform.lib.us.us_states import STATE_CHOICES
from applyform.lib.shirts.shirts import SHIRT_CHOICES
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
    major = forms.ModelChoiceField(
        required=False,
        label="Current Major",
        queryset=Major.objects.all(),
    )
    grad_date = forms.ModelChoiceField(
        required=False,
        label="Anticipated Graduation Semester",
        queryset=Semester.objects.filter(end_date__gte=datetime.now()),
    )
    semester_for_310 = forms.ModelChoiceField(
        required=False,
        label="UBUS 310 Completion Semester",
        queryset=Semester.objects.all(),
    )
    semester_for_311 = forms.ModelChoiceField(
        required=False,
        label="UBUS 311 Completion Semester",
        queryset=Semester.objects.all(),
    )
    is_grad_student = forms.TypedChoiceField(
        required=False,
        label="Graduate Student",
        widget=forms.RadioSelect(),
        choices=((1, 'Yes'),(0, 'No')),\
    )
    is_honors_student = forms.TypedChoiceField(
        required=False,
        label="Honors Student",
        widget=forms.RadioSelect(),
        choices=((1, 'Yes'),(0, 'No')),
    )
    
    # Miscellaneous Info
    tshirt_size = forms.ChoiceField(
        required=False,
        choices=SHIRT_CHOICES,
        widget=forms.Select(attrs={'class': 'text_field'})
    )
    
class ProjectSelectForm(forms.Form):
    PROJECT_RATING_CHOICES = (
        ('', '--------'),
        ('0', 'Not Interested'),
        ('1', 'Interested'),
        ('2', 'Very Interested'),
    )
    
    project = forms.IntegerField(
        required=False,
        widget=forms.HiddenInput(),
    )
    project_name = forms.CharField(
        required=False,
        widget=forms.HiddenInput(),
    )
    interest_rating = forms.ChoiceField(
        required=False,
        choices=PROJECT_RATING_CHOICES,
        widget=forms.Select(),
    )
    
class CoverLetterForm(forms.Form):
    cover_letter = forms.CharField(
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

class ReferenceForm(forms.Form):
    email = forms.EmailField(
        label='Reference Email',
        required=True,
    )
    first_name = forms.CharField(
        label="First Name",
        required=True,
    )
    last_name = forms.CharField(
        label="Last Name",
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
    
class ReportSemesterForm(forms.Form):
    semester = forms.ModelChoiceField(
        required=False,
        label="Semester",
        queryset=Semester.objects.filter(project_set__consultants__isnull=False).distinct(),
    )

class ReportProjectForm(forms.Form):
    class ProjectModelChoiceField(forms.ModelChoiceField):
        def label_from_instance(self, obj):
            def smart_truncate(content, length=40, suffix='...'):
                if len(content) <= length:
                    return content
                else:
                    return ' '.join(content[:length+1].split(' ')[0:-1]) + suffix
                
            return " - ".join((smart_truncate(obj.sponsors_string, 20), smart_truncate(obj.project_name)))
        
    project = ProjectModelChoiceField(
        required=False,
        label="Project",
        queryset=sorted(Project.objects.all(), key=lambda a: a.sponsors_string),
    )

class ResumeUploadForm(forms.Form):
    file_upload = forms.FileField()
    
class FinalizeSubmissionForm(forms.Form):
    understand = forms.BooleanField(
        label="I understand that once I click submit I can no longer change my application",
    )
    