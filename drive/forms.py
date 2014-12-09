
from django import forms

class UploadFileForm(forms.ModelForm):
    class Meta:
        fields = ('file',)
