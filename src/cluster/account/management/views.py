# -*- coding:utf-8 -*-
'''
Created on 19/11/13

@author: hamed
'''
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from cluster.account.management.forms import IntroPageForm
from cluster.account.management.models import IntroPageContent
from cluster.utils.permissions import PermissionController


@login_required
def edit_intro_page(request):
    if not PermissionController.is_admin(request.user):
        return HttpResponseRedirect('/login/')
    instance = IntroPageContent.get_instance()
    if request.method == 'POST':
        form = IntroPageForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, u"ویرایش اطلاعات با موفقیت انجام شد.")
        else:
            messages.error(request,u"فرم نا معتبر است.")
    else:
        form = IntroPageForm(instance=instance)

    return render_to_response('accounts/edit_intro_page.html',{"form":form},context_instance=RequestContext(request))
