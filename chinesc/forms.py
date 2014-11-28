from django import forms
from bootstrap_plugin.forms import simpleFactory

class CodeForm(simpleFactory(forms.Form)):
    user_code = forms.CharField(
        label='Your Code',
        widget=forms.Textarea()
    )
