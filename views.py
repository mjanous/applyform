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
    
    try:
        semester_accepting = Semester.accepting_semesters.get()
    except Semester.DoesNotExist:
        semester_accepting = None
    except Semester.MultipleObjectsReturned:
        semester_accepting = None
    
    try:
        student_profile, created = userprofile.student_profile.get_or_create()
        current_app_complete = student_profile.applications.get(for_semester=semester_accepting).is_complete()
    except Application.DoesNotExist:
        current_app_complete = False
    except UnboundLocalError:
        current_app_complete = False

    return render_to_response(
        'applyform/apply_menu.html',
        {
            'current_app_complete': current_app_complete,
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
        semester_accepting = Semester.accepting_semesters.get()
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
    
    projects = semester_accepting.project_set.all()
    application, created = student_profile.applications.get_or_create(for_semester=semester_accepting)
    
    initial_data = []
    for project in projects:
        try:
            interest = project.projectinterest_set.get(application=application).interest
        except ProjectInterest.DoesNotExist:
            interest = None
        except ProjectInterest.MultipleObjectsReturned:
            # THIS SHOULD NEVER HAPPEN. If it does, something's seriously messed up.
            interest = None
        
        initial_data.append({
            'project_name': project.project_name,
            'project': project.pk, 'interest': interest
        })

    from django.forms.formsets import formset_factory
    ProjectSelectFormSet = formset_factory(ProjectSelectForm, extra=0)
    if request.method == 'POST':
        formset = ProjectSelectFormSet(request.POST)
        if formset.is_valid():
            for i in range(int(request.POST['form-TOTAL_FORMS'])):
                project_interest, created = application.projectinterest_set.get_or_create(
                    project=Project.objects.get(pk=formset.forms[i].cleaned_data['project'])
                )
                project_interest.interest = formset.forms[i].cleaned_data['interest']
                project_interest.save()
            return HttpResponseRedirect(reverse('apply_menu'))
    else:
        formset = ProjectSelectFormSet(initial=initial_data)
    return render_to_response(
        'applyform/project_select.html',
        {
            'formset': formset,
            'projects': projects,
            'semester': semester_accepting,
            'user': request.user,
            'MEDIA_URL': settings.MEDIA_URL,
        }
    )

@login_required
def resume(request):
    user = request.user
    userprofile, created = user.userprofile_set.get_or_create()
    student_profile, created = userprofile.student_profile.get_or_create()
        
    try:
        semester_accepting = Semester.accepting_semesters.get()
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
    
    projects = semester_accepting.project_set.all()
    application, created = student_profile.applications.get_or_create(for_semester=semester_accepting)
    
    if request.method == 'POST':
        form = ResumeForm(request.POST)
        if form.is_valid():
            application.resume = form.cleaned_data['resume'].replace(
                '&lt;!--', '<!--').replace('--&gt;', '-->')
            application.save()
            return HttpResponseRedirect(reverse('apply_menu'))
    else:
        form = ResumeForm(
            initial={
                'resume': application.resume
            }
        )
    
    return render_to_response(
        'applyform/resume.html',
        {
            'form': form,
            'user': request.user,
            'MEDIA_URL': settings.MEDIA_URL,
        }
    )

@login_required
def reference(request):
    if request.method == 'POST':
        form = ReferenceCheckForm(request.POST)
        if form.is_valid():
            ref_email = form.cleaned_data['email']
            refs = User.objects.filter(email=ref_email)
            if not refs:
                return render_to_response(
                    'applyform/ref_add.html',
                    {
                        'ref_email': ref_email,
                        'form': form,
                        'user': request.user,
                        'request': request,
                        'MEDIA_URL': settings.MEDIA_URL,
                    }
                )
            else:
                return render_to_response(
                    'applyform/ref_confirm.html',
                    {
                        'ref_email': ref_email,
                        'refs': refs,
                        'form': form,
                        'user': request.user,
                        'request': request,
                        'MEDIA_URL': settings.MEDIA_URL,
                    }
                )
    else:
        form = ReferenceCheckForm()
        
    return render_to_response(
        'applyform/ref_check.html',
        {
            'form': form,
            'user': request.user,
            'request': request,
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
