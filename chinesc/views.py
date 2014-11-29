from django.shortcuts import render_to_response
from django.template import RequestContext

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
        context = RequestContext(
            request,
            dict(code=code,
                 style=formatter.get_style_defs('.highlight'),
                 form=form,)
        )
        return render_to_response('chinesc_submitted.html', context)
    else:
        return render_to_response('chinesc.html',
                RequestContext(request, {'form': CodeForm()}))
