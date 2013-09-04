# -*- coding:utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext

__author__ = 'M.Y'


def index(request):
    return render_to_response('intro.html', {}, context_instance=RequestContext(request))
