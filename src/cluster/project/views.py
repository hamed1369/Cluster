# -*- coding:utf-8 -*-
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from cluster.account.account.models import Member
from cluster.project.handlers import ProjectHandler
from cluster.project.models import ProjectArbiter
from cluster.utils.permissions import PermissionController


@login_required
def register(request):
    if not PermissionController.is_member(request.user):
        raise Http404()

    member = Member.objects.get(user=request.user)

    if not member.is_confirmed:
        messages.error(request, u"تا زمان عدم تایید عضویت شما از طریق مدیریت سامانه شما قادر به ایجاد طرح نیستید.")
        return render_to_response('show_message.html', {}, context_instance=RequestContext(request))

    project_handler = ProjectHandler(request)

    project_handler.initial_forms()
    if project_handler.is_valid_forms():
        project_handler.save_forms()
        messages.success(request, u"ثبت نام طرح با موفقیت انجام شد.")
        return render_to_response('show_message.html', {}, context_instance=RequestContext(request))

    context = project_handler.get_context()
    return render_to_response('project/register.html',
                              context,
                              context_instance=RequestContext(request))


@login_required
def view_arbiter_comment(request, project_arbiter_id):
    if (not PermissionController.is_admin(request.user) and not PermissionController.is_supervisor(
            request.user)) or not project_arbiter_id:
        raise Http404()
    project_arbiter = get_object_or_404(ProjectArbiter, id=project_arbiter_id)
    return render_to_response('project/view_arbiter_comment.html', {'project_arbiter': project_arbiter},
                              context_instance=RequestContext(request))
