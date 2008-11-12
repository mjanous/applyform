from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True, related_name='profile')
    dob = models.DateField(blank=True, null=True)
    address = models.CharField(max_length=80, blank=True)
    city = models.CharField(max_length=40, blank=True)
    state = models.CharField(max_length=2, blank=True)
    zipcode = models.IntegerField(max_length=5, blank=True, null=True)
    home_phone = models.CharField(max_length=14, blank=True)
    mobile_phone = models.CharField(max_length=14, blank=True)
    
    def __unicode__(self):
        return self.user.username
    
class StudentProfile(models.Model):
    profile = models.OneToOneField(
        UserProfile, unique=True, related_name='student_profile')
    major = models.CharField(max_length=40, blank=True)
    grad_date = models.ForeignKey('Semester', blank=True, null=True)
    grad_status = models.BooleanField(
        verbose_name='Graduate Student?',
        help_text='Check this box if you are a graduate student',
        blank=True
    )
    enrollment_status = models.BooleanField(
        verbose_name='Enrolled in or have completed UBUS 311',
        blank=True
    )
    honors_status = models.BooleanField(
        verbose_name='Honors Student?',
        help_text='Check this box if you are an honors student',
        blank=True
    )
    hear_about_us = models.CharField(max_length=60, blank=True)
    project = models.ManyToManyField(
        'Project', related_name='students', blank=True)
    
    def __unicode__(self):
        return self.profile.user.username
    
class CoachProfile(models.Model):
    profile = models.OneToOneField(
        UserProfile, unique=True, related_name='coach_profile')
    project = models.ManyToManyField('Project', related_name='coaches')    

    def __unicode__(self):
        return self.profile.user.username

class AssistantCoachProfile(models.Model):
    profile = models.OneToOneField(
        UserProfile, unique=True, related_name='assistant_coach_profile')
    project = models.ManyToManyField(
        'Project', related_name='assistant_coaches')
        
    def __unicode__(self):
        return self.profile.user.username

class ReferenceProfile(models.Model):
    profile = models.OneToOneField(
        UserProfile, unique=True, related_name='reference_profile')
    students = models.ManyToManyField(
        StudentProfile, through='ReferenceRating')

class Application(models.Model):
    student = models.ForeignKey(StudentProfile, related_name='applications')
    project_interests = models.ManyToManyField(
        'Project', through='ProjectInterest', related_name='applications')
    submitted = models.BooleanField('Application submitted?')
    
    def __unicode__(self):
        return self.student.profile.user.username

class Semester(models.Model):
    year = models.IntegerField()
    season = models.CharField(max_length=6)
    start_date = models.DateField()
    end_date = models.DateField()

    def __unicode__(self):
        return ' '.join((self.season, str(self.year)))
    
class Project(models.Model):
    project_name = models.CharField(max_length=60)
    semester = models.ForeignKey(Semester)
    sponsor = models.ForeignKey('Sponsor')
    
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
    
class ReferenceRating(models.Model):
    reference = models.ForeignKey(ReferenceProfile)
    student = models.ForeignKey(StudentProfile)
    rating = models.IntegerField(max_length=2)
    