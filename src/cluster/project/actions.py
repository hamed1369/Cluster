# -*- coding: utf-8 -*-
from django.contrib import messages
from django.forms.models import inlineformset_factory
from django.http import Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from cluster.project.forms import ProjectManagerForm, ProjectForm, AdminProjectManagerForm, ArbiterProjectManagerForm, MilestoneForm, ProjectArbiterForm, ProjectArbitrationForm
from cluster.project.models import Project, ProjectMilestone, ProjectComment, ProjectArbiter
from cluster.utils.manager.action import ManagerAction
from cluster.utils.messages import MessageServices, SMSService
from cluster.utils.permissions import PermissionController

__author__ = 'M.Y'

ProjectMilestoneFormset = inlineformset_factory(Project, ProjectMilestone, form=MilestoneForm, extra=1)
ProjectArbiterFormset = inlineformset_factory(Project, ProjectArbiter, form=ProjectArbiterForm, extra=1)


class AdminProjectCheckAction(ManagerAction):
    is_view = True
    action_name = u'check_project'
    action_verbose_name = u"بررسی طرح"
    min_count = '1'

    def action_view(self, http_request, selected_instances):
        if not selected_instances:
            raise Http404()

        instance = selected_instances[0]
        old_state = instance.project_status
        old_state_display = instance.get_project_status_display()
        milestone_formset = None
        if http_request.method == 'POST':
            form = AdminProjectManagerForm(http_request.POST, http_request.FILES, instance=instance)
            arbiter_formset = ProjectArbiterFormset(http_request.POST, http_request.FILES, instance=instance,
                                                    prefix='project_arbiter')
            if old_state > 1:
                milestone_formset = ProjectMilestoneFormset(http_request.POST, http_request.FILES, instance=instance,
                                                            prefix='project_milestone')
            milestone_formset_valid = True
            if milestone_formset and not milestone_formset.is_valid():
                milestone_formset_valid = False

            arbiter_formset_valid = True
            if arbiter_formset and not arbiter_formset.is_valid():
                arbiter_formset_valid = False

            if form.is_valid() and milestone_formset_valid and arbiter_formset_valid:
                if old_state > 1:
                    milestone_formset.save()

                instance = form.save()
                form = None
                new_state = instance.project_status
                if new_state == 1:
                    arbiter_formset.save()
                elif new_state < 1:
                    instance.project_arbiters.all().delete()
                new_state_display = instance.get_project_status_display()
                if old_state != new_state:
                    message_body = u'وضعیت طرح "%s" از "%s" به "%s" تغییر پیدا کرد.' % (
                        instance.title, old_state_display, new_state_display)
                    message = MessageServices.get_title_body_message(u"تغییر وضعیت طرح", message_body)
                    if instance.single_member:
                        member = instance.single_member
                    else:
                        member = instance.cluster.head
                    MessageServices.send_message(u"تغییر وضعیت طرح", message, member.user)
                    if new_state == Project.REJECT_STATE:
                        message_body = u'وضعیت طرح "%s" به رد شده تغییر پیدا کرد.' % (
                            instance.title)
                        SMSService.send_sms(message_body, [member.mobile])
                    elif new_state == Project.CONFIRM_STATE:
                        message_body = u'وضعیت طرح "%s" به تاییدشده تغییر پیدا کرد.' % (
                            instance.title)
                        SMSService.send_sms(message_body, [member.mobile])

                for project_arbiter in instance.project_arbiters.all():
                    arbiter = project_arbiter.arbiter
                    #if old_arbiter != new_arbiter and new_arbiter:
                    message_body = u'%s محترم، مدیریت سامانه موسسه پژوهشی نگاه نو طرح با عنوان "%s" را برای داوری به شما سپرده است.' % (
                        unicode(arbiter), instance.title)
                    message = MessageServices.get_title_body_message(u"ارسال طرح برای شما جهت داوری", message_body)
                    MessageServices.send_message(u"ارسال طرح برای شما جهت داوری", message, arbiter.user)
                    #    #SMSService.send_sms(message_body, [new_arbiter.mobile])

                messages.success(http_request, u"بررسی طرح با موفقیت انجام شد.")
        else:
            form = AdminProjectManagerForm(instance=instance)
            if instance.project_status > 1:
                milestone_formset = ProjectMilestoneFormset(instance=instance, prefix='project_milestone')
            arbiter_formset = ProjectArbiterFormset(instance=instance, prefix='project_arbiter')
        return render_to_response('project/check_project.html',
                                  {'form': form, 'milestone_formset': milestone_formset, 'title': u"بررسی طرح",
                                   'project': instance, 'arbiter_formset': arbiter_formset,
                                   'project_arbiters': instance.project_arbiters.all(), },
                                  context_instance=RequestContext(http_request))


class ArbiterProjectCheckAction(ManagerAction):
    is_view = True
    action_name = u'check_project'
    action_verbose_name = u"بررسی طرح"
    min_count = '1'

    def action_view(self, http_request, selected_instances):
        if not selected_instances:
            raise Http404()
        instance = selected_instances[0]
        project_arbiter = get_object_or_404(ProjectArbiter, arbiter=http_request.user.arbiter, project=instance)
        form = ArbiterProjectManagerForm(instance=instance, http_request=http_request)
        for field in form.fields:
            form.fields[field].widget.attrs.update({'readonly': 'readonly', 'disabled': 'disabled'})

        if http_request.method == 'POST':
            inline_form = ProjectArbitrationForm(http_request.POST, http_request.FILES, instance=project_arbiter,
                                                 prefix='project_arbiter')
            if inline_form.is_valid():
                inline_form.save()
                form = None
                messages.success(http_request, u"بررسی طرح با موفقیت انجام شد.")
        else:
            inline_form = ProjectArbitrationForm(instance=project_arbiter, prefix='project_arbiter')

        return render_to_response('project/check_project.html',
                                  {'form': form, 'title': u"بررسی طرح", 'project': instance,
                                   'inline_form': inline_form},
                                  context_instance=RequestContext(http_request))


class ProjectDetailAction(ManagerAction):
    is_view = True
    action_name = u'detail'
    action_verbose_name = u"مشاهده جزئیات"
    min_count = '1'
    for_admin = True

    def __init__(self, has_comments=True):
        super(ProjectDetailAction, self).__init__()
        self.has_comments = has_comments

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

        if http_request.method == 'POST' and self.has_comments:
            comment_txt = http_request.POST.get('project-comment-text')
            if comment_txt:
                comment = ProjectComment.objects.create(user=http_request.user, comment=comment_txt, project=instance)
                if not PermissionController.is_arbiter(http_request.user):
                    comment.seen_by_member = True
                    comment.save()

        project = None
        if self.for_admin:
            project = instance

        if not self.has_comments:
            comments = None
        else:
            if PermissionController.is_member(http_request.user):
                comments = instance.comments.filter(seen_by_member=True).order_by('-id')
            else:
                comments = instance.comments.all().order_by('-id')

        return render_to_response('project/show_project.html',
                                  {'form': form, 'inline_form': inline_form, 'title': u"جزئیات طرح",
                                   'project': project, 'comments': comments, 'has_comments': self.has_comments},
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
            messages.error(http_request, u"طرح شما در جریان افتاده است و امکان ویرایش آن وجود ندارد.")
            return render_to_response('project/show_project.html',
                                      {'form': form, 'inline_form': inline_form, 'title': u"جزئیات طرح",
                                       'has_comments': False},
                                      context_instance=RequestContext(http_request))

        if http_request.method == 'POST':
            form = ProjectForm(http_request.POST, http_request.FILES, instance=instance, user=http_request.user)
            if form.is_valid():
                form.save()
                form = None
                messages.success(http_request, u"ویرایش طرح با موفقیت انجام شد.")
        else:
            form = ProjectForm(instance=instance, user=http_request.user)

        return render_to_response('project/edit_project.html',
                                  {'register_form': form, 'title': u"بررسی طرح"},
                                  context_instance=RequestContext(http_request))
