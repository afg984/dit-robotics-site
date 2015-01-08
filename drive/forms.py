
from django import forms
from .models import DriveFile, DriveDirectory

class UploadFileForm(forms.ModelForm):
    class Meta:
        model = DriveFile
        fields = ('file',)

class MkdirForm(forms.ModelForm):
    class Meta:
        model = DriveDirectory
        fields = ('name', )
