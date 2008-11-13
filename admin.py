from django.contrib.auth.models import User
from applyform.models import *
from django.contrib import admin

class BlankAdmin(admin.ModelAdmin):
    pass

admin.site.register(UserProfile, BlankAdmin)
admin.site.register(Student, BlankAdmin)
admin.site.register(Consultant, BlankAdmin)
admin.site.register(AssistantCoach, BlankAdmin)
admin.site.register(Application, BlankAdmin)
admin.site.register(Resume, BlankAdmin)
admin.site.register(Keycard, BlankAdmin)
admin.site.register(Semester, BlankAdmin)
admin.site.register(Project, BlankAdmin)
admin.site.register(Sponsor, BlankAdmin)
admin.site.register(ProjectInterest, BlankAdmin)
admin.site.register(Reference, BlankAdmin)