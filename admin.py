from applyform.models import *
from django.contrib import admin

class SponsorContactInline(admin.StackedInline):
    model = SponsorContact
    extra = 1
    
class ProjectSponsorInline(admin.TabularInline):
    model = ProjectSponsor
    extra = 1
    
class ProjectContactInline(admin.TabularInline):
    model = ProjectContact
    extra = 1

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
    
    list_display = ('user', 'first_name', 'last_name')
    
class ApplicationAdmin(admin.ModelAdmin):
    inlines = [
        ProjectInterestInline,
    ]

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('project_name', 'semester', 'implemented_as')
    inlines = [
        ProjectContactInline,
        ProjectSponsorInline,
    ]
    
class SponsorContactAdmin(admin.ModelAdmin):
    inlines = [
        ProjectContactInline,
    ]

class SponsorAdmin(admin.ModelAdmin):
    inlines = [
        ProjectSponsorInline,
        SponsorContactInline,
    ]
    
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Consultant, BlankAdmin)
admin.site.register(AssistantCoach, BlankAdmin)
admin.site.register(Application, ApplicationAdmin)
admin.site.register(Keycard, BlankAdmin)
admin.site.register(Semester, BlankAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Sponsor, SponsorAdmin)
admin.site.register(SponsorContact, SponsorContactAdmin)
admin.site.register(ProjectInterest, BlankAdmin)
admin.site.register(Coach, BlankAdmin)
admin.site.register(Major, BlankAdmin)
admin.site.register(College, BlankAdmin)
admin.site.register(ReferenceRating, BlankAdmin)
admin.site.register(ImplementationType, BlankAdmin)
