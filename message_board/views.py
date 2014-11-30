from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from .models import Message
from .forms import AnonymousMessageForm, UserMessageForm

# Create your views here.
def message_board(request):
    context = RequestContext(request)
    if request.user.is_authenticated():
        MessageForm = UserMessageForm
    else:
        MessageForm = AnonymousMessageForm

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('message_board')
        else:
            context['form'] = form
    else:
        context['form'] = MessageForm()
    context['messages'] = Message.objects.order_by('-id')
    return render_to_response('message_board.html', context)
