from django.shortcuts import render

from pygments import highlight
from pygments.lexers import CppLexer
from pygments.formatters import HtmlFormatter

from .defs import htmlConvert
from .forms import CodeForm

# Create your views here.

def chinesc(request):
    form = CodeForm(request.GET)
    if form.is_valid():
        formatter = HtmlFormatter(style='xcode')
        code = highlight(form.cleaned_data['user_code'], CppLexer(), formatter)
        code = htmlConvert(code)
        context = dict(
            code=code,
            style=formatter.get_style_defs('.highlight'),
            form=form,
            title='ChinesC'
        )
        return render(request, 'chinesc_submitted.html', context)
    else:
        return render(request, 'chinesc.html', {'form': CodeForm(), 'title': 'ChinesC'})
