from applyform.models import *
from django.contrib.auth.models import User
from django.contrib import admin

class AssignedKeycardInline(admin.StackedInline):
    model = AssignedKeycard
    extra = 1

class UserInline(admin.StackedInline):
    model = User
    extra = 0

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

class ProjectCoachInline(admin.TabularInline):
    model = ProjectCoach
    extra = 1
    
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
        AssignedKeycardInline,
    ]
    search_fields = ['user__first_name', 'user__last_name', 'user__username']
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
        ProjectCoachInline,
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
    
class KeycardAdmin(admin.ModelAdmin):
    inlines = [
        AssignedKeycardInline,
    ]
    
class CoachAdmin(admin.ModelAdmin):
    inlines = [
        ProjectCoachInline,
    ]
    
class AssistantCoachAdmin(admin.ModelAdmin):
    filter_vertical = ['projects']
    
class ConsultantAdmin(admin.ModelAdmin):
    filter_vertical = ['projects']
    
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Consultant, ConsultantAdmin)
admin.site.register(AssistantCoach, AssistantCoachAdmin)
admin.site.register(Application, ApplicationAdmin)
admin.site.register(Keycard, KeycardAdmin)
admin.site.register(Semester, BlankAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Sponsor, SponsorAdmin)
admin.site.register(SponsorContact, SponsorContactAdmin)
admin.site.register(ProjectInterest, BlankAdmin)
admin.site.register(Coach, CoachAdmin)
admin.site.register(Major, BlankAdmin)
admin.site.register(College, BlankAdmin)
admin.site.register(ReferenceRating, BlankAdmin)
admin.site.register(ImplementationType, BlankAdmin)
