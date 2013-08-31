# -*- coding:utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

__author__ = 'M.Y'


@login_required
def index(request):
    return HttpResponseRedirect(reverse('edit_accounts'))
