from django.forms import ModelForm
from bootstrap_plugin.forms import simpleFactory

from .models import Message

class MessageForm(simpleFactory(ModelForm)):
    class Meta:
        model = Message
        fields = ['nickname', 'message']
