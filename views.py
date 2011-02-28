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
from django.core.files.uploadedfile import SimpleUploadedFile

def index(request):
    try:
        semester_accepting = Semester.accepting_semesters.get()
        return HttpResponseRedirect(reverse('apply_menu'))
    except:
        return HttpResponseRedirect(reverse('not_accepting'))



@login_required
@require_accepting
def start_app(request):
    semester_accepting = Semester.accepting_semesters.get()
    user = request.user
    profile = user.get_profile()
    student, created = profile.student_profile.get_or_create()
    app, created = student.applications.get_or_create(for_semester=semester_accepting)
    
    return HttpResponseRedirect(reverse('apply_menu'))

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
                'semester_accepting': semester_accepting,
                 'user': request.user,
                 'request': request,
                 'MEDIA_URL': settings.MEDIA_URL,
            }
        )

    return render_to_response(
        'applyform/apply_menu.html',
        {
            'reference': reference,
            'semester': semester_accepting,
            'current_app': current_app,
            'user': request.user,
            'request': request,
            'MEDIA_URL': settings.MEDIA_URL,
            'profile_complete': profile_complete
        }
    )

@login_required
@require_accepting
@require_app_started
@submit_restriction
def basic_info(request):
    user = request.user
    userprofile = user.userprofile_set.get()
    student_profile = userprofile.student_profile.get()
        
    if request.method == 'POST':
        if request.POST['update'] == "Cancel":
            return HttpResponseRedirect(reverse('apply_menu'))
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
            
            student_profile.major = form.cleaned_data['major']
            student_profile.grad_date = form.cleaned_data['grad_date']
            student_profile.semester_for_310 = form.cleaned_data['semester_for_310']
            student_profile.semester_for_311 = form.cleaned_data['semester_for_311']
            if form.cleaned_data['is_grad_student'] == u"1":
                student_profile.is_grad_student = True
            elif form.cleaned_data['is_grad_student'] == u"0":
                student_profile.is_grad_student = False
            if form.cleaned_data['is_honors_student'] == u"1":
                student_profile.is_honors_student = True
            elif form.cleaned_data['is_honors_student'] == u"0":
                student_profile.is_honors_student = False
            student_profile.save()
            
            if request.POST['update'] == "Save and Continue":
                return HttpResponseRedirect(reverse('project_select'))
            else:
                return HttpResponseRedirect(reverse('apply_menu'))
    else:
        try:
            major_pk = student_profile.major.pk
        except:
            major_pk = None
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
        
        try:
            is_grad_student = int(student_profile.is_grad_student)
        except TypeError:
            is_grad_student = None
        
        try:
            is_honors_student = int(student_profile.is_honors_student)
        except TypeError:
            is_honors_student = None
        
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
                'major': major_pk,
                'grad_date': grad_date_pk,
                'semester_for_310': semester_for_310_pk,
                'semester_for_311': semester_for_311_pk,
                'is_grad_student': is_grad_student,
                'is_honors_student': is_honors_student,
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
            interest_rating = project.projectinterest_set.get(application=application).interest_rating
        except (ProjectInterest.DoesNotExist, ProjectInterest.MultipleObjectsReturned):
            interest_rating = None
        
        initial_data.append({
            'project_name': project.project_name,
            'project_purpose': project.project_purpose,
            'meeting_times': project.meeting_times,
            'sponsors_string': project.sponsors_string,
            'project': project.pk,
            'interest_rating': interest_rating,
            'project_coaches': project.coach_set.all(),
        })

    from django.forms.formsets import formset_factory
    ProjectSelectFormSet = formset_factory(ProjectSelectForm, extra=0)
    if request.method == 'POST':
        if request.POST['update'] == "Cancel":
            return HttpResponseRedirect(reverse('apply_menu'))
        formset = ProjectSelectFormSet(request.POST)
        if formset.is_valid():
            for i in range(int(request.POST['form-TOTAL_FORMS'])):
                project_interest, created = application.projectinterest_set.get_or_create(
                    project=Project.objects.get(pk=formset.forms[i].cleaned_data['project'])
                )
                if formset.forms[i].cleaned_data['interest_rating'] == u'':
                    project_interest.interest_rating = None
                else:
                    project_interest.interest_rating = formset.forms[i].cleaned_data['interest_rating']
                project_interest.save()
            if request.POST['update'] == "Save and Continue":
                return HttpResponseRedirect(reverse('cover_letter'))
            else:
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
        if request.POST['update'] == "Cancel":
            return HttpResponseRedirect(reverse('apply_menu'))
        form = CoverLetterForm(request.POST)
        if form.is_valid():
            application.cover_letter = form.cleaned_data['cover_letter'].replace(
                '&lt;!--', '<!--').replace('--&gt;', '-->')
            application.save()
            if request.POST['update'] == "Save and Continue":
                return HttpResponseRedirect(reverse('reference'))
            else:
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
    user = request.user
    userprofile = user.userprofile_set.get()
    student_profile = userprofile.student_profile.get()
    application = student_profile.applications.get(for_semester=semester_accepting)
    try:
        reference = Reference.objects.get(applications=application)
    except Reference.DoesNotExist:
        reference = None
    if request.method == 'POST':
        if request.POST['update'] == "Cancel":
            return HttpResponseRedirect(reverse('apply_menu'))
        form = ReferenceForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            new_reference, created = Reference.objects.get_or_create(email=email)
            if created:
                new_reference.first_name = first_name
                new_reference.last_name = last_name
                new_reference.save()
            
            try:
                previous_rr = ReferenceRating.objects.get(application=application)
                previous_rr.delete()
            except ReferenceRating.DoesNotExist:
                pass
            
            ReferenceRating.objects.get_or_create(application=application, reference=new_reference)
            
            if request.POST['update'] == "Save and Continue":
                return HttpResponseRedirect(reverse('resume_upload'))
            else:
                return HttpResponseRedirect(reverse('apply_menu'))
    else:
        form = ReferenceForm()
        
    return render_to_response(
        'applyform/reference_edit.html',
        {
            'reference': reference,
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
    
    project_interests = ProjectInterest.objects.filter(
        project=project).filter(
            interest_rating__isnull=False).filter(
                interest_rating__gt=0).filter(application__is_submitted=True)
    order = ''
    order_type = ''
    if request.GET.has_key('o'):
        order = request.GET['o']
        if request.GET.has_key('ot'):
            order_type = request.GET['ot']
            if order_type == 'asc':
                if order == '1':
                    project_interests = project_interests.order_by('application__student__profile__user__last_name')
                elif order == '2':
                    project_interests = project_interests.order_by('interest_rating')
                elif order == '3':
                    project_interests = project_interests.order_by('application__student__major')
                elif order == '4':
                    project_interests = project_interests.order_by('application__student__grad_date')
                elif order == '5':
                    project_interests = project_interests.order_by('application__student__semester_for_311')
                elif order == '6':
                    project_interests = project_interests.order_by('-application__student__is_grad_student')
                elif order == '7':
                    project_interests = project_interests.order_by('-application__student__is_honors_student')
                else:
                    pass
            else:
                order_type = 'dsc'
                if order == '1':
                    project_interests = project_interests.order_by('-application__student__profile__user__last_name')
                elif order == '2':
                    project_interests = project_interests.order_by('-interest_rating')
                elif order == '3':
                    project_interests = project_interests.order_by('-application__student__major')
                elif order == '4':
                    project_interests = project_interests.order_by('-application__student__grad_date')
                elif order == '5':
                    project_interests = project_interests.order_by('-application__student__semester_for_311')
                elif order == '6':
                    project_interests = project_interests.order_by('application__student__is_grad_student')
                elif order == '7':
                    project_interests = project_interests.order_by('application__student__is_honors_student')                    
                else:
                    pass
    
    try:
        coach_profile = userprofile.coach_profile.get()
    except Coach.DoesNotExist:
        # TODO: Make this redirect to a page explaining User is not a coach.
        # Actually... change it to display the error on the page without a
        # redirect
        return HttpResponseRedirect(reverse('login'))
    
    try:
        coach_profile.projects.get(pk=project.pk)
    except Project.DoesNotExist:
        # TODO: Display an error that this coach is not a member of this
        # project instead of redirecting to not_accepting page.
        return HttpResponseRedirect(reverse('login'))

    return render_to_response(
        'applyform/coach_list_students.html',
        {
            'project_interests': project_interests,
            'project': project,
            'user': user,
            'request': request,
            'MEDIA_URL': settings.MEDIA_URL,
            'project_id': project_id,
            'ot': order_type,
            'o': order,
        }
    )

@login_required
def apps_detail(request, app_id):
    application = Application.objects.get(pk=app_id)
    user = request.user
    
    from applyform.lib.plaintext2html import plaintext2html
    cover_letter = plaintext2html(application.cover_letter)
    
    return render_to_response(
        'applyform/app_detail.html',
        {
            'app': application,
            'cover_letter': cover_letter,
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
                'z-id',
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
                'is_assistant_coach',
                'tshirt_size',
                'honors_student',
                'major',
                'anticipated_graduation_date',
            ])
            
            for consultant in consultants:
                try:
                    major_title = consultant.student.major.title
                except AttributeError:
                    major_title = ""
                    
                project = consultant.projects.get(semester=semester)
                writer.writerow([
                    consultant.student.profile.user.username,
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
                    'False',
                    consultant.student.profile.tshirt_size,
                    consultant.student.is_honors_student,
                    major_title,
                    consultant.student.grad_date,
                ])
                
            for assistant_coach in assistant_coaches:
                try:
                    major_title = assistant_coach.student.major.title
                except AttributeError:
                    major_title = ""
                    
                project = assistant_coach.projects.get(semester=semester)
                writer.writerow([
                    assistant_coach.student.profile.user.username,
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
                    'True',
                    assistant_coach.student.profile.tshirt_size,
                    assistant_coach.student.is_honors_student,
                    major_title,
                    assistant_coach.student.grad_date,
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
                'z-id',
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
                'is_assistant_coach',
                'tshirt_size',
                'honors_student',
                'major',
            ])
            
            for consultant in consultants:
                try:
                    major_title = consultant.student.major.title
                except AttributeError:
                    major_title = ""
                    
                writer.writerow([
                    consultant.student.profile.user.username,
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
                    'False',
                    consultant.student.profile.tshirt_size,
                    consultant.student.is_honors_student,
                    major_title,
                ])
                
            for assistant_coach in assistant_coaches:
                try:
                    major_title = assistant_coach.student.major.title
                except AttributeError:
                    major_title = ""
                    
                writer.writerow([
                    assistant_coach.student.profile.user.username,
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
                    'True',
                    assistant_coach.student.profile.tshirt_size,
                    assistant_coach.student.is_honors_student,
                    major_title,
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

@login_required
@require_accepting
@require_app_started
@submit_restriction
def resume_upload(request):
    from applyform.lib.file_handlers import handle_uploaded_resume
    
    semester_accepting = Semester.accepting_semesters.get()
    user = request.user
    userprofile = user.userprofile_set.get()
    student_profile = userprofile.student_profile.get()
    application = student_profile.applications.get(for_semester=semester_accepting)
    
    if request.method == 'POST':
        if request.POST['update'] == "Cancel":
            return HttpResponseRedirect(reverse('apply_menu'))
        form = ResumeUploadForm(request.POST, request.FILES)
        if form.is_valid():
            filename = handle_uploaded_resume(request.FILES['file_upload'], request.user.username)
            if application.resume:
                import os
                old_filename = application.resume.file.name
                application.resume = None
                application.save()
                os.remove(old_filename)
                
            application.resume = filename
            application.save()
            if request.POST['update'] == "Save and Continue":
                return HttpResponseRedirect(reverse('finalize_submission'))
            else:
                return HttpResponseRedirect(reverse('apply_menu'))
    else:
        form = ResumeUploadForm()
        return render_to_response(
            'applyform/resume_upload.html',
            {
                'application': application,
                'form': form,
                'user': request.user,
                'request': request,
                'MEDIA_URL': settings.MEDIA_URL,
            }
       )

@login_required
@require_accepting
@require_app_started
@submit_restriction
def finalize_submission(request):
    semester_accepting = Semester.accepting_semesters.get()
    user = request.user
    userprofile = user.userprofile_set.get()
    student_profile = userprofile.student_profile.get()
    application = student_profile.applications.get(for_semester=semester_accepting)
    try:
        reference = application.get_reference()
    except Reference.DoesNotExist:
        reference = None
        
    if userprofile.profile_info_completed() and application.is_complete() and \
       application.cover_letter and reference and application.resume:
        if request.method == "POST":
            if request.POST['update'] == "Cancel":
                return HttpResponseRedirect(reverse('apply_menu'))
            form = FinalizeSubmissionForm(request.POST)
            if form.is_valid():
                understand = form.cleaned_data['understand']
                if understand:
                    from applyform.lib.mailer import Mailer
                    
                    email_body = """
You have successfully submitted your application to the ELC.
You will be notified of your application's status the week of November 1st.

If you had any difficulties with the online application process, please email
Matthew Janouskovec at mjanous@niu.edu or call him at (815)501-4446.
"""
                    m = Mailer(user.email, email_body)
                    application.is_submitted = True
                    application.date_submitted = datetime.now()
                    application.save()
                    m.mail_it()
                    return HttpResponseRedirect(reverse('thanks'))
        
        else:
            form = FinalizeSubmissionForm()
            from applyform.lib.plaintext2html import plaintext2html
            cover_letter = plaintext2html(application.cover_letter)
            return render_to_response(
                'applyform/finalize_submission.html',
                {
                    'is_complete': True,
                    'form': form,
                    'application': application,
                    'cover_letter': cover_letter,
                    'user': request.user,
                    'userprofile': userprofile,
                    'student_profile': student_profile,
                    'request': request,
                    'MEDIA_URL': settings.MEDIA_URL,
                }
            )
    else:
        return render_to_response(
            'applyform/finalize_submission.html',
            {
                'is_complete': False,
                'application': application,
                'user': request.user,
                'userprofile': userprofile,
                'student_profile': student_profile,
                'request': request,
                'MEDIA_URL': settings.MEDIA_URL,
            }
)
    
def not_accepting(request):
    not_accepting_text = Config.objects.get(name="not_accepting_text").value
    user = request.user
    return render_to_response(
        'applyform/not_accepting.html',
        {
            'text': not_accepting_text,
            'MEDIA_URL': settings.MEDIA_URL,
            'request': request,
            'user': user,
        }
    )

def thanks(request):
    user = request.user
    return render_to_response(
        'applyform/thanks.html',
        {
            'MEDIA_URL': settings.MEDIA_URL,
            'request': request,
            'user': user,
        }
    )

def error_500(request):
    user = request.user
    return render_to_response(
        '500.html',
        {
            'MEDIA_URL': settings.MEDIA_URL,
            'request': request,
            'user': user,
        }
    )

def upcoming_project_list(request):
    from datetime import datetime
    now = datetime.now()
    user = request.user
    projects = Project.objects.filter(semester__start_date__gt=now)
    return render_to_response(
        'applyform/upcoming_project_list.html',
        {
            'MEDIA_URL': settings.MEDIA_URL,
            'request': request,
            'user': user,
            'projects': projects,
        }
    )

def applicant_list(request):
    if request.method == 'POST':
        form = ApplicantListForm(request.POST)
        if form.is_valid():
            semester = form.cleaned_data['semester']
            applications = Application.objects.filter(for_semester=semester).filter(is_submitted=True)
            projects = Project.objects.filter(semester=semester)
            headers = [
                'z-id',
                'first_name',
                'last_name',
                'email',
                'major',
                'is_honors?',
                'is_grad?',
                'grad_date',
                'ref_first_name',
                'ref_last_name',
                'ref_email',
            ]
            for project in projects:
                headers.append(project.sponsors_string)
                
            response = HttpResponse(mimetype='text/csv')
            response['Content-Disposition'] = 'attachment; filename=report.csv'
            writer = csv.writer(response)
            writer.writerow(headers)
            
            for application in applications:
                try:
                    major_title = application.student.major.title
                except AttributeError:
                    major_title = ""
                try:
                    reference_first_name = application.get_reference().first_name
                except:
                    reference_first_name = None
                try:
                    reference_last_name = application.get_reference().last_name
                except:
                    reference_last_name = None
                try:
                    reference_email = application.get_reference().email
                except:
                    reference_email = None

                columns = [
                    application.student.profile.user.username,
                    application.student.profile.user.first_name,
                    application.student.profile.user.last_name,
                    application.student.profile.user.email,
                    major_title,
                    application.student.is_honors_student,
                    application.student.is_grad_student,
                    application.student.grad_date,
                    reference_first_name,
                    reference_last_name,
                    reference_email,
                ]
                
                for project in projects:
                    try:
                        interest_rating = application.projectinterest_set.filter(project=project)[0].interest_rating
                    except:
                        interest_rating = None
                    columns.append(interest_rating)
                    
                writer.writerow(columns)
            return response
            
    else:
        form = ApplicantListForm()
        
    return render_to_response(
        'applyform/applicant_list.html',
        {
            'form': form,
            'user': request.user,
            'request': request,
            'MEDIA_URL': settings.MEDIA_URL,
        }
   )
