# -*- coding: utf-8 -*-
from django import forms
from django.contrib import messages
from django.http import Http404
from django.shortcuts import render_to_response
from django.template.context import RequestContext

__author__ = 'M.Y'


class ManagerAction(object):
    action_name = u""  # the name that use for creating js and ajax
    action_verbose_name = u""  # the name that show to user
    is_view = False  # if True should override action_view

    height = '200'
    width = '800'

    min_count = None

    def do(self, http_request, selected_instances):
        pass

    def action_view(self, http_request, selected_instances):
        pass


class AddAction(ManagerAction):
    is_view = True

    def __init__(self, modelForm, action_name='add', action_verbose_name=u"افزودن", form_title=u"افزودن",
                 save_def=None):
        self.action_name = action_name
        self.action_verbose_name = action_verbose_name
        self.modelForm = modelForm
        self.form_title = form_title
        self.save_def = save_def

    def action_view(self, http_request, selected_instances):
        if http_request.method == 'POST':
            form = self.modelForm(http_request.POST)
            if form.is_valid():
                if self.save_def:
                    instance = form.save(commit=False)
                    self.save_def(http_request, instance)
                else:
                    form.save()
                form = None
                messages.success(http_request, u"%s با موفقیت انجام شد." % self.form_title)
        else:
            form = self.modelForm()

        return render_to_response('manager/actions/add_edit.html', {'form': form, 'title': self.form_title},
                                  context_instance=RequestContext(http_request))


class EditAction(ManagerAction):
    is_view = True

    def __init__(self, modelForm, action_name='edit', action_verbose_name=u"ویرایش", form_title=u"ویرایش",
                 min_count='1'):
        self.action_name = action_name
        self.action_verbose_name = action_verbose_name
        self.modelForm = modelForm
        self.form_title = form_title
        self.min_count = min_count

    def action_view(self, http_request, selected_instances):
        if not selected_instances:
            raise Http404()
        if http_request.method == 'POST':
            form = self.modelForm(http_request.POST, instance=selected_instances[0])
            if form.is_valid():
                form.save()
                form = None
                messages.success(http_request, u"%s با موفقیت انجام شد." % self.form_title)
        else:
            form = self.modelForm(instance=selected_instances[0])

        return render_to_response('manager/actions/add_edit.html', {'form': form, 'title': self.form_title},
                                  context_instance=RequestContext(http_request))


class DeleteAction(ManagerAction):
    action_name = 'delete'
    action_verbose_name = u"حذف"

    def __init__(self, do_function=None, action_name='delete', action_verbose_name=u"حذف", min_count='1',
                 confirm_message=None):
        if do_function:
            self.do = do_function
        self.action_name = action_name
        self.action_verbose_name = action_verbose_name
        self.min_count = min_count
        self.confirm_message = confirm_message
        if not confirm_message:
            self.confirm_message = u"آیا از حذف موارد انتخاب شده اطمینان دارید؟"

    def do(self, http_request, selected_instances):
        for user in selected_instances:
            user.delete()


class ShowAction(ManagerAction):
    action_name = 'show'
    action_verbose_name = u"مشاهده جزئیات"
    is_view = True

    def __init__(self, modelForm, action_name='show', action_verbose_name=u"مشاهده جزئیات", form_title=u"مشاهده",
                 width='800', height='200', min_count='1'):
        self.action_name = action_name
        self.action_verbose_name = action_verbose_name
        self.modelForm = modelForm
        self.form_title = form_title
        self.height = height
        self.width = width
        self.min_count = min_count

    def action_view(self, http_request, selected_instances):
        form = self.modelForm(instance=selected_instances[0])
        for field in form.fields:
            form.fields[field].widget.attrs.update({'readonly': 'readonly', 'disabled': 'disabled'})
        return render_to_response('manager/actions/show.html', {'form': form, 'title': self.form_title},
                                  context_instance=RequestContext(http_request))


class ConfirmAction(ManagerAction):
    is_view = True

    def __init__(self, field_name, action_name='confirm', action_verbose_name=u"بررسی", form_title=u"بررسی",
                 min_count='1', field_label=u"تایید شده", on_change_event=None):
        self.action_name = action_name
        self.action_verbose_name = action_verbose_name
        self.field_name = field_name
        self.form_title = form_title
        self.min_count = min_count
        self.field_label = field_label
        self.height = '200'
        self.on_change_event = on_change_event

    def action_view(self, http_request, selected_instances):
        if not selected_instances:
            raise Http404()

        field_label = self.field_label
        field_val = getattr(selected_instances[0], self.field_name)

        class ConfirmForm(forms.Form):
            confirm = forms.NullBooleanField(label=field_label, initial=field_val, required=False)
            confirm.widget.choices = ((u'1', u"نامشخص"),
                                      (u'2', u"بله"),
                                      (u'3', u"خیر"))

        if http_request.method == 'POST':
            form = ConfirmForm(http_request.POST)
            if form.is_valid():
                confirm = form.cleaned_data.get('confirm')
                setattr(selected_instances[0], self.field_name, confirm)
                selected_instances[0].save()
                form = None
                if self.on_change_event:
                    self.on_change_event(selected_instances[0], confirm)
                messages.success(http_request, u"%s با موفقیت انجام شد." % self.form_title)
        else:
            form = ConfirmForm()

        return render_to_response('manager/actions/add_edit.html', {'form': form, 'title': self.form_title},
                                  context_instance=RequestContext(http_request))
