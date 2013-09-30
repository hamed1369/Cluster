# -*- coding: utf-8 -*-
from django.contrib import messages
from django.forms.models import inlineformset_factory
from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from cluster.project.forms import ProjectManagerForm, ProjectForm
from cluster.project.models import Project, ProjectMilestone
from cluster.utils.forms import ClusterBaseModelForm
from cluster.utils.manager.action import ManagerAction
from cluster.utils.messages import MessageServices

__author__ = 'M.Y'


class MilestoneForm(ClusterBaseModelForm):
    js_validation_configs = {
        'required': False,
    }

    class Meta:
        model = ProjectMilestone
        exclude = ('is_announced',)


ProjectMilestoneForm = inlineformset_factory(Project, ProjectMilestone, form=MilestoneForm, extra=1)


class ProjectCheckAction(ManagerAction):
    is_view = True
    action_name = u'check_project'
    action_verbose_name = u"بررسی طرح"
    min_count = '1'

    def action_view(self, http_request, selected_instances):
        if not selected_instances:
            raise Http404()

        instance = selected_instances[0]
        old_state = instance.project_status

        if http_request.method == 'POST':
            form = ProjectManagerForm(http_request.POST, instance=instance)
            inline_form = ProjectMilestoneForm(http_request.POST, instance=instance, prefix='project_milestone')
            if form.is_valid() and inline_form.is_valid():
                instance = form.save()
                inline_form.save()
                form = None
                new_state = instance.project_status
                if old_state != new_state:
                    message = MessageServices.get_title_body_message(u"تغییر وضعیت طرح",
                                                                     u"وضعیت طرح %s از %s به %s تغییر پیدا کرد." % (
                                                                         instance.title, old_state, new_state))
                    if instance.single_member:
                        user = instance.single_member.user
                    else:
                        user = instance.cluster.head.user
                    MessageServices.send_message(u"تغییر وضعیت طرح", message, user)

                messages.success(http_request, u"بررسی طرح با موفقیت انجام شد.")
        else:
            form = ProjectManagerForm(instance=instance)
            inline_form = ProjectMilestoneForm(instance=instance, prefix='project_milestone')

        return render_to_response('project/check_project.html',
                                  {'form': form, 'inline_form': inline_form, 'title': u"بررسی طرح",
                                   'project': instance},
                                  context_instance=RequestContext(http_request))


class ProjectDetailAction(ManagerAction):
    is_view = True
    action_name = u'detail'
    action_verbose_name = u"مشاهده جزئیات"
    min_count = '1'
    for_admin = True

    def action_view(self, http_request, selected_instances):
        if not selected_instances:
            raise Http404()

        ProjectMilestoneForm = inlineformset_factory(Project, ProjectMilestone, form=MilestoneForm, extra=0)
        instance = selected_instances[0]
        form = ProjectManagerForm(instance=instance)
        for field in form.fields:
            form.fields[field].widget.attrs.update({'readonly': 'readonly', 'disabled': 'disabled'})
        inline_form = ProjectMilestoneForm(instance=instance, prefix='project_milestone')
        inline_form.readonly = True

        project = None
        if self.for_admin:
            project = instance

        return render_to_response('project/show_project.html',
                                  {'form': form, 'inline_form': inline_form, 'title': u"جزئیات طرح",
                                   'project': project},
                                  context_instance=RequestContext(http_request))


class ProjectDetailMemberAction(ProjectDetailAction):
    for_admin = False


class EditProjectAction(ManagerAction):
    is_view = True
    action_name = u'edit_project'
    action_verbose_name = u"ویرایش طرح"
    min_count = '1'

    def action_view(self, http_request, selected_instances):
        if not selected_instances:
            raise Http404()

        instance = selected_instances[0]
        if instance.project_status > 0:
            ProjectMilestoneForm = inlineformset_factory(Project, ProjectMilestone, form=MilestoneForm, extra=0)
            form = ProjectManagerForm(instance=instance)
            for field in form.fields:
                form.fields[field].widget.attrs.update({'readonly': 'readonly', 'disabled': 'disabled'})
            inline_form = ProjectMilestoneForm(instance=instance, prefix='project_milestone')
            inline_form.readonly = True
            messages.error(http_request, u"طرح شما تایید شده است و امکان ویرایش آن وجود ندارد.")
            return render_to_response('project/show_project.html',
                                      {'form': form, 'inline_form': inline_form, 'title': u"جزئیات طرح"},
                                      context_instance=RequestContext(http_request))

        if http_request.method == 'POST':
            form = ProjectForm(http_request.POST, instance=instance, user=http_request.user)
            if form.is_valid():
                form.save()
                form = None
                messages.success(http_request, u"ویرایش طرح با موفقیت انجام شد.")
        else:
            form = ProjectForm(instance=instance, user=http_request.user)

        return render_to_response('project/edit_project.html',
                                  {'register_form': form, 'title': u"بررسی طرح"},
                                  context_instance=RequestContext(http_request))

