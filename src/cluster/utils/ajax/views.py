# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
from django.utils import simplejson
from cluster.utils.permissions import PermissionController

__author__ = 'M.Y'


def validationEngine(request):
    field_id = request.GET.get('fieldId')
    field_val = request.GET.get('fieldValue')
    result = [field_id, True]

    if field_id.find('username') > -1:
        try:
            if request.user.is_anonymous():
                User.objects.get(username=field_val)
            else:
                User.objects.get(Q(username=field_val), ~Q(id=request.user.id))
            result = [field_id, False]
        except User.DoesNotExist:
            pass
    elif field_id.find('email') > -1:
        try:
            if request.user.is_anonymous():
                users = User.objects.filter(email=field_val)
            else:
                users = User.objects.filter(Q(email=field_val), ~Q(id=request.user.id))
            if users:
                result = [field_id, False]
        except User.DoesNotExist:
            pass

    json = simplejson.dumps(result)
    return HttpResponse(json, mimetype='application/json')


@login_required
def select2(request):
    term = request.GET.get('q')
    result = {}
    if term:
        allow_users = PermissionController.get_available_receivers(request.user)
        if term:
            query = Q(username__icontains=term) | Q(first_name__icontains=term) | Q(last_name__icontains=term)
            allow_users = allow_users.filter(query)
            for user in allow_users:
                result[user.username] = {'id': user.id, 'name': unicode(user)}
    json = simplejson.dumps(result)
    return HttpResponse(json, mimetype='application/json')
