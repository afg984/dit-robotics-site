from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

class LoginRequiredMixin:
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)


class SuperuserRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super(SuperuserRequiredMixin, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

class PermissionRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        perms = self.permission_required
        if not isinstance(perms, (list, tuple)):
            perms = (perms,)
        if request.user.has_perms(perms):
            return super(PermissionRequiredMixin, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied
