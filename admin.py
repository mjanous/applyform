from applyform.models import *
from django.contrib.auth.models import User
from django.contrib import admin

class SponsorLogoInline(admin.StackedInline):
    model = SponsorLogo
    extra = 1

class ReferenceRatingInline(admin.StackedInline):
    model = ReferenceRating
    extra = 1
    
class ReferenceInline(admin.StackedInline):
    model = Reference
    extra = 1
    
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
    
class ProjectConsultantInline(admin.TabularInline):
    model = ProjectConsultant
    extra = 6
    
class JobPlacementInline(admin.StackedInline):
    model = JobPlacement
    extra = 1
    
class BlankAdmin(admin.ModelAdmin):
    pass

class StudentAdmin(admin.ModelAdmin):
    inlines = [
        AssistantCoachInline,
        ApplicationInline,
    ]
    search_fields = [
        'profile__user__first_name',
        'profile__user__last_name',
        'profile__user__username'
    ]
    list_display = ('profile', 'first_name', 'last_name')

class UserProfileAdmin(admin.ModelAdmin):
    
    inlines = [
        StudentInline,
        CoachInline,
        AssignedKeycardInline,
        JobPlacementInline,
    ]
    search_fields = ['user__first_name', 'user__last_name', 'user__username']
    list_display = ('user', 'first_name', 'last_name')
    
class ApplicationAdmin(admin.ModelAdmin):
    inlines = [
        ProjectInterestInline,
        ReferenceRatingInline,
    ]
    search_fields = [
        'student__profile__user__first_name',
        'student__profile__user__last_name',
        'student__profile__user__username',
        'for_semester__season',
        'for_semester__year',
        'date_submitted',
    ]
    
    list_filter = ('for_semester', 'is_submitted',)
    list_display = (
        '__unicode__',
        'first_name',
        'last_name',
        'for_semester',
        'date_submitted',
        'is_submitted',
        'get_reference',
        'reference_name',
    )

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'semester', 'implemented_as')
    list_filter = ('semester', 'sponsors')
    inlines = [
        ProjectContactInline,
        ProjectSponsorInline,
        ProjectCoachInline,
        ProjectConsultantInline,
    ]
    search_fields = [
        'project_name',
        'semester__year',
        'semester__season',
        'sponsors__sponsor_name',
    ]
    
class SponsorContactAdmin(admin.ModelAdmin):
    inlines = [
        ProjectContactInline,
    ]

class SponsorAdmin(admin.ModelAdmin):
    inlines = [
        ProjectSponsorInline,
        SponsorContactInline,
        SponsorLogoInline,
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
    inlines = [
        ProjectConsultantInline,
    ]
    filter_vertical = ['projects']
    search_fields = [
        'student__profile__user__first_name',
        'student__profile__user__last_name',
        'projects__project_name',
        'projects__sponsors__sponsor_name',
        'projects__semester__season',
        'projects__semester__year',
    ]
    
class SponsorLogoAdmin(admin.ModelAdmin):
    list_display = ['sponsor', 'admin_thumbnail']
    
class JobPlacementAdmin(admin.ModelAdmin):
    list_display = [
        'first_name',
        'last_name',
        'company',
    ]
        

admin.site.register(SponsorLogo, SponsorLogoAdmin)
admin.site.register(Config, BlankAdmin)
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
admin.site.register(Reference, BlankAdmin)
admin.site.register(JobPlacement, JobPlacementAdmin)