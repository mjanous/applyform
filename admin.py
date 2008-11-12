from django.contrib.auth.models import User
from applyform.models import *
from django.contrib import admin

class BlankAdmin(admin.ModelAdmin):
    pass

admin.site.register(UserProfile, BlankAdmin)
admin.site.register(StudentProfile, BlankAdmin)
admin.site.register(AssistantCoachProfile, BlankAdmin)
admin.site.register(Application, BlankAdmin)
admin.site.register(Semester, BlankAdmin)
admin.site.register(Project, BlankAdmin)
admin.site.register(Sponsor, BlankAdmin)
admin.site.register(ProjectInterest, BlankAdmin)
admin.site.register(ReferenceProfile, BlankAdmin)