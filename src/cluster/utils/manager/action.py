# -*- coding: utf-8 -*-
from django.contrib import messages
from django.http import Http404
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


class EditAction(ManagerAction):
    is_view = True

    def __init__(self, modelForm, action_name='edit', action_verbose_name=u"ویرایش", form_title=u"ویرایش"):
        self.action_name = action_name
        self.action_verbose_name = action_verbose_name
        self.modelForm = modelForm
        self.form_title = form_title

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

    def __init__(self, do_function=None, action_name='delete', action_verbose_name=u"حذف"):
        if do_function:
            self.do = do_function
        self.action_name = action_name
        self.action_verbose_name = action_verbose_name

    def do(self, http_request, selected_instances):
        for user in selected_instances:
            user.delete()


class ShowAction(ManagerAction):
    action_name = 'show'
    action_verbose_name = u"مشاهده جزئیات"
    is_view = True

    def __init__(self, modelForm, action_name='show', action_verbose_name=u"مشاهده جزئیات", form_title=u"مشاهده"):
        self.action_name = action_name
        self.action_verbose_name = action_verbose_name
        self.modelForm = modelForm
        self.form_title = form_title

    def action_view(self, http_request, selected_instances):
        form = self.modelForm(instance=selected_instances[0])
        for field in form.fields:
            form.fields[field].widget.attrs.update({'readonly': 'readonly', 'disabled': 'disabled'})
        return render_to_response('manager/actions/show.html', {'form': form, 'title': self.form_title},
                                  context_instance=RequestContext(http_request))
