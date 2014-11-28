from django.forms import Textarea
from bootstrap_plugin.forms import BSModelForm

from .models import Message

class MessageForm(BSModelForm):
    class Meta:
        model = Message
        fields = ['nickname', 'message']
        widgets = {
            'message': Textarea(attrs={'rows': 4})
        }
