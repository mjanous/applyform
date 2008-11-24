#Create your views here.

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from applyform.models import *
from applyform.forms import *
from django.conf import settings
from django.contrib.auth.decorators import login_required

def index(request):
    return render_to_response(
        'applyform/index.html',
        {
            'user': request.user,
            'request': request,
            'MEDIA_URL': settings.MEDIA_URL,
        }
    )

@login_required
def apply_page1(request):
    user = request.user
    try:
        userprofile = user.get_profile()

    except: # TODO: What kind of exception!?
        userprofile = user.userprofile_set.create()
        
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.save()
            
            userprofile.address1 = form.cleaned_data['address1']
            userprofile.address2 = form.cleaned_data['address2']
            userprofile.dob = form.cleaned_data['dob']
            userprofile.city = form.cleaned_data['city']
            userprofile.state = form.cleaned_data['state']
            userprofile.save()
            return HttpResponseRedirect('/thanks/')
        
    else:
        form = ApplicationForm(
            initial={
                'first_name': user.first_name,
                'last_name': user.last_name,
                'address1': userprofile.address1,
                'address2': userprofile.address2,
                'dob': userprofile.dob,
                'city': userprofile.city,
                'state': userprofile.state or 'IL',
                'email': user.email,
            }
        )
        
    return render_to_response(
        'applyform/apply_page1.html',
        {
            'user': request.user,
            'form': form,
            'MEDIA_URL': settings.MEDIA_URL,
        }
    )

def thanks(request):
    return render_to_response(
        'applyform/thanks.html',
        {
            'user': request.user,
            'request': request,
            'MEDIA_URL': settings.MEDIA_URL,
        }
    )
