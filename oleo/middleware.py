from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect
from django.urls import resolve
import re


class LoginRequiredMiddleware(MiddlewareMixin):
    def process_request(self, request):
        app_name = resolve(request.path).app_name
        
        if 'admins' == app_name and request.path != '/admin/login':
            if not request.user.is_superuser:
                return redirect('/admin/login')
