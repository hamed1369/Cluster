# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from cluster.utils.manager.main import manager_children

__author__ = 'M.Y'


@login_required
def process_main_page(request, manager_name):
    for manager in manager_children:
        if manager.manager_name == manager_name:
            manager_obj = manager(http_request=request)
            if not manager_obj.can_view():
                raise Http404()
            manager_content = manager_obj.render_main_list()

            c = {
                'manager_content': manager_content
            }

            return render_to_response('manager/main.html', c, context_instance=RequestContext(request))
    raise Http404()


@login_required
def process_actions(request, manager_name):
    for manager in manager_children:
        if manager.manager_name == manager_name:
            manager_obj = manager(http_request=request)
            if not manager_obj.can_view():
                raise Http404()
            return manager_obj.process_action_request()
    raise Http404()