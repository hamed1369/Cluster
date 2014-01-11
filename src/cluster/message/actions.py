# -*- coding: utf-8 -*-
from django.http import Http404
from cluster.message.forms import MessageShowForm, ArbiterMessageForm, MemberMessageForm, AdminMessageForm, EmailSendForm
from cluster.message.models import Message
from cluster.utils.messages import MessageServices
from cluster.utils.permissions import PermissionController

__author__ = 'M.Y'


# -*- coding: utf-8 -*-
from django.contrib import messages
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from cluster.utils.manager.action import ManagerAction


class SendMessage(ManagerAction):
    action_name = 'send_message'
    action_verbose_name = u"ارسال پیام جدید"
    is_view = True
    height = '550'

    def action_view(self, http_request, selected_instances):
        if PermissionController.is_admin(http_request.user):
            model_form = AdminMessageForm
        elif PermissionController.is_arbiter(http_request.user):
            model_form = ArbiterMessageForm
        else:
            model_form = MemberMessageForm

        if http_request.method == 'POST':
            form = model_form(http_request.POST, http_request.FILES, user=http_request.user)
            if form.is_valid():
                form.save()
                form = None
                messages.success(http_request, u"پیام ارسال شد.")
        else:
            form = model_form(user=http_request.user)

        return render_to_response('manager/actions/add_edit.html', {'form': form, 'title': u"ارسال پیام"},
                                  context_instance=RequestContext(http_request))


class ShowMessage(ManagerAction):
    action_name = 'show_message'
    action_verbose_name = u"مشاهده پیام"
    is_view = True
    min_count = 1
    height = '310'

    def action_view(self, http_request, selected_instances):
        form = MessageShowForm(instance=selected_instances[0])
        for field in form.fields:
            form.fields[field].widget.attrs.update({'readonly': 'readonly', 'disabled': 'disabled'})
        form.fields.keyOrder = ['title', 'sender', 'body']
        selected_instances[0].state = Message.UNREAD
        selected_instances[0].save()
        return render_to_response('manager/actions/show.html', {'form': form, 'title': u"مشاهده پیام"},
                                  context_instance=RequestContext(http_request))


class SendEmail(ManagerAction):
    action_name = 'send_email'
    action_verbose_name = u"ارسال پست الکترونیک"
    is_view = True
    height = '550'

    def action_view(self, http_request, selected_instances):
        if not PermissionController.is_admin(http_request.user):
            raise Http404
        if http_request.method == 'POST':
            form = EmailSendForm(http_request.POST)
            if form.is_valid():
                email = form.cleaned_data.get('email')
                receivers = form.cleaned_data.get('receivers')
                subject = form.cleaned_data.get('subject')
                body = form.cleaned_data.get('body')
                MessageServices.send_mass_message(subject, body, receivers,email)
                form = None
                messages.success(http_request, u"پست الکترونیک ارسال شد.")
        else:
            form = EmailSendForm()

        return render_to_response('manager/actions/add_edit.html', {'form': form, 'title': u"ارسال پیام"},
                                  context_instance=RequestContext(http_request))
