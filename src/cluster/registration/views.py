# -*- coding:utf-8 -*-
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from cluster.account.account.models import Cluster, Arbiter
from cluster.registration.forms import ArbiterForm
from cluster.registration.handlers import ClusterHandler


def handle_register_view(request, cluster_id=None):
    try:
        register_handler = ClusterHandler(request, cluster_id)
    except Cluster.DoesNotExist:
        raise Http404
    message = register_handler.has_permission()
    if message:
        messages.error(request, message)
        return render_to_response('show_message.html', {}, context_instance=RequestContext(request))

    register_handler.initial_forms()
    if register_handler.is_valid_forms():
        register_handler.save_forms()
        messages.success(request, u"ثبت نام شما با موفقیت انجام شد.")
        return HttpResponseRedirect('login')

    context = register_handler.get_context()
    return render_to_response('registration/register.html',
                              context,
                              context_instance=RequestContext(request))


def register(request):
    return handle_register_view(request)


@login_required()
def register_member(request, cluster_id):
    return handle_register_view(request, cluster_id)


def arbiter_register(request):
    if request.POST:
        arbiter_form = ArbiterForm(request.POST, prefix='register')
        if arbiter_form.is_valid():
            arbiter_form.save()
            messages.success(request, u"ثبت نام شما با موفقیت انجام شد.")
            return HttpResponseRedirect('login')
    else:
        arbiter_form = ArbiterForm(prefix='register')
    context = {
        'arbiter_form': arbiter_form,
    }
    return render_to_response('registration/arbiter_register.html', context, context_instance=RequestContext(request))


@login_required
def arbiter_edit(request):
    try:
        arbiter = request.user.arbiter
    except Arbiter.DoesNotExist:
        raise Http404
    if request.POST:
        arbiter_form = ArbiterForm(request.POST, instance=arbiter, prefix='edit')
        if arbiter_form.is_valid():
            arbiter_form.save()
            messages.success(request, u"ویرایش اطلاعات با موفقیت انجام شد.")
            arbiter_form = ArbiterForm(instance=arbiter, prefix='edit')
    else:
        arbiter_form = ArbiterForm(instance=arbiter, prefix='edit')
    context = {
        'arbiter_form': arbiter_form,
    }
    return render_to_response('registration/arbiter_edit.html', context, context_instance=RequestContext(request))
