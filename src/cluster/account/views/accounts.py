# -*- coding:utf-8 -*-
'''
Created on 16/08/13

@author: hamed
'''
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404

from django.shortcuts import render_to_response
from django.template import RequestContext
from cluster.account.account.models import Member
from cluster.account.forms import AdminForm
from cluster.registration.handlers import ClusterHandler
from cluster.utils.permissions import PermissionController


def handle_member_edit(request):
    member = request.user.member
    handler = ClusterHandler(request, cluster_id=member.cluster_id)
    handler.initial_forms(member=member)

    if handler.is_valid_forms():
        handler.save_forms()
        messages.success(request, u"ویرایش اطلاعات با موفقیت انجام شد.")
        handler = ClusterHandler(request, cluster_id=member.cluster_id)
        handler.initial_forms(member=member, check_post=False)

    c = handler.get_context()
    return render_to_response('accounts/edit_accounts.html',
                              c,
                              context_instance=RequestContext(request))


def handle_admin_edit(request):
    if request.method == 'POST':
        form = AdminForm(request.POST, prefix='admin', instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, u"ویرایش اطلاعات با موفقیت انجام شد.")
            form = AdminForm(prefix='admin', instance=request.user)
    else:
        form = AdminForm(prefix='admin', instance=request.user)
    return render_to_response('accounts/edit_admin.html', {'form': form}, context_instance=RequestContext(request))


@login_required
def edit_account(request):
    if PermissionController.is_member(request.user):
        return handle_member_edit(request)
    elif PermissionController.is_admin(request.user):
        return handle_admin_edit(request)
    else:
        raise Http404
