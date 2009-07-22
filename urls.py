from django.conf.urls.defaults import *
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
    url('^cover_letter/$',
        view='cover_letter',
        name='cover_letter',
    ),
    url('^reference/$',
        view='reference',
        name='reference',
    ),
    url('^coach/$',
        view='coach_list_projects',
        name='coach_list_projects',
    ),
    url('^project/(?P<project_id>\d*)/$',
        view='coach_list_students',
        name='coach_list_students',
    ),
    url('apps/(?P<app_id>\d*)/$',
        view='apps_detail',
        name='apps_detail',
    ),
    url('contact_s/$',
        view='student_contact_report_by_semester',
        name='student_contact_report_by_semester',
    ),
    url('contact_p/$',
        view='student_contact_report_by_project',
        name='student_contact_report_by_project',
    ),
    url('projects/page(?P<page>[0-9]+)/$',
        view='project_list',
        name='project_list',
    ),
    url('projects/(?P<object_id>\d+)/$',
        view='project_detail',
        name='project_detail',
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
    url('^not_accepting/$',
        'direct_to_template',
        {'template': 'applyform/not_accepting.html'},
        name='not_accepting',
    ),
    # TODO: Make this point to a real page for already submitted error.
    url('^already_submitted/$',
        'direct_to_template',
        {'template': 'applyform/not_accepting.html'},
        name='already_submitted',
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
