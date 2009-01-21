from django.conf.urls.defaults import *
from django.conf import settings
from applyform.models import *

urlpatterns = patterns('applyform.views',
    url('^menu/$',
        view='apply_menu',
        name='apply_menu',
    ),
    url('^basic_info/$',
        view='basic_info',
        name='basic_info',
    ),
    url('^project_select/$',
        view='project_select',
        name='project_select',
    ),
    url('^resume/$',
        view='resume',
        name='resume',
    ),
    url('reference/$',
        view='reference',
        name='reference',
    ),
)

urlpatterns += patterns('django.views.generic.simple',
    url('^$',
        'direct_to_template',
        {'template': 'applyform/index.html'},
        name='index',
    ),
    url('^thanks/$',
        'direct_to_template',
        {'template': 'applyform/thanks.html'},
        name='thanks',
    ),
    url('^sorry/$',
        'direct_to_template',
        {'template': 'applyform/not_accepting.html'},
        name='not_accepting',
    ),
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
