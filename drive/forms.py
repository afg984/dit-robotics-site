
from django import forms
from .models import DriveFile

class UploadFileForm(forms.ModelForm):
    class Meta:
        model = DriveFile
        fields = ('file',)
