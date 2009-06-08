from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

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
            