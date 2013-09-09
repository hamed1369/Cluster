# -*- coding: utf-8 -*-
from cluster.message.forms import MessageForm, MessageShowForm
from cluster.message.models import Message

__author__ = 'M.Y'


# -*- coding: utf-8 -*-
from django.contrib import messages
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from cluster.utils.manager.action import ManagerAction

__author__ = 'M.Y'


class SendMessage(ManagerAction):
    action_name = 'send_message'
    action_verbose_name = u"ارسال پیام جدید"
    is_view = True

    def action_view(self, http_request, selected_instances):

        if http_request.method == 'POST':
            form = MessageForm(http_request.POST, user=http_request.user)
            if form.is_valid():
                form.save()
                form = None
                messages.success(http_request, u"پیام ارسال شد.")
        else:
            form = MessageForm(user=http_request.user)
        return render_to_response('manager/actions/add_edit.html', {'form': form, 'title': u"ارسال پیام"},
                                  context_instance=RequestContext(http_request))


class ShowMessage(ManagerAction):
    action_name = 'show_message'
    action_verbose_name = u"مشاهده پیام"
    is_view = True

    def action_view(self, http_request, selected_instances):
        form = MessageShowForm(instance=selected_instances[0])
        for field in form.fields:
            form.fields[field].widget.attrs.update({'readonly': 'readonly', 'disabled': 'disabled'})
        form.fields.keyOrder = ['title', 'sender', 'body']
        selected_instances[0].state = Message.UNREAD
        selected_instances[0].save()
        return render_to_response('manager/actions/show.html', {'form': form, 'title': u"مشاهده پیام"},
                                  context_instance=RequestContext(http_request))
