# -*- coding:utf-8 -*-
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from cluster.account.forms import SignInForm
from cluster.utils.permissions import PermissionController

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
            elif PermissionController.is_member(user) and user.member.is_confirmed is False:
                messages.error(request, u"ثبت نام شما از طرف مدیریت رد شده است و نمی توانید در سامانه وارد شوید.")
            else:
                login(request, user)
                next_page = request.GET.get('next')
                #if PermissionController.is_admin(user):
                #    ProjectMilestone.check_milestones()
                if next_page:
                    return HttpResponseRedirect(next_page)
                else:
                    return HttpResponseRedirect(PermissionController.get_user_redirect_url(user))
    else:
        login_form = SignInForm()

    return render_to_response('accounts/login_page.html', {'login_form': login_form},
                              context_instance=RequestContext(request))
