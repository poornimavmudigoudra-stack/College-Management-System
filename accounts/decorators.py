from functools import wraps

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from .models import User


def role_required(*roles):
    """Allow the view only for logged-in users whose role is in `roles` (superusers always pass)."""

    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def wrapper(request, *args, **kwargs):
            user = request.user
            if user.is_superuser or user.role in roles:
                return view_func(request, *args, **kwargs)
            messages.error(request, "You do not have permission to access that page.")
            return redirect("accounts:dashboard")

        return wrapper

    return decorator


admin_required = role_required(User.Role.ADMIN)
staff_required = role_required(User.Role.ADMIN, User.Role.FACULTY)
student_required = role_required(User.Role.STUDENT)
