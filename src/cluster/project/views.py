# -*- coding:utf-8 -*-
from django.contrib import messages
from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from cluster.project.handlers import ProjectHandler
from cluster.utils.permissions import PermissionController


def register(request):

    if not PermissionController.is_member(request.user):
        raise Http404()

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