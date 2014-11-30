from django import forms
from django.contrib.auth.models import User

from bootstrap_plugin.forms import simpleFactory

class EmailForm(simpleFactory(forms.Form)):
    email = forms.EmailField()
