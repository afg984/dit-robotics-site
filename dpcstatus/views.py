import json
import datetime
import traceback
import urllib.request
import urllib.error

from django.utils.dateparse import parse_datetime
from django.shortcuts import render

# Create your views here.

URL = 'http://192.168.100.12'
SUMMARY_URL = URL + '/summary/'

def add_context(data):
    printer = data['printer']
    printer['timestamp'] = parse_datetime(printer['timestamp'])
    printer['age'] = datetime.datetime.now() - printer['timestamp']
    if 'starttime' in printer:
        printer['starttime'] = datetime.datetime.fromtimestamp(printer['starttime'])
    if 'secondsremain' in printer:
        printer['remaining'] = datetime.timedelta(seconds=printer['remaining'])
        printer['done'] = printer['timestamp'] + printer['remaining']
    if 'status' in printer:
        printer['statusstyle'] = {
            'Printing': 'primary',
            'SD Printing': 'primary',
            'Disconnected': 'warning',
            'Idle': 'success',
        }.get(printer['status'], 'danger')


def get_data(url=URL):
    try:
        data = json.loads(urllib.request.urlopen(url, timeout=1).read().decode())
        add_context(data)
        return data
    except urllib.error.URLError:
        return {
            'ERROR': traceback.format_exc(),
            'printer': {
                'status': 'Computer Offline',
                'statusstyle': 'danger',
            }
        }
    except Exception:
        return {
            'ERROR': traceback.format_exc(),
            'printer': {
                'status': 'ERROR',
                'statusstyle': 'danger',
            }
        }
    

def index(request, template_name, summary=False):
    if not request.user.is_authenticated() or request.user.profile.access_level < 2:
        return render(
            request,
            'dpcstatus/denied.html',
        )
    return render(
        request,
        template_name,
        get_data(SUMMARY_URL if summary else URL),
    )
