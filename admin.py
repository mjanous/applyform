from django.contrib.auth.models import User
from applyform.models import *
from django.contrib import admin

class ApplicationInline(admin.StackedInline):
    model = Application
    extra = 1

class ConsultantInline(admin.StackedInline):
    model = Consultant
    verbose_name_plural = "Consultant Projects"
    extra = 1
    
class AssistantCoachInline(admin.StackedInline):
    model = AssistantCoach
    verbose_name_plural = "Assitant Coach Projects"
    extra = 1
    
class StudentInline(admin.StackedInline):
    model = Student
    verbose_name_plural = "Student Profile"
    extra = 1
    
class ProjectInterestInline(admin.StackedInline):
    model = ProjectInterest
    
class CoachInline(admin.StackedInline):
    model = Coach
    verbose_name_plural = "Coach Projects"
    
class BlankAdmin(admin.ModelAdmin):
    pass

class StudentAdmin(admin.ModelAdmin):
    inlines = [
        ConsultantInline,
        AssistantCoachInline,
        ApplicationInline,
    ]

class UserProfileAdmin(admin.ModelAdmin):
    inlines = [
        StudentInline,
        CoachInline,
    ]
    
class ApplicationAdmin(admin.ModelAdmin):
    inlines = [
        ProjectInterestInline,
    ]
    
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Consultant, BlankAdmin)
admin.site.register(AssistantCoach, BlankAdmin)
admin.site.register(Application, ApplicationAdmin)
admin.site.register(Resume, BlankAdmin)
admin.site.register(Keycard, BlankAdmin)
admin.site.register(Semester, BlankAdmin)
admin.site.register(Project, BlankAdmin)
admin.site.register(Sponsor, BlankAdmin)
admin.site.register(SponsorContact, BlankAdmin)
admin.site.register(ProjectInterest, BlankAdmin)
admin.site.register(Reference, BlankAdmin)
admin.site.register(Coach, BlankAdmin)