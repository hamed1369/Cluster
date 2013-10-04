# -*- coding: utf-8 -*-
from django import forms
from django.contrib import messages
from django.http import Http404
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from cluster.account.account.models import Member
from cluster.registration.handlers import ClusterHandler
from cluster.utils.forms import ClusterBaseForm
from cluster.utils.manager.action import ManagerAction
from cluster.utils.messages import MessageServices

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


class ClusterConfirmAction(ManagerAction):
    is_view = True

    def __init__(self, action_name='confirm', action_verbose_name=u"بررسی", form_title=u"بررسی",
                 min_count='1', field_label=u"تایید شده"):
        self.action_name = action_name
        self.action_verbose_name = action_verbose_name
        self.form_title = form_title
        self.min_count = min_count
        self.field_label = field_label

    def action_view(self, http_request, selected_instances):
        if not selected_instances:
            raise Http404()

        field_label = self.field_label
        field_val = selected_instances[0].head.is_confirmed

        class ConfirmForm(forms.Form):
            confirm = forms.NullBooleanField(label=field_label, initial=field_val, required=False)

        if http_request.method == 'POST':
            form = ConfirmForm(http_request.POST)
            if form.is_valid():
                confirm = form.cleaned_data.get('confirm')
                for user_domain in selected_instances[0].user_domains.all():
                    try:
                        user_domain.user.member.is_confirmed = confirm
                        user_domain.save()
                    except Member.DoesNotExist:
                        pass
                selected_instances[0].head.is_confirmed = confirm
                selected_instances[0].head.save()

                if confirm is True:
                    message = MessageServices.get_title_body_message(u"تایید خوشه",
                                                                     u"وضعیت خوشه شما با نام  %s به تاییدشده تغییر یافت.\n هم اکنون شما میتوانید در سامانه فعالیت داشته باشید." %
                                                                     selected_instances[0].name)
                elif confirm is False:
                    message = MessageServices.get_title_body_message(u"تغییر وضعیت خوشه",
                                                                     u"عضویت خوشه شما با نام %s  در سامانه از طرف مدیریت رد  شد. شما دیگر نمیتوانید در سامانه فعالیت داشته باشید." %
                                                                     selected_instances[0].name)
                else:
                    message = MessageServices.get_title_body_message(u"تغییر وضعیت خوشه",
                                                                     u"وضعیت خوشه شما با نام  %s به نامشخص تغییر یافت." %
                                                                     selected_instances[0].name)

                MessageServices.send_message(u"تغییر وضعیت خوشه", message, selected_instances[0].head.user)
                if confirm is False:
                    selected_instances[0].delete()

                form = None
                messages.success(http_request, u"%s با موفقیت انجام شد." % self.form_title)
        else:
            form = ConfirmForm()

        return render_to_response('manager/actions/add_edit.html', {'form': form, 'title': self.form_title},
                                  context_instance=RequestContext(http_request))


class EditMemberAction(ManagerAction):
    is_view = True
    min_count = 1
    action_name = 'edit_member'
    action_verbose_name = u"ویرایش"

    def action_view(self, http_request, selected_instances):
        instance = selected_instances[0]
        member = instance
        handler = ClusterHandler(http_request, cluster_id=member.cluster_id, has_cluster=False)
        handler.initial_forms(member=member)
        if handler.is_valid_forms():
            handler.save_forms()
            messages.success(http_request, u"ویرایش اطلاعات با موفقیت انجام شد.")
            return render_to_response('accounts/edit_member_action.html', {},
                                      context_instance=RequestContext(http_request))

        c = handler.get_context()
        return render_to_response('accounts/edit_member_action.html', c,
                                  context_instance=RequestContext(http_request))


class EditClusterAction(ManagerAction):
    is_view = True
    min_count = 1
    action_name = 'edit_cluster'
    action_verbose_name = u"ویرایش"

    def action_view(self, http_request, selected_instances):
        cluster = selected_instances[0]
        handler = ClusterHandler(http_request, cluster_id=cluster.id, has_register=False, member=cluster.head)
        handler.initial_forms()
        if handler.is_valid_forms():
            handler.save_only_cluster(cluster.head)
            messages.success(http_request, u"ویرایش اطلاعات با موفقیت انجام شد.")
            return render_to_response('accounts/edit_member_action.html', {},
                                      context_instance=RequestContext(http_request))

        c = handler.get_context()
        return render_to_response('accounts/edit_member_action.html', c,
                                  context_instance=RequestContext(http_request))


def on_no_cluster_member_confirm_change(instance, confirm):
    if confirm:
        message = MessageServices.get_title_body_message(u"تغییر وضعیت عضویت",
                                                         u"وضعیت عضویت شما به تاییدنشده تغییر یافت.")
    else:
        message = MessageServices.get_title_body_message(u"تایید عضویت",
                                                         u"وضعیت عضویت شما به تاییدشده تغییر یافت.")
    MessageServices.send_message(u"تغییر وضعیت خوشه", message, instance.user)
