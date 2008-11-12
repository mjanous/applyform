#Create your views here.

from django.shortcuts import render_to_response
from applyform.models import *
from django.conf import settings

def index(request):
    return render_to_response(
        'applyform/index.html',
        {
            'request': request,
            'MEDIA_URL': settings.MEDIA_URL,
        }
    )
