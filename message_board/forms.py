from django.forms import ModelForm, Textarea

from .models import Message

class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['nickname', 'message']
        widgets = {
            'message': Textarea(attrs={'rows': 4})
        }
