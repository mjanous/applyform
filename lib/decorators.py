from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

try:
    from functools import wraps
except ImportError:
    from django.utils.functional import wraps  # Python 2.3, 2.4 fallback.
    
def require_student_profile(func):
    """
    Decorator to make a view create a student profile for the user if one
    isn't already started. Usage::
    
        @require_app_started
        def my_view(request):
            # I can assume now that we have a student profile.
    """
    
    def inner(request, *args, **kwargs):
        from applyform.models import Semester
        semester_accepting = Semester.accepting_semesters.get()
        userprofile, created = request.user.userprofile_set.get_or_create()
        student_profile, created = userprofile.student_profile.get_or_create()
        return func(request, *args, **kwargs)
    return wraps(func)(inner)
    
def require_app_started(func):
    """
    Decorator to make a view allow access only if user has started the
    ELC application process. If not started, will bring them to a view asking
    if they would like to begin.
    Usage::
    
        @require_app_started
        def my_view(request):
            # I can assume now that we have started the app process.
    """
    
    def inner(request, *args, **kwargs):
        from applyform.models import Semester
        semester_accepting = Semester.accepting_semesters.get()
        
        try:
            userprofile = request.user.userprofile_set.get()
            student_profile = userprofile.student_profile.get()
            application = student_profile.applications.get(
                for_semester=semester_accepting)
        except (UserProfile.DoesNotExist, Student.DoesNotExist, Application.DoesNotExist):
            return HttpResponseRedirect('begin_app')
        return func(request, *args, **kwargs)
    return wraps(func)(inner)

def require_accepting(func):
    """
    Decorator to make a view allow access only if we're currently
    accepting apps.
    Usage::

        @require_accepting
        def my_view(request):
            # I can assume now that we have a current semester
            # assigned to semester_accepting
            # ...
    """

    def inner(request, *args, **kwargs):
        from applyform.models import Semester
        try:
            semester_accepting = Semester.accepting_semesters.get()
        except (Semester.DoesNotExist, Semester.MultipleObjectsReturned):
            return HttpResponseRedirect(reverse('not_accepting'))
        return func(request, *args, **kwargs)
    return wraps(func)(inner)


def user_has_submitted_application(test_func):
    """
    """
    def _dec(view_func):
        def _checksubmitstatus(request, *args, **kwargs):
            if test_func(request.user):
                return view_func(request, *args, **kwargs)
            return HttpResponseRedirect(reverse('already_submitted'))
        return _checksubmitstatus
    return _dec

submit_restriction = user_has_submitted_application(
    lambda u: not u.get_profile().current_app_is_complete()
)