from django.http import HttpResponse

from drs import settings

class AttachmentResponse(HttpResponse):
    def __init__(self, *args, file, **kwargs):
        super().__init__(*args, **kwargs)
        self['Content-Disposition'] = 'attachment'
        del self['Content-Type']
        if settings.DEBUG:
            self.content = file.file.read()
        else:
            self['X-Accel-Redirect'] = file.url
