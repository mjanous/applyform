from django.db import models
from django.contrib.localflavor.us.models import PhoneNumberField, USStateField
from django.contrib.auth.models import User

class AcceptingAppsManager(models.Manager):
    '''This manager goes with the Semester model to return a queryset of
    semesters that we are currently accepting applications for.'''
    def get_query_set(self):
        from datetime import datetime
        now = datetime.now()
        return super(AcceptingAppsManager, self).get_query_set().filter(
            accepting_start_date__lte=now, accepting_end_date__gte=now
        )

class CurrentAppsManager(models.Manager):
    '''This manager goes with the Applications model to return a queryset
    of applications that are for the current semester(s) we're accepting
    apps for.'''
    def get_query_set(self):
        from datetime import datetime
        now = datetime.now()
        return super(CurrentAppsManager, self).get_query_set().filter(
            for_semester__accepting_start_date__lte=now,
            for_semester__accepting_end_date__gte=now,
        )
    
class AcceptingAppsProjectsManager(models.Manager):
    '''This manager goes with the Projects model to return a queryset of
    projects that students are allowed to apply for, for the next semester'''
    def get_query_set(self):
        from datetime import datetime
        now = datetime.now()
        return super(AcceptingAppsProjectsManager, self).get_query_set().filter(
            semester__accepting_start_date__lte=now,
            semester__accepting_end_date__gte=now,
        )

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    dob = models.DateField(blank=True, null=True)
    address1 = models.CharField(max_length=40, blank=True)
    address2 = models.CharField(max_length=40, blank=True)
    city = models.CharField(max_length=40, blank=True)
    state = USStateField(blank=True)
    zipcode = models.IntegerField(max_length=5, blank=True, null=True)
    home_phone = PhoneNumberField(blank=True)
    mobile_phone = PhoneNumberField(blank=True)
    bio = models.TextField(blank=True)
    
    def __unicode__(self):
        return self.user.username
    
    def profile_info_completed(self):
        '''This method determines if all the required fields for a correct
        application are filled out'''
        try:
            if (
                (self.user.first_name) and
                (self.user.last_name) and 
                (self.dob) and
                (self.address1) and
                (self.city) and
                (self.state) and
                (self.zipcode) and
                (self.home_phone or self.mobile_phone) and
                (self.student_profile.get().grad_date) and
                (self.student_profile.get().grad_status is not None) and
                (self.student_profile.get().enrollment_status is not None) and
                (self.student_profile.get().honors_status is not None)
            ):
                return True
            else:
                return False
        except:
            return False
            
        
class Student(models.Model):
    profile = models.ForeignKey(UserProfile, unique=True, related_name='student_profile')
    major = models.ForeignKey('Major', related_name='student_set', null=True, blank=True)
    grad_date = models.ForeignKey('Semester', blank=True, null=True)
    grad_status = models.NullBooleanField(
        verbose_name='Graduate Student?',
        help_text='Check this box if you are a graduate student',
        blank=True,
        null=True,
    )
    enrollment_status = models.NullBooleanField(
        verbose_name='Enrolled in or have completed UBUS 311',
    )
    honors_status = models.NullBooleanField(
        verbose_name='Honors Student?',
    )
    hear_about_us = models.CharField(max_length=60, blank=True)
    
    def __unicode__(self):
        return self.profile.user.username
    
    def get_current_applications(self):
        '''This method retrieves the student's applications for the semester(s)
        that are accepting applications. Will return DoesNotExist errors if
        there is no current semester or no application for that semester.'''
        accepting_semesters = Semester.accepting_semesters.all()
        applications = []
        for semester in accepting_semesters:
            try:
                applications.append(self.applications.get(for_semester=semester))
            except Application.DoesNotExist:
                pass
            
        return applications
            
    
class Consultant(models.Model):
    student = models.ForeignKey(
        Student, related_name='consultant_profile')
    project = models.ManyToManyField(
        'Project', related_name='students')
    
    def __unicode__(self):
        return self.student.profile.user.username
    
class AssistantCoach(models.Model):
    student = models.ForeignKey(
        Student, related_name='assistant_coach_profile')
    project = models.ManyToManyField(
        'Project', related_name='assistant_coaches')
    
    def __unicode__(self):
        return self.student.profile.user.username
    
    class Meta:
        verbose_name_plural = "Assistant coaches"
    
class Coach(models.Model):
    profile = models.ForeignKey(
        UserProfile, unique=True, related_name='coach_profile')
    project = models.ManyToManyField('Project', related_name='coaches')

    def __unicode__(self):
        return self.profile.user.username
    
    class Meta:
        verbose_name_plural = "Coaches"

class Reference(models.Model):
    profile = models.ForeignKey(
        UserProfile, unique=True, related_name='reference_profile')
    students = models.ManyToManyField(
        Student, through='ReferenceRating')

class Application(models.Model):
    student = models.ForeignKey(Student, related_name='applications')
    project_interests = models.ManyToManyField(
        'Project', through='ProjectInterest', related_name='applications')
    submitted = models.BooleanField('Application submitted?')
    date_submitted = models.DateField(blank=True, null=True)
    for_semester = models.ForeignKey('Semester', related_name='applications')
    
    # Managers
    objects = models.Manager()
    current_apps = CurrentAppsManager()    
    
    def __unicode__(self):
        return self.student.profile.user.username
    
    class Meta:
        unique_together = ('student', 'for_semester')

class Semester(models.Model):
    year = models.IntegerField()
    season = models.CharField(max_length=6)
    start_date = models.DateField()
    end_date = models.DateField()
    accepting_start_date = models.DateField(blank=True, null=True)
    accepting_end_date = models.DateField(blank=True, null=True)
    
    # Managers
    objects = models.Manager()
    accepting_semesters = AcceptingAppsManager()

    def __unicode__(self):
        return ' '.join((self.season, str(self.year)))
    
    class Meta:
        ordering = ['-start_date']
    
class Project(models.Model):
    project_name = models.CharField(max_length=60)
    semester = models.ForeignKey(Semester, related_name='project_set')
    sponsor = models.ForeignKey('Sponsor', related_name='project_set')
    sponsor_contacts = models.ManyToManyField('SponsorContact', related_name='projects', blank=True)
    
    # Managers
    objects = models.Manager()
    accepting_apps = AcceptingAppsProjectsManager()
    
    def __unicode__(self):
        return self.project_name
    
class Sponsor(models.Model):
    sponsor_name = models.CharField(max_length=60)
    
    def __unicode__(self):
        return self.sponsor_name
 
class ProjectInterest(models.Model):
    application = models.ForeignKey(Application)
    project = models.ForeignKey(Project)
    score = models.IntegerField(max_length=2)
    
    def __unicode__(self):
        return ' '.join((
            self.application.student.profile.user.username,
            self.project.project_name
        ))
    
    class Meta:
        unique_together = ('application', 'project')
        
class ReferenceRating(models.Model):
    reference = models.ForeignKey(Reference)
    student = models.ForeignKey(Student)
    rating = models.IntegerField(max_length=2)
    
class SponsorContact(models.Model):
    company = models.ForeignKey(Sponsor, related_name='contact_set')
    first_name = models.CharField(max_length=40, blank=True)
    last_name = models.CharField(max_length=40, blank=True)
    title = models.CharField(max_length=40, blank=True)
    address1 = models.CharField(max_length=40, blank=True)
    address2 = models.CharField(max_length=40, blank=True)
    city = models.CharField(max_length=40, blank=True)
    state = USStateField(blank=True)
    zipcode = models.IntegerField(max_length=5, blank=True, null=True)
    
    def __unicode__(self):
        return ' '.join((self.first_name, self.last_name))
    
class Keycard(models.Model):
    owner = models.ForeignKey(UserProfile, related_name='keycard_set')
    number = models.IntegerField(max_length=20)
    returned = models.BooleanField()
    
    def __unicode__(self):
        return self.owner.user.username
    
class Resume(models.Model):
    application = models.ForeignKey(Application, related_name='resume')
    resume_file = models.FileField(upload_to='resumes')
    
    def __unicode__(self):
        return self.application.student.profile.user.username

class Major(models.Model):
    title = models.CharField(max_length=50)
    college = models.ForeignKey('College', related_name='majors')
    
    def __unicode__(self):
        return self.title
        
class College(models.Model):
    name = models.CharField(max_length=40)
    
    def __unicode__(self):
        return self.name