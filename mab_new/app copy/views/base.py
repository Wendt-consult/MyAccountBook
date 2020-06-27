from django.views import View
from django.shortcuts import render

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import User


class UnAuthorized(View):

    def get(self, request):
        template_name = 'app/base/error_page.html'
        return render(request, template_name, {})


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        raw_password = request.POST.get('password')
        User.objects.create_user(username=username, password=raw_password)
        return redirect('login')
    else:
        return render(request, 'app/registration/signup.html')