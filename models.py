from django.db import models
from django.contrib.localflavor.us.models import PhoneNumberField
from applyform.lib.us.models import USStateField
from applyform.lib.shirts.models import ShirtSizeField
from django.contrib.auth.models import User
from django.conf import settings

User._meta.ordering = ['last_name', 'first_name']

class AcceptingAppsManager(models.Manager):
    """Manager class for Semester model
    
    Queryset is of all semesters that we are currently accepting
    applications for.
    
    """
    def get_query_set(self):
        from datetime import datetime
        now = datetime.now()
        return super(AcceptingAppsManager, self).get_query_set().filter(
            accepting_start_date__lte=now, accepting_end_date__gte=now
        )

class CurrentAppsManager(models.Manager):
    """Manager class for Application model
    
    Queryset is of all applications for the semesters we are currently
    accepting applications fstor.
    
    """    
    def get_query_set(self):
        from datetime import datetime
        now = datetime.now()
        return super(CurrentAppsManager, self).get_query_set().filter(
            for_semester__accepting_start_date__lte=now,
            for_semester__accepting_end_date__gte=now,
        )
    
class AcceptingAppsProjectsManager(models.Manager):
    """Manager class for the Project model
    
    Queryset is of all projects that students are allowed to apply for.
    
    """
    def get_query_set(self):
        from datetime import datetime
        now = datetime.now()
        return super(AcceptingAppsProjectsManager, self).get_query_set().filter(
            semester__accepting_start_date__lte=now,
            semester__accepting_end_date__gte=now,
        )

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    address1 = models.CharField(max_length=40, blank=True)
    address2 = models.CharField(max_length=40, blank=True)
    city = models.CharField(max_length=40, blank=True)
    state = USStateField(blank=True)
    zipcode = models.IntegerField(max_length=5, blank=True, null=True)
    home_phone = PhoneNumberField(blank=True)
    mobile_phone = PhoneNumberField(blank=True)
    bio = models.TextField(blank=True)
    keycards = models.ManyToManyField(
        'Keycard', related_name='owner', through='AssignedKeycard', blank=True
    )
    tshirt_size = ShirtSizeField(max_length=10, blank=True)
    
    def __unicode__(self):
        return ''.join((self.user.last_name, ', ', self.user.first_name, ' - ', self.user.username,))
    
    def profile_info_completed(self):
        """
        Returns True if if all the required fields for a valid
        application are filled out.
        """
        try:
            if (
                (self.user.first_name) and
                (self.user.last_name) and 
                (self.address1) and
                (self.city) and
                (self.state) and
                (self.zipcode) and
                (self.home_phone or self.mobile_phone) and
                (self.student_profile.get().grad_date) and
                (self.student_profile.get().is_grad_student is not None) and
                (self.student_profile.get().is_honors_student is not None)
            ):
                return True
            else:
                return False
        except:
            return False
        
    def current_app_is_complete(self):
        from datetime import datetime
        now = datetime.now()
        try:
            return self.student_profile.get().applications.get_query_set().filter(
                for_semester__accepting_start_date__lte=now,
                for_semester__accepting_end_date__gte=now,
            )[0].is_submitted
        except:
            return False
        
    def _get_first_name(self):
        return self.user.first_name
    first_name = property(_get_first_name)
    
    def _get_last_name(self):
        return self.user.last_name
    last_name = property(_get_last_name)
        
    class Meta:
        ordering = ['user']
            
class Student(models.Model):
    profile = models.ForeignKey(UserProfile, unique=True, related_name='student_profile')
    major = models.ForeignKey('Major', related_name='student_set', null=True, blank=True)
    grad_date = models.ForeignKey('Semester', blank=True, null=True)
    is_grad_student = models.NullBooleanField(
        verbose_name='Graduate Student?',
        help_text='Check this box if you are a graduate student',
        blank=True,
        null=True,
    )
    is_honors_student = models.NullBooleanField(
        verbose_name='Honors Student?',
    )
    hear_about_us = models.CharField(max_length=60, blank=True)
    semester_for_310 = models.ForeignKey('Semester', blank=True, null=True, related_name='310_grad')
    semester_for_311 = models.ForeignKey('Semester', blank=True, null=True, related_name='311_grad')
    
    def __unicode__(self):
        return self.profile.__unicode__()
    
    def get_current_applications(self):
        """Return a list of Application objects
        
        This method retrieves the student's applications for the semester(s)
        that are accepting applications. Will return an empty list if there
        is no current semester or if there is no application for that semester.
        
        """
        accepting_semesters = Semester.accepting_semesters.all()
        applications = []
        for semester in accepting_semesters:
            try:
                applications.append(self.applications.get(for_semester=semester))
            except Application.DoesNotExist:
                pass
            
        return applications
    
    def _get_first_name(self):
        return self.profile.user.first_name
    first_name = property(_get_first_name)
    
    def _get_last_name(self):
        return self.profile.user.last_name
    last_name = property(_get_last_name)
    
    class Meta:
        ordering = ['profile']
    
class Consultant(models.Model):
    student = models.ForeignKey(
        Student, related_name='consultant_profile', unique=True)
    projects = models.ManyToManyField(
        'Project', related_name='consultants')
    
    def __unicode__(self):
        return self.student.profile.__unicode__()
    
    class Meta:
        ordering = ['student']
    
class AssistantCoach(models.Model):
    student = models.ForeignKey(
        Student, related_name='assistant_coach_profile', unique=True)
    projects = models.ManyToManyField(
        'Project', related_name='assistant_coaches')
    
    def __unicode__(self):
        return self.student.profile.__unicode__()
    
    class Meta:
        verbose_name_plural = "Assistant coaches"
        ordering = ['student']
    
class Coach(models.Model):
    profile = models.ForeignKey(
        UserProfile, unique=True, related_name='coach_profile')
    projects = models.ManyToManyField(
        'Project', related_name='coach_set', through='ProjectCoach')
    expertise = models.TextField(blank=True)

    def __unicode__(self):
        return self.profile.__unicode__()
    
    class Meta:
        verbose_name_plural = "Coaches"
        ordering = ['profile']

class Application(models.Model):
    student = models.ForeignKey(Student, related_name='applications')
    project_interests = models.ManyToManyField(
        'Project', through='ProjectInterest', related_name='applications')
    reference = models.ManyToManyField(
        'Reference', through='ReferenceRating', related_name='applications')
    is_submitted = models.BooleanField('Application submitted?')
    date_submitted = models.DateField(blank=True, null=True)
    for_semester = models.ForeignKey('Semester', related_name='applications')
    resume = models.FileField(upload_to='resumes', blank=True, null=True)
    cover_letter = models.TextField(blank=True)
    
    # Managers
    objects = models.Manager()
    current_apps = CurrentAppsManager()    
    
    def __unicode__(self):
        return self.student.profile.user.username
    
    def is_complete(self):
        """Return true if all ProjectInterest objects are complete
        
        Find all projects that need ProjectInterest objects for the
        Application's "for_semester" field. Return False if any ProjectInterest
        object is not found or has a null for boolean interest value.
        
        """
        semester_projects = Project.objects.filter(semester=self.for_semester)
        for p in semester_projects:
            try:
                proj_interest = self.projectinterest_set.get(project=p)
                if proj_interest.interest_rating is None:
                    return False
                else:
                    pass
            except ProjectInterest.DoesNotExist:
                return False
        return True
    
    def get_reference(self):
        """Return Reference object or None if None
        
        Get the Reference object that is listed on the Application
        
        """
        try:
            reference = self.referencerating_set.get().reference
        except ReferenceRating.DoesNotExist:
            reference = None
        except ReferenceRating.MultipleObjectsReturned:
            reference = None
        
        return reference

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
    project_purpose = models.TextField(blank=True)
    semester = models.ForeignKey(Semester, related_name='project_set', blank=True, null=True)
    sponsors = models.ManyToManyField(
        'Sponsor', related_name='project_set', through='ProjectSponsor', blank=True
    )
    sponsor_contacts = models.ManyToManyField(
        'SponsorContact', related_name='projects', through='ProjectContact', blank=True
    )
    implemented_as = models.ForeignKey('ImplementationType', related_name='projects', blank=True, null=True)
    is_marketing_plan = models.BooleanField()
    is_market_research = models.BooleanField()
    is_operations = models.BooleanField()
    is_information_systems = models.BooleanField()
    is_interactive_marketing = models.BooleanField()
    is_finance = models.BooleanField()
    is_accountancy = models.BooleanField()
    is_human_resources = models.BooleanField()
    is_organizational_management = models.BooleanField()
    project_expiration = models.DateField(blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    meeting_times = models.TextField(blank=True)
    
    # Managers
    objects = models.Manager()
    accepting_apps = AcceptingAppsProjectsManager()
    
    def __unicode__(self):
        project_sponsors = []
        for sponsor in self.sponsors.all():
            project_sponsors.append(sponsor.sponsor_name)
        return ' - '.join(['\\'.join(project_sponsors), self.project_name])
    
    def _get_sponsors_string(self):
        sponsors_list = []
        for sponsor in self.sponsors.all():
            sponsors_list.append(sponsor.sponsor_name)
        return '\\'.join(sponsors_list)
    sponsors_string = property(_get_sponsors_string)
    
    @models.permalink
    def get_absolute_url(self):
        return ('project_detail', (), {
            'object_id': self.id})
    
    class Meta:
        ordering = ['project_name']
    
class ImplementationType(models.Model):
    implement = models.CharField(max_length=60)
    
    def __unicode__(self):
        return self.implement
    
class Sponsor(models.Model):
    sponsor_name = models.CharField(max_length=60)
    
    def __unicode__(self):
        return self.sponsor_name
    
    class Meta:
        ordering = ['sponsor_name']
 
class ProjectInterest(models.Model):
    application = models.ForeignKey(Application)
    project = models.ForeignKey(Project, related_name="projectinterest_set")
    interest_rating = models.IntegerField(blank=True, null=True)
    
    def __unicode__(self):
        return ' '.join((
            self.application.student.profile.user.username,
            self.project.project_name
        ))
    
    def save(self, force_insert=False, force_update=False):
        """
        Makes sure that we don't have project interests created on
        applications for a semester different than that project's
        participating semester.
        """
        if self.application.for_semester != self.project.semester:
            return
        else:
            super(ProjectInterest, self).save(force_insert, force_update)
    
    class Meta:
        unique_together = ('application', 'project')
        
class ReferenceRating(models.Model):
    reference = models.ForeignKey('Reference')
    application = models.ForeignKey('Application')
    department = models.CharField(max_length=40, blank=True)
    q_how_known = models.TextField(
        verbose_name="In what capacity have you known the student?",
        blank=True,
    )
    q_strengths = models.TextField(
        verbose_name=("What strengths of the student would contribute to a "
            "successful project outcome?"),
        blank=True,
    )
    q_strength_example = models.TextField(
        verbose_name=("Please give an example of a situation when the "
            "student has demonstrated one or more of these strengths"),
        blank=True,
    )
    q_weakness = models.TextField(
        verbose_name="What is an area of weakness for the student?",
        blank=True,
    )
    q_weakness_improve = models.TextField(
        verbose_name=("How will being a member of an ELC team help the "
            "student address this weakness?"),
        blank=True,
    )
    ability_rating = models.IntegerField(
        verbose_name=("On a scale from 1-10 (10 being the highest), "
            "please rate the ability of this student to work in a "
            "self-directed, team focused project."),
        null=True, blank=True)
    
    def __unicode__(self):
        return self.application.student.profile.user.username
    
class SponsorContact(models.Model):
    company = models.ForeignKey(Sponsor, related_name='contact_set')
    salutation = models.CharField(max_length=10, blank=True)
    first_name = models.CharField(max_length=40, blank=True)
    last_name = models.CharField(max_length=40, blank=True)
    email = models.EmailField(blank=True)
    title = models.CharField(max_length=40, blank=True)
    address1 = models.CharField(max_length=40, blank=True)
    address2 = models.CharField(max_length=40, blank=True)
    city = models.CharField(max_length=40, blank=True)
    state = USStateField(blank=True)
    zipcode = models.IntegerField(max_length=5, blank=True, null=True)
    phone = PhoneNumberField(blank=True)
    
    def __unicode__(self):
        return ' '.join((self.first_name, self.last_name))
    
class Keycard(models.Model):
    keycard_number = models.IntegerField(unique=True)
    is_active = models.BooleanField()
    
    def __unicode__(self):
        return unicode(self.keycard_number)
    
    class Meta:
        ordering = ['keycard_number']

class Major(models.Model):
    title = models.CharField(max_length=50)
    college = models.ForeignKey('College', related_name='majors')
    
    def __unicode__(self):
        return self.title
        
class College(models.Model):
    name = models.CharField(max_length=40)
    
    def __unicode__(self):
        return self.name
    
class ProjectContact(models.Model):
    project = models.ForeignKey(Project)
    sponsor_contact = models.ForeignKey(SponsorContact)
    
    def __unicode__(self):
        return self.project.project_name
    
class ProjectSponsor(models.Model):
    project = models.ForeignKey(Project)
    sponsor = models.ForeignKey(Sponsor)
    
class AssignedKeycard(models.Model):
    owner = models.ForeignKey(UserProfile)
    keycard = models.ForeignKey(Keycard)
    issue_date = models.DateField(blank=True, null=True)
    return_date = models.DateField(blank=True, null=True)
    
class ProjectCoach(models.Model):
    project = models.ForeignKey(Project)
    coach = models.ForeignKey(Coach)
    
class Reference(models.Model):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=40, blank=True)
    last_name = models.CharField(max_length=40, blank=True)
    phone_number = PhoneNumberField(blank=True)
    verified = models.BooleanField(default=False)
    
    def __unicode__(self):
        return self.email
    