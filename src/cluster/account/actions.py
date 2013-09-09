# -*- coding: utf-8 -*-
from django import forms
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from cluster.utils.forms import ClusterBaseModelForm, ClusterBaseForm
from cluster.utils.manager.action import ManagerAction

__author__ = 'M.Y'


class ChangeUserName(ManagerAction):
    action_name = 'change_user_name'
    action_verbose_name = u"تغییر نام"
    is_view = True

    def action_view(self, http_request, selected_instances):
        if selected_instances:
            class UserForm(ClusterBaseForm):
                first_name = forms.CharField(label=u"نام")
                last_name = forms.CharField(label=u"نام خانوادگی")

            if http_request.method == 'POST':
                form = UserForm(http_request.POST)
                if form.is_valid():
                    first_name = form.cleaned_data.get('first_name')
                    last_name = form.cleaned_data.get('last_name')
                    selected_instances[0].first_name = first_name
                    selected_instances[0].last_name = last_name
                    selected_instances[0].save()
                    messages.success(http_request, u"تغییر نام با موفقیت انجام شد.")
            else:
                form = UserForm()
            return render_to_response('accounts/simple_action_form.html', {'form': form},
                                      context_instance=RequestContext(http_request))
        raise Http404()
