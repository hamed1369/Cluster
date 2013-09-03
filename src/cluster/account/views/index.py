# -*- coding:utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

__author__ = 'M.Y'



def index(request):
    return render_to_response('intro.html', {}, context_instance=RequestContext(request))
