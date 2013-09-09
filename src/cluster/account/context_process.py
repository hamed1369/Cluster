# -*- coding:utf-8 -*-
import datetime
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from cluster.account.forms import SignInForm
from cluster.utils.permissions import PermissionController

__author__ = 'M.Y'


def login_form_check(request):
    if not hasattr(request, 'login_form'):
        path = request.path
        if request.method == 'POST' and request.POST.get('login-submit'):
            login_form = SignInForm(request.POST)
            if login_form.is_valid():
                username = login_form.cleaned_data['username']
                password = login_form.cleaned_data['password']

                user = authenticate(username=username, password=password)
                if user is None or not user.is_active:
                    messages.error(request, u"نام کاربری یا گذرواژه نادرست است.")
                else:
                    login(request, user)
                    return HttpResponseRedirect(path)

        else:
            login_form = SignInForm()

        return {'login_form': login_form}
    return {}


def default_context(request):
    today = datetime.date.today()
    user_menus = PermissionController.get_user_menus(request.user)
    return {'today': today, 'menus': user_menus}
