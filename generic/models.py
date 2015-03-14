from django.db import models
from django.utils.html import mark_safe
from markdown import markdown

class MarkdownTextField(models.TextField):
    def __init__(self, *args, **kwother):
        kwargs = {
            'help_text': '本欄位使用 <a href="http://markdown.tw/" target="_blank">Markdown</a> 標記。'
        }
        kwargs.update(kwother)
        super().__init__(*args, **kwargs)

    def as_html(self):
        return mark_safe(markdown(self, safe_mode=True))
