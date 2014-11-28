from django.shortcuts import render

# Create your views here.

def drive(request):
    return render(request, 'drive.html')
