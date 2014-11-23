from django import forms

class CodeForm(forms.Form):
    user_code = forms.CharField(widget=forms.Textarea)
