import re
import json
import datetime
import traceback
import urllib.request
import urllib.error

from django.utils.dateparse import parse_datetime
from django.shortcuts import render

# Create your views here.

URL = 'http://192.168.100.12'


pattern = re.compile(
    r'Hotend:(?P<temp>[\d\.]+) E:\d+ W:\d+  Printing:(?P<perc>[\d\.]+) % \| Line# \d+of \d+ lines \| Est: (?P<est>\d\d\:\d\d\:\d\d) of: \d\d\:\d\d\:\d\d Remaining \|  Z: [\d\.]+ mm'
)
ptimepattern = re.compile(
    r'(?P<hours>\d+)\:(?P<minutes>\d+)\:(?P<seconds>\d+)'
)


def add_pretty(datadict):
    targetmsg = datadict['STATUS'][-1]
    stuff = pattern.match(targetmsg['message'])
    if stuff is None:
        stuff = dict()
        msg = targetmsg['message']
        if '無法連接設備' in msg or 'is offline' in msg:
            stuff['status'] = 'Disconnected'
            stuff['statusstyle'] = 'warning'
        elif msg.startswith('Loaded'):
            stuff['status'] = 'Idle'
            stuff['statusstyle'] = 'success'
    else:
        stuff = stuff.groupdict()
        stuff['status'] = 'Printing'
        stuff['statusstyle'] = 'primary'
        if stuff['est'] is not None:
            deltakw = ptimepattern.match(stuff['est']).groupdict()
            for k in deltakw:
                deltakw[k] = int(deltakw[k])
            stuff['done'] = (parse_datetime(targetmsg['time']) + datetime.timedelta(**deltakw)).strftime('%m/%d %H:%M:%S')
    datadict.update(stuff)


def get_data():
    try:
        data = json.loads(urllib.request.urlopen(URL, timeout=3).read().decode())
        add_pretty(data)
        return data
    except urllib.error.URLError:
        return {
            'ERROR': traceback.format_exc(),
            'status': 'Computer Offline',
            'statusstyle': 'danger',
        }
    except Exception:
        return {
            'ERROR': traceback.format_exc(),
            'status': 'ERROR',
            'statusstyle': 'danger',
        }
    

def index(request, template_name):
    if not request.user.is_authenticated() or request.user.profile.access_level < 2:
        return render(
            request,
            'dpcstatus/denied.html',
        )
    return render(
        request,
        template_name,
        get_data(),
    )
