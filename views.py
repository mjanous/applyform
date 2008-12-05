#Create your views here.

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from applyform.models import *
from applyform.forms import *
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

def index(request):
    return render_to_response(
        'applyform/index.html',
        {
            'user': request.user,
            'request': request,
            'MEDIA_URL': settings.MEDIA_URL,
        }
    )

@login_required
def apply_menu(request):
    user = request.user
    profile_complete = False
    try:  
        userprofile = user.get_profile()
        if userprofile.profile_info_completed():
            profile_complete = True
    except UserProfile.DoesNotExist:
        profile_complete = False

    return render_to_response(
        'applyform/apply_menu.html',
        {
            'user': request.user,
            'request': request,
            'MEDIA_URL': settings.MEDIA_URL,
            'profile_complete': profile_complete
        }
    )

@login_required
def basic_info(request):
    user = request.user
    userprofile, created = user.userprofile_set.get_or_create()
    student_profile, created = userprofile.student_profile.get_or_create()
        
    if request.method == 'POST':
        form = BasicInfoForm(request.POST)
        if form.is_valid():
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.save()
            
            userprofile.address1 = form.cleaned_data['address1']
            userprofile.address2 = form.cleaned_data['address2']
            userprofile.dob = form.cleaned_data['dob']
            userprofile.city = form.cleaned_data['city']
            userprofile.state = form.cleaned_data['state']
            if form.cleaned_data['zipcode'] == u'':
                userprofile.zipcode = None
            else:
                userprofile.zipcode = form.cleaned_data['zipcode'] 
            userprofile.home_phone = form.cleaned_data['home_phone']
            userprofile.mobile_phone = form.cleaned_data['mobile_phone']
            userprofile.save()
            
            student_profile.grad_date = form.cleaned_data['grad_date']
            student_profile.grad_status = form.cleaned_data['grad_status']
            student_profile.enrollment_status = form.cleaned_data['enrollment_status']
            student_profile.honors_status = form.cleaned_data['honors_status']
            student_profile.save() 
            return HttpResponseRedirect(reverse('apply_menu'))
    else:
        try:
            grad_date_pk = student_profile.grad_date.pk
        except AttributeError:
            grad_date_pk = None
            
        form = BasicInfoForm(
            initial={
                'first_name': user.first_name,
                'last_name': user.last_name,
                'address1': userprofile.address1,
                'address2': userprofile.address2,
                'dob': userprofile.dob,
                'city': userprofile.city,
                'state': userprofile.state or 'IL',
                'zipcode': userprofile.zipcode,
                'email': user.email,
                'home_phone': userprofile.home_phone,
                'mobile_phone': userprofile.mobile_phone,
                'grad_date': grad_date_pk,
                'grad_status': student_profile.grad_status,
                'enrollment_status': student_profile.enrollment_status,
                'honors_status': student_profile.honors_status,
            }
        )
        
    return render_to_response(
        'applyform/basic_info.html',
        {
            'user': request.user,
            'form': form,
            'MEDIA_URL': settings.MEDIA_URL,
        }
    )

@login_required
def project_select(request):
    user = request.user
    userprofile, created = user.userprofile_set.get_or_create()
    student_profile, created = userprofile.student_profile.get_or_create()
        
    try:
        semester = Semester.accepting_semesters.get()
    except Semester.DoesNotExist:
        return HttpResponseRedirect(reverse('not_accepting'))
    except Semester.MultipleObjectsReturned:
        # BIG WARNING!! Currently, if more than one semester has an
        # 'Accepting Apps' Date range that 'now' falls into, this exception
        # will happen and it will appear as if there aren't any applications
        # being accepted. I don't forsee us accepting applications for more
        # than one semester at a time but I've left the functionality in there
        # just in case. This exception will have to be changed and redirected
        # to it's own view that will allow a student to choose which semester
        # they want to apply for.
        return HttpResponseRedirect(reverse('not_accepting'))
    
    projects = Project.accepting_apps.all()

        
    return render_to_response(
        'applyform/project_select.html',
        {
            'projects': projects,
            'semester': semester,
            'user': request.user,
            'MEDIA_URL': settings.MEDIA_URL,
        }
    )

def not_accepting(request):
    return render_to_response(
        'applyform/not_accepting.html',
        {
            'user': request.user,
            'request': request,
            'MEDIA_URL': settings.MEDIA_URL,
        }
    )

def thanks(request):
    return render_to_response(
        'applyform/thanks.html',
        {
            'user': request.user,
            'request': request,
            'MEDIA_URL': settings.MEDIA_URL,
        }
    )
