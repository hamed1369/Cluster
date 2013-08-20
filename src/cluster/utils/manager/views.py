# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from cluster.utils.manager.main import manager_children

__author__ = 'M.Y'


@login_required
def process_main_page(request, manager_name):
    for manager in manager_children:
        if manager.manager_name == manager_name:
            manager

        return render_to_response('manager/main.html', {}, context_instance=RequestContext(request))
    raise Http404()


@login_required
def process_actions(request, manager_name):
    pass
