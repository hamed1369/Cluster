# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404, HttpResponse
from django.utils import simplejson
from cluster.utils.manager.main import manager_children

__author__ = 'M.Y'


@login_required
def validationEngine(request):
    field_id = request.GET.get('fieldId')
    field_val = request.GET.get('fieldValue')
    result = [field_id, True]
    if field_id.find('username') > -1:
        try:
            User.objects.get(username=field_val)
            result = [field_id, False]
        except User.DoesNotExist:
            pass
    elif field_id.find('email') > -1:
        try:
            users = User.objects.filter(email=field_val)
            if users:
                result = [field_id, False]
        except User.DoesNotExist:
            pass

    json = simplejson.dumps(result)
    return HttpResponse(json, mimetype='application/json')
