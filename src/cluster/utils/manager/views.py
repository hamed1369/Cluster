# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template.context import RequestContext

__author__ = 'M.Y'


@login_required
def process_main_page(request, manager_name):
    return render_to_response('manager/main.html', {}, context_instance=RequestContext(request))


@login_required
def process_actions(request, manager_name):
    pass
