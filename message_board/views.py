from django.shortcuts import render, redirect

from .models import Message
from .forms import MessageForm

# Create your views here.
def message_board(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('message_board')
        else:
            context = dict()
            context['form'] = form
    else:
        context = dict()
        context['form'] = MessageForm()
        context['messages'] = Message.objects.order_by('-id')
    return render(request, 'message_board.html', context)
