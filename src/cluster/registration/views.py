# -*- coding:utf-8 -*-
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from cluster.account.account.models import Cluster, Arbiter
from cluster.registration.forms import ArbiterForm
from cluster.registration.handlers import ClusterHandler
from cluster.utils.messages import MessageServices, SMSService


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
        member = register_handler.save_forms()
        subject = u"ثبت نام شما با موفقیت انجام شد."
        message_body = u"توجه داشته باشید که تا زمان تاییدشدن عضویت شما توسط مدیر سامانه ، نمیتوانید طرحی را در سامانه ثبت کنید ."
        message = MessageServices.get_title_body_message(subject, message_body)
        MessageServices.send_message(u"ثبت نام در سامانه موسسه پژوهشی نگاه نو", message, member.user)
        SMSService.send_sms(subject + '\n' + message_body, [member.mobile])

        messages.success(request, u"ثبت نام شما با موفقیت انجام شد.")
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('edit_accounts'))
        return HttpResponseRedirect(reverse('login'))

    context = register_handler.get_context()
    return render_to_response('registration/register.html',
                              context,
                              context_instance=RequestContext(request))


def register(request):
    if not request.user.is_anonymous():
        messages.error(request, u"شما دارای پروفایل هستید.")
        return render_to_response('show_message.html', {}, context_instance=RequestContext(request))
    return handle_register_view(request)


@login_required()
def register_member(request, cluster_id):
    return handle_register_view(request, cluster_id)


def arbiter_register(request):
    invitation_key = request.GET.get('c')
    arbiter = None
    if invitation_key:
        arbiter = get_object_or_404(Arbiter, invitation_key=invitation_key, invited=True)
    if request.POST:
        arbiter_form = ArbiterForm(request.POST, prefix='register', instance=arbiter)
        if arbiter_form.is_valid():
            arbiter_form.save()
            messages.success(request, u"ثبت نام شما با موفقیت انجام شد.")
            return HttpResponseRedirect(reverse('login'))
    else:
        arbiter_form = ArbiterForm(prefix='register', instance=None)
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
