# -*- coding:utf-8 -*-
'''
Created on 16/08/13

@author: hamed
'''
from django.contrib.auth.decorators import login_required
from django.http import Http404

from django.shortcuts import render_to_response
from django.template import RequestContext
from cluster.account.account.models import Member
from cluster.registration.handlers import ClusterHandler


@login_required
def edit_account(request):
    try:
        member = request.user.member
    except Member.DoesNotExist:
        raise Http404
    handler = ClusterHandler(request, cluster_id=member.cluster_id)
    handler.initial_forms(member=member)
    c = handler.get_context()
    return render_to_response('registration/register.html',
                              c,
                              context_instance=RequestContext(request))