from django.shortcuts import render, redirect

from .models import Message
from .forms import AnonymousMessageForm, UserMessageForm

# Create your views here.
def message_board(request):
    context = {}
    if request.user.is_authenticated():
        MessageForm = UserMessageForm
    else:
        MessageForm = AnonymousMessageForm

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            if request.user.is_authenticated():
                message.user = request.user
            message.save()
            return redirect('message_board')
        else:
            context['form'] = form
    else:
        context['form'] = MessageForm()
    context['messages'] = Message.objects.order_by('-id')
    return render(request, 'message_board.html', context)
