from django.contrib import messages
from django.shortcuts import redirect


def anonymous_required(view_func=None, /, *, redirect_url="pages:index"):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if request.user.is_authenticated:
                messages.warning(request, "您已登入，無法存取此頁面")
                return redirect(redirect_url)
            return view_func(request, *args, **kwargs)

        return wrapper

    if view_func is None:
        return decorator
    return decorator(view_func)
