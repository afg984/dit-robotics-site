class TemplateDebugContext:

    def __init__(self, category, request):
        self.category = category
        self.request = request

    def __getattr__(self, name):
        return '%s_%s' % (self.category, name)


def template_debug_context(request):
    return {'DEFECT': TemplateDebugContext('DEFECT', request)}
