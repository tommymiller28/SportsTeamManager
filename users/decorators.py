from django.http import HttpResponseForbidden

def coach_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == "coach":
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("You are not authorized to view this page.")
    return _wrapped_view
