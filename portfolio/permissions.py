from django.shortcuts import render
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.urls import reverse

def paid_user_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            next_url = request.get_full_path()
            return redirect(f'{reverse("signin")}?next={next_url}')

        if not request.user.is_paid:
            return render(request, '403_forbidden.html', status=403)

        return view_func(request, *args, **kwargs)
    
    return _wrapped_view