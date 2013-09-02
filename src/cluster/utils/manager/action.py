# -*- coding: utf-8 -*-
from django.contrib import messages
from django.shortcuts import render_to_response
from django.template.context import RequestContext

__author__ = 'M.Y'


class ManagerAction(object):
    action_name = u""  # the name that use for creating js and ajax
    action_verbose_name = u""  # the name that show to user
    is_view = False  # if True should override action_view

    def do(self, http_request, selected_instances):
        pass

    def action_view(self, http_request, selected_instances):
        pass


class AddAction(ManagerAction):
    is_view = True

    def __init__(self, modelForm, action_name='add', action_verbose_name=u"افزودن", form_title=u"افزودن"):
        self.action_name = action_name
        self.action_verbose_name = action_verbose_name
        self.modelForm = modelForm
        self.form_title = form_title

    def action_view(self, http_request, selected_instances):
        if http_request.method == 'POST':
            form = self.modelForm(http_request.POST)
            if form.is_valid():
                form.save()
                form = None
                messages.success(http_request, u"%s با موفقیت انجام شد." % self.form_title)
        else:
            form = self.modelForm()

        return render_to_response('manager/actions/add_edit.html', {'form': form, 'title': self.form_title},
                                  context_instance=RequestContext(http_request))