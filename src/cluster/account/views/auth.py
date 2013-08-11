# -*- coding:utf-8 -*-
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from cluster.account.forms import SignInForm

__author__ = 'M.Y'


def login_view(request):

    if request.method == 'POST':
        login_form = SignInForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']

            user = authenticate(username=username, password=password)
            if user is None or not user.is_active:
                messages.error(request, u"نام کاربری یا گذرواژه نادرست است.")
            else:
                login(request, user)
                next_page = request.GET.get('next')
                if next_page:
                    return HttpResponseRedirect(reverse(next_page))
                else:
                    return HttpResponseRedirect(reverse('register'))
    else:
        login_form = SignInForm()

    return render_to_response('accounts/login_page.html', {'login_form': login_form},
                              context_instance=RequestContext(request))