# -*- coding:utf-8 -*-
'''
Created on 16/08/13

@author: hamed
'''
import datetime
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect

from django.shortcuts import render_to_response
from django.template import RequestContext
from tracking.models import Visitor
from cluster.account.forms import AdminForm, SupervisorForm
from cluster.registration.handlers import ClusterHandler
from cluster.utils.permissions import PermissionController


@login_required
def handle_member_edit(request):
    member = request.user.member
    if member.is_confirmed is False:
        messages.error(request, u"ثبت نام شما از طرف مدیریت رد شده است و نمی توانید در سامانه وارد شوید.")
        logout(request)
        return HttpResponseRedirect(reverse('login'))
    handler = ClusterHandler(request, cluster_id=member.cluster_id, has_cluster=member.cluster is not None)
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


@login_required
def handle_admin_edit(request):
    if request.method == 'POST':
        form = AdminForm(request.POST, prefix='admin', instance=request.user, http_request=request)
        if form.is_valid():
            form.save()
            messages.success(request, u"ویرایش اطلاعات با موفقیت انجام شد.")
            form = AdminForm(prefix='admin', instance=request.user, http_request=request)
    else:
        form = AdminForm(prefix='admin', instance=request.user, http_request=request)
    return render_to_response('accounts/edit_admin.html', {'form': form}, context_instance=RequestContext(request))


@login_required
def handle_supervisor_edit(request):
    if request.method == 'POST':
        form = SupervisorForm(request.POST, instance=request.user.supervisor, http_request=request)
        if form.is_valid():
            form.save()
            messages.success(request, u"ویرایش اطلاعات با موفقیت انجام شد.")
            form = SupervisorForm(instance=request.user.supervisor, http_request=request)
    else:
        form = SupervisorForm(instance=request.user.supervisor, http_request=request)
    return render_to_response('accounts/edit_supervisor.html', {'form': form}, context_instance=RequestContext(request))


@login_required
def edit_account(request):
    if PermissionController.is_member(request.user):
        return handle_member_edit(request)
    elif PermissionController.is_supervisor(request.user):
        return handle_supervisor_edit(request)
    elif PermissionController.is_admin(request.user):
        return handle_admin_edit(request)
    else:
        raise Http404


class StatisticRecord(object):

    def __init__(self,key,value):
        self.key = key
        self.value = value

def get_statistics():
    today = datetime.date.today
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    last_month = datetime.date.today() - datetime.timedelta(days=30)
    today_visits = Visitor.objects.filter(start_time__gte=today,start_time__lt = tomorrow).count()
    yesterday_visits = Visitor.objects.filter(start_time__gte=yesterday,start_time__lt = today).count()
    last_month_visits = Visitor.objects.filter(start_time__gte=last_month,start_time__lt = tomorrow).count()
    #today_visits = Visitor.objects.filter(session_start__gte=today,session_start__lt = tomorrow).count()
    #yesterday_visits = Visitor.objects.filter(session_start__gte=yesterday,session_start__lt = today).count()
    #last_month_visits = Visitor.objects.filter(session_start__gte=last_month,session_start__lt = tomorrow).count()
    overrall_visits = Visitor.objects.all().count()
    statistics = []
    statistics.append(StatisticRecord('بازدید های امروز',today_visits))
    statistics.append(StatisticRecord('بازدید های دیروز',yesterday_visits))
    statistics.append(StatisticRecord('بازدید های 30 روز گذشته',last_month_visits))
    statistics.append(StatisticRecord('کل بازدیدها',overrall_visits))
    return statistics

@login_required
def statistics(request):
    statistics = get_statistics()
    return render_to_response('statistics.html', {'statistics':statistics},
                      context_instance=RequestContext(request))
