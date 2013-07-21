# -*- coding:utf-8 -*-
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render_to_response


def login(request):
    if request.method != 'POST':
        login_form = AuthenticationForm()
        return render_to_response('accounts/login.html',{'login_form':login_form})


def logout(request):
    pass