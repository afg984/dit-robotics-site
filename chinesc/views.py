from django.shortcuts import render

from pygments import highlight
from pygments.lexers import CppLexer
from pygments.formatters import HtmlFormatter

from .forms import CodeForm

# Create your views here.

def chinesc(request):
    form = CodeForm(request.GET)
    if form.is_valid():
        formatter = HtmlFormatter(style='default')
        context = dict(
            code=highlight(form.cleaned_data.['user_code'], CppLexer(), formatter),
            style=formatter.get_style_defs('.highlight'),
            form=form
        )
        return render(request, 'chinesc.html', context)
    else:
        return render(request, 'chinesc.html', {'form': form})
