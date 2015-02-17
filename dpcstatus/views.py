import json
import traceback
import urllib.request


from django.shortcuts import render

# Create your views here.

URL = 'http://192.168.100.12:5000'

def get_data():
    try:
        return json.loads(urllib.request.urlopen(URL, timeout=3).read().decode())
    except Exception:
        return {'ERROR': traceback.format_exc()}
    

def index(request):
    if not request.user.is_authenticated() or request.user.profile.access_level < 2:
        return render(
            request,
            'dpcstatus/denied.html',
        )
    return render(
        request,
        'dpcstatus/index.html',
        get_data(),
    )
