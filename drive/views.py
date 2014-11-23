from django.shortcuts import render

# Create your views here.

def drive(request):
    data = {title: 'Drive'}
    return render(request, 'drive.html', data)
