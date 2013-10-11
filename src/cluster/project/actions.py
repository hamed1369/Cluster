# -*- coding: utf-8 -*-
from django.contrib import messages
from django.forms.models import inlineformset_factory
from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from cluster.project.forms import ProjectManagerForm, ProjectForm, AdminProjectManagerForm
from cluster.project.models import Project, ProjectMilestone, ProjectComment
from cluster.utils.forms import ClusterBaseModelForm
from cluster.utils.manager.action import ManagerAction
from cluster.utils.messages import MessageServices, SMSService

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
    ActionForm = ProjectManagerForm

    def action_view(self, http_request, selected_instances):
        if not selected_instances:
            raise Http404()

        instance = selected_instances[0]
        old_state = instance.project_status
        old_state_display = instance.get_project_status_display()
        old_arbiter = instance.arbiter
        inline_form = None
        if http_request.method == 'POST':
            form = self.ActionForm(http_request.POST, instance=instance)
            if old_state > 1:
                inline_form = ProjectMilestoneForm(http_request.POST, instance=instance, prefix='project_milestone')
            inline_form_valid = True
            if inline_form and not inline_form.is_valid():
                inline_form_valid = False

            if form.is_valid() and inline_form_valid:
                if old_state > 1:
                    inline_form.save()
                instance = form.save()
                form = None
                new_state = instance.project_status
                new_state_display = instance.get_project_status_display()
                new_arbiter = instance.arbiter
                if old_state != new_state:
                    message_body = u'وضعیت طرح "%s" از "%s" به "%s" تغییر پیدا کرد.' % (
                        instance.title, old_state_display, new_state_display)
                    message = MessageServices.get_title_body_message(u"تغییر وضعیت طرح", message_body)
                    if instance.single_member:
                        member = instance.single_member
                    else:
                        member = instance.cluster.head
                    MessageServices.send_message(u"تغییر وضعیت طرح", message, member.user)
                    SMSService.send_sms(message_body, [member.mobile])

                if old_arbiter != new_arbiter and new_arbiter:
                    message_body = u'%s محترم، مدیریت سامانه موسسه پژوهشی نگاه نو طرح با عنوان "%s" را برای داوری به شما سپرده است.' % (
                        unicode(new_arbiter.user), instance.title)
                    message = MessageServices.get_title_body_message(u"ارسال طرح به شما برای داوری", message_body)
                    MessageServices.send_message(u"ارسال طرح به شما برای داوری", message, new_arbiter.user)
                    SMSService.send_sms(message_body, [new_arbiter.mobile])

                messages.success(http_request, u"بررسی طرح با موفقیت انجام شد.")
        else:
            form = self.ActionForm(instance=instance)
            if instance.project_status > 1:
                inline_form = ProjectMilestoneForm(instance=instance, prefix='project_milestone')

        return render_to_response('project/check_project.html',
                                  {'form': form, 'inline_form': inline_form, 'title': u"بررسی طرح",
                                   'project': instance},
                                  context_instance=RequestContext(http_request))


class AdminProjectCheckAction(ProjectCheckAction):
    ActionForm = AdminProjectManagerForm


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
        inline_form = None
        if instance.project_status > 1:
            inline_form = ProjectMilestoneForm(instance=instance, prefix='project_milestone')
            inline_form.readonly = True

        if http_request.method == 'POST':
            comment_txt = http_request.POST.get('project-comment-text')
            if comment_txt:
                ProjectComment.objects.create(user=http_request.user, comment=comment_txt, project=instance)

        project = None
        if self.for_admin:
            project = instance

        return render_to_response('project/show_project.html',
                                  {'form': form, 'inline_form': inline_form, 'title': u"جزئیات طرح",
                                   'project': project, 'comments': instance.comments.all()},
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

            inline_form = None
            if instance.project_status > 1:
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
