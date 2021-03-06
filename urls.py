from django.conf.urls.defaults import *
from django.conf import settings
from applyform.models import *

urlpatterns = patterns('applyform.views',
    url('^$',
        view='index',
        name='index',
    ),
    url('^basic_info/$',
        view='basic_info',
        name='basic_info',
    ),
    url('^thanks/$',
        view='thanks',
        name='thanks',
    ),
)

urlpatterns += patterns('',
    (
        r'^login/$',
        'django.contrib.auth.views.login',
        {'template_name': 'applyform/login.html'}
    ),
    (
        r'^logout/$',
        'django.contrib.auth.views.logout',
        {'template_name': 'applyform/logged_out.html'}
    ),
)
