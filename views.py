import csv

from django.views.generic import list_detail
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from applyform.models import *
from applyform.forms import *
from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required
from django.core.urlresolvers import reverse
from applyform.lib.decorators import (
    submit_restriction, require_accepting, require_app_started, require_student_profile)

def index(request):
    try:
        semester_accepting = Semester.accepting_semesters.get()
    except (Semester.DoesNotExist, Semester.MultipleObjectsReturned):
        semester_accepting = False
    return render_to_response(
        'applyform/index.html',
        {
            'semester_accepting': semester_accepting,
            'user': request.user,
            'request': request,
            'MEDIA_URL': settings.MEDIA_URL,
        }
    )

@login_required
@require_accepting
@require_student_profile
def apply_menu(request):
    semester_accepting = Semester.accepting_semesters.get()
    user = request.user
    profile_complete = False
    userprofile = user.get_profile()
    profile_complete = userprofile.profile_info_completed()
    
    try:
        student_profile = userprofile.student_profile.get()
        current_app = student_profile.applications.get(for_semester=semester_accepting)
        reference = current_app.get_reference()
    except (Student.DoesNotExist, Application.DoesNotExist, Reference.DoesNotExist, UnboundLocalError):
        return render_to_response(
            'applyform/start_app.html',
            {
                'semester': semester_accepting,
                'user': request.user,
                'request': request,
                'MEDIA_URL': settings.MEDIA_URL,
                'profile_complete': profile_complete
            }
        )

    try:
        current_app_complete = current_app.is_complete()
    except:
        current_app_complete = False

    return render_to_response(
        'applyform/apply_menu.html',
        {
            'reference': reference,
            'semester': semester_accepting,
            'current_app_complete': current_app_complete,
            'user': request.user,
            'request': request,
            'MEDIA_URL': settings.MEDIA_URL,
            'profile_complete': profile_complete
        }
    )

@login_required
@require_student_profile
def basic_info(request):
    user = request.user
    userprofile = user.userprofile_set.get()
    student_profile = userprofile.student_profile.get()
        
    if request.method == 'POST':
        form = BasicInfoForm(request.POST)
        if form.is_valid():
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.save()
            
            userprofile.address1 = form.cleaned_data['address1']
            userprofile.address2 = form.cleaned_data['address2']
            userprofile.city = form.cleaned_data['city']
            userprofile.state = form.cleaned_data['state']
            if form.cleaned_data['zipcode'] == u'':
                userprofile.zipcode = None
            else:
                userprofile.zipcode = form.cleaned_data['zipcode'] 
            userprofile.home_phone = form.cleaned_data['home_phone']
            userprofile.mobile_phone = form.cleaned_data['mobile_phone']
            userprofile.tshirt_size = form.cleaned_data['tshirt_size']
            userprofile.save()
            
            student_profile.grad_date = form.cleaned_data['grad_date']
            student_profile.semester_for_310 = form.cleaned_data['semester_for_310']
            student_profile.semester_for_311 = form.cleaned_data['semester_for_311']            
            student_profile.is_grad_student = form.cleaned_data['is_grad_student']
            student_profile.is_honors_student = form.cleaned_data['is_honors_student']
            student_profile.save() 
            return HttpResponseRedirect(reverse('apply_menu'))
    else:
        try:
            grad_date_pk = student_profile.grad_date.pk
        except AttributeError:
            grad_date_pk = None
        try:
            semester_for_310_pk = student_profile.semester_for_310.pk
        except AttributeError:
            semester_for_310_pk = None
        try:
            semester_for_311_pk = student_profile.semester_for_311.pk
        except AttributeError:
            semester_for_311_pk = None
            
        form = BasicInfoForm(
            initial={
                'first_name': user.first_name,
                'last_name': user.last_name,
                'address1': userprofile.address1,
                'address2': userprofile.address2,
                'city': userprofile.city,
                'state': userprofile.state,
                'zipcode': userprofile.zipcode,
                'email': user.email,
                'home_phone': userprofile.home_phone,
                'mobile_phone': userprofile.mobile_phone,
                'grad_date': grad_date_pk,
                'semester_for_310': semester_for_310_pk,
                'semester_for_311': semester_for_311_pk,
                'is_grad_student': student_profile.is_grad_student,
                'is_honors_student': student_profile.is_honors_student,
                'tshirt_size' : userprofile.tshirt_size
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
@require_accepting
@require_app_started
@submit_restriction
def project_select(request):
    semester_accepting = Semester.accepting_semesters.get()
    user = request.user
    userprofile = user.userprofile_set.get()
    student_profile = userprofile.student_profile.get()
    projects = semester_accepting.project_set.all()
    application = student_profile.applications.get(for_semester=semester_accepting)
    
    initial_data = []
    for project in projects:
        try:
            is_interested = project.projectinterest_set.get(application=application).is_interested
        except (ProjectInterest.DoesNotExist, ProjectInterest.MultipleObjectsReturned):
            is_interested = None
        
        initial_data.append({
            'project_name': project.project_name,
            'project': project.pk, 'is_interested': is_interested
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
                project_interest.is_interested = formset.forms[i].cleaned_data['is_interested']
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
@require_accepting
@require_app_started
@submit_restriction
def cover_letter(request):
    semester_accepting = Semester.accepting_semesters.get()
    user = request.user
    userprofile = user.userprofile_set.get()
    student_profile = userprofile.student_profile.get()
    projects = semester_accepting.project_set.all()
    application = student_profile.applications.get(for_semester=semester_accepting)
    
    if request.method == 'POST':
        form = CoverLetterForm(request.POST)
        if form.is_valid():
            application.cover_letter = form.cleaned_data['cover_letter'].replace(
                '&lt;!--', '<!--').replace('--&gt;', '-->')
            application.save()
            return HttpResponseRedirect(reverse('apply_menu'))
    else:
        form = CoverLetterForm(
            initial={
                'cover_letter': application.cover_letter
            }
        )
    
    return render_to_response(
        'applyform/cover_letter.html',
        {
            'form': form,
            'user': request.user,
            'MEDIA_URL': settings.MEDIA_URL,
        }
    )

@login_required
@require_accepting
@require_app_started
@submit_restriction
def reference(request):
    semester_accepting = Semester.accepting_semesters.get()
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

@login_required
def reference_rate(request):
    if request.method == 'POST':
        form = ReferenceRatingForm(request.POST)
        if form.is_valid():
            # TODO
            pass
        else:
            # TODO
            pass
    else:
        # TODO
        form = ReferenceRatingForm()
        
    return render_to_response(
        'applyform/ref_check.html',
        {
            'form': form,
            'user': request.user,
            'request': request,
            'MEDIA_URL': settings.MEDIA_URL,
        }
    )

@login_required
def coach_list_projects(request):
    user=request.user
    userprofile, _ = user.userprofile_set.get_or_create()
    try:
        coach_profile = userprofile.coach_profile.get()
    except Coach.DoesNotExist:
        # TODO: Make this redirect to a page explaining User is not a coach.
        return HttpResponseRedirect(reverse('not_accepting'))
    
    try:
        projects = coach_profile.projects.all()
    except:
        projects = None
    
    return render_to_response(
        'applyform/coach_list_projects.html',
        {
            'projects': projects,
            'user': user,
            'request': request,
            'MEDIA_URL': settings.MEDIA_URL,
        }
    )

@login_required
def coach_list_students(request, project_id):
    user=request.user
    userprofile, _ = user.userprofile_set.get_or_create()
    project = Project.objects.get(pk=project_id)
    apps = project.applications.filter(
        is_submitted=True).filter(projectinterest__is_interested=True)
    
    try:
        coach_profile = userprofile.coach_profile.get()
    except Coach.DoesNotExist:
        # TODO: Make this redirect to a page explaining User is not a coach.
        # Actually... change it to display the error on the page without a
        # redirect
        return HttpResponseRedirect(reverse('not_accepting'))
    
    try:
        coach_profile.projects.get(pk=project.pk)
    except Project.DoesNotExist:
        # TODO: Display an error that this coach is not a member of this
        # project instead of redirecting to not_accepting page.
        return HttpResponseRedirect(reverse('not_accepting'))
    
    return render_to_response(
        'applyform/coach_list_students.html',
        {
            'apps': apps,
            'project': project,
            'user': user,
            'request': request,
            'MEDIA_URL': settings.MEDIA_URL,
        }
    )

@login_required
def apps_detail(request, app_id):
    application = Application.objects.get(pk=app_id)
    user = request.user
    
    return render_to_response(
        'applyform/app_detail.html',
        {
            'app': application,
            'user': user,
            'request': request,
            'MEDIA_URL': settings.MEDIA_URL,
        }
    )

@login_required
@permission_required('is_staff')
def student_contact_report_by_semester(request):
    if request.method == 'POST':
        form = ReportSemesterForm(request.POST)
        if form.is_valid():
            semester = form.cleaned_data['semester']
            consultants = Consultant.objects.filter(projects__semester=semester)
            assistant_coaches = AssistantCoach.objects.filter(projects__semester=semester)
            response = HttpResponse(mimetype='text/csv')
            response['Content-Disposition'] = 'attachment; filename=report.csv'
            writer = csv.writer(response)
            writer.writerow([
                'first_name',
                'last_name',
                'email',
                'semester',
                'project_sponsor',
                'project_name',
                'address1',
                'address2',
                'city',
                'state',
                'zip',
                'is_assistant_coach'
            ])
            
            for consultant in consultants:
                project = consultant.projects.get(semester=semester)
                writer.writerow([
                    consultant.student.profile.user.first_name,
                    consultant.student.profile.user.last_name,
                    consultant.student.profile.user.email,
                    semester.__unicode__(),
                    project.sponsors_string,
                    project.project_name,
                    consultant.student.profile.address1,
                    consultant.student.profile.address2,
                    consultant.student.profile.city,
                    consultant.student.profile.state,
                    consultant.student.profile.zipcode,
                    'False'
                ])
                
            for assistant_coach in assistant_coaches:
                project = assistant_coach.projects.get(semester=semester)
                writer.writerow([
                    assistant_coach.student.profile.user.first_name,
                    assistant_coach.student.profile.user.last_name,
                    assistant_coach.student.profile.user.email,
                    semester.__unicode__(),
                    project.sponsors_string,
                    project.project_name,
                    assistant_coach.student.profile.address1,
                    assistant_coach.student.profile.address2,
                    assistant_coach.student.profile.city,
                    assistant_coach.student.profile.state,
                    assistant_coach.student.profile.zipcode,
                    'True'
                ])
                
            return response

    else:
        form = ReportSemesterForm()
        
    return render_to_response(
        'applyform/report_semester.html',
        {
            'form': form,
            'user': request.user,
            'request': request,
            'MEDIA_URL': settings.MEDIA_URL,
        }
    )

@login_required
@permission_required('is_staff')
def student_contact_report_by_project(request):
    if request.method == 'POST':
        form = ReportProjectForm(request.POST)
        if form.is_valid():
            project = form.cleaned_data['project']
            consultants = Consultant.objects.filter(projects=project)
            assistant_coaches = AssistantCoach.objects.filter(projects=project)
            semester = project.semester
        
            response = HttpResponse(mimetype='text/csv')
            response['Content-Disposition'] = 'attachment; filename=report.csv'
            
            writer = csv.writer(response)
            writer.writerow([
                'first_name',
                'last_name',
                'email',
                'semester',
                'project_sponsor',
                'project_name',
                'address1',
                'address2',
                'city',
                'state',
                'zip',
                'is_assistant_coach'
            ])
            
            for consultant in consultants:
                writer.writerow([
                    consultant.student.profile.user.first_name,
                    consultant.student.profile.user.last_name,
                    consultant.student.profile.user.email,
                    semester.__unicode__(),
                    project.sponsors_string,
                    project.project_name,
                    consultant.student.profile.address1,
                    consultant.student.profile.address2,
                    consultant.student.profile.city,
                    consultant.student.profile.state,
                    consultant.student.profile.zipcode,
                    'False'
                ])
                
            for assistant_coach in assistant_coaches:
                writer.writerow([
                    assistant_coach.student.profile.user.first_name,
                    assistant_coach.student.profile.user.last_name,
                    assistant_coach.student.profile.user.email,
                    semester.__unicode__(),
                    project.sponsors_string,
                    project.project_name,
                    assistant_coach.student.profile.address1,
                    assistant_coach.student.profile.address2,
                    assistant_coach.student.profile.city,
                    assistant_coach.student.profile.state,
                    assistant_coach.student.profile.zipcode,
                    'True'
                ])
                
            return response
    
    else:
        form = ReportProjectForm()
        
    return render_to_response(
        'applyform/report_project.html',
        {
            'form': form,
            'user': request.user,
            'request': request,
            'MEDIA_URL': settings.MEDIA_URL,
        }
    )

@login_required
@permission_required('is_staff')
def project_list(request, page):
    order = ''
    order_type = ''
    
    if request.GET.has_key('o'):
        order = request.GET['o']
        if request.GET.has_key('ot'):
            order_type = request.GET['ot']
            if order_type == 'asc':
                if order == 'name':
                    query = Project.objects.all().order_by('project_name')
                elif order == 'semester':
                    query = Project.objects.all().order_by('semester')
                else:
                    query = Project.objects.all()
            else:
                order_type = 'dsc'
                if order == 'name':
                    query = Project.objects.all().order_by('-project_name')
                elif order == 'semester':
                    query = Project.objects.all().order_by('-semester')
                else:
                    query = Project.objects.all()
    else:
        query = Project.objects.all()
        
    return list_detail.object_list(
        request,
        queryset=query,
        template_name='applyform/project_list.html',
        paginate_by=30,
        page=page,
        extra_context={'ot': order_type, 'o': order},
    )

@login_required
@permission_required('is_staff')
def project_detail(request, object_id):
    return list_detail.object_detail(
        request,
        queryset=Project.objects.all(),
        template_name='applyform/project_detail.html',
        object_id=object_id,
    )