from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect

class LoginRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return super().dispatch(request, *args, **kwargs)
        return redirect('social:begin', backend='facebook')


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
