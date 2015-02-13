import json
import traceback
import urllib.request


from django.shortcuts import render_to_response
from django.template import RequestContext

# Create your views here.

URL = 'http://192.168.100.12:5000'

def get_data():
    try:
        return json.loads(urllib.request.urlopen(URL, timeout=3).read().decode())
    except Exception:
        return {'ERROR': traceback.format_exc()}
    

def index(request):
    if not request.user.is_authenticated() or request.user.profile.access_level < 2:
        return render_to_response(
            'dpcstatus/denied.html',
            context_instance=RequestContext(request)
        )
    return render_to_response(
        'dpcstatus/index.html',
        get_data(),
        context_instance=RequestContext(request)
    )
