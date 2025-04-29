from django.shortcuts import redirect

class TokenAuthMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            if not hasattr(request.user, 'token') or not request.user.token:
                from django.contrib.auth import logout
                logout(request)
                return redirect('login')
        response = self.get_response(request)
        return response
