# -*- coding:utf-8 -*-
'''
Created on 16/08/13

@author: hamed
'''


from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext


def edit_account(request):
    context = {}
    return render_to_response('accounts/edit_accounts.html',
                          context,
                          context_instance=RequestContext(request))