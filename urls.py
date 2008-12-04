from django.conf.urls.defaults import *
from django.conf import settings
from applyform.models import *

urlpatterns = patterns('applyform.views',
    url('^$',
        view='index',
        name='index',
    ),
    url('^menu/$',
        view='apply_menu',
        name='apply_menu',
    ),
    url('^basic_info/$',
        view='basic_info',
        name='basic_info',
    ),
    url('^thanks/$',
        view='thanks',
        name='thanks',
    ),
    url('^project_select/$',
        view='project_select',
        name='project_select',
    ),
    url('^sorry/$',
        view='not_accepting',
        name='not_accepting',
    )
)

urlpatterns += patterns('',
    url(
        r'^login/$',
        view='django.contrib.auth.views.login',
        kwargs={'template_name': 'applyform/login.html'},
        name='login',
    ),
    url(
        r'^logout/$',
        view='django.contrib.auth.views.logout',
        kwargs={'template_name': 'applyform/logged_out.html'},
        name='logout',
    ),
)
