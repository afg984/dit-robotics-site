from django.dispatch import receiver


def unique_receiver(signal, **kwargs):
    def _receiver(callback):
        kwargs.setdefault(
            'dispatch_uid', 
            '%s.%s' % (callback.__module__, callback.__qualname__)
        )
        return receiver(signal, **kwargs)(callback)
    return _receiver
