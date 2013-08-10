# -*- coding:utf-8 -*-
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from cluster.registration.handlers import RegisterHandler


def register(request, cluster_id=None):
    register_handler = RegisterHandler(request, cluster_id)
    register_handler.initial_forms()
    if register_handler.is_valid_forms():
        register_handler.save_forms()
        messages.success(request, u"ثبت نام شما با موفقیت انجام شد.")
        return HttpResponseRedirect(reverse('login'))

    context = register_handler.get_context()
    return render_to_response('registration/register.html',
                              context,
                              context_instance=RequestContext(request))