from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponseForbidden


def role_required(*allowed_roles):
    """Decorator: @role_required('admin', 'teacher')"""

    def decorator(view_func):

        @wraps(view_func)
        def wrapper(request, *args, **kwargs):

            if not request.user.is_authenticated:
                messages.warning(request, "Please log in to access the page.")
                return redirect('login')

            user_role = request.user.profile.role

            if user_role not in allowed_roles:
                messages.error(
                    request,
                    "You do not have permission to access this page."
                )
                return HttpResponseForbidden("Access denied.")

            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator