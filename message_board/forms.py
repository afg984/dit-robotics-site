from django.forms import ModelForm
from bootstrap_plugin.forms import simpleFactory

from .models import Message

class AnonymousMessageForm(simpleFactory(ModelForm)):
    class Meta:
        model = Message
        fields = ['nickname', 'message']

class UserMessageForm(simpleFactory(ModelForm)):
    class Meta:
        model = Message
        fields = ['message']
