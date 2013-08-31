# -*- coding:utf-8 -*-
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mass_mail
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from cluster.account.account.models import Cluster
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
        return render_to_response('show_message.html', {}, context_instance=RequestContext(request))

    context = register_handler.get_context()
    return render_to_response('registration/register.html',
                              context,
                              context_instance=RequestContext(request))


def register(request):
    return handle_register_view(request)


@login_required()
def register_member(request, cluster_id):
    return handle_register_view(request, cluster_id)


def email_test(request):
    message1 = ('Subject here', 'Here is the message', 'from@example.com', ['hamed.tahmooresi@gmail.com'])
    send_mass_mail((message1,), fail_silently=False)
    return HttpResponse("done!")