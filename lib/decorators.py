from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

try:
    from functools import wraps
except ImportError:
    from django.utils.functional import wraps  # Python 2.3, 2.4 fallback.

def require_accepting(func):
    """
    Decorator to make a view allow access only if we're currently
    accepting apps. Also adds a semester_accepting variable to the view.
    Usage::

        @require_accepting
        def my_view(request, semester_accepting):
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
        return func(request, semester_accepting, *args, **kwargs)
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