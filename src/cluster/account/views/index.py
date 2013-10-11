# -*- coding:utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from cluster.account.forms import SignInForm
from cluster.news.models import News

__author__ = 'M.Y'


def index(request):
    login_form = SignInForm()
    news_list = News.objects.all().order_by('-publish_date')
    return render_to_response('intro.html', {'login_form':login_form,'news_list':news_list}, context_instance=RequestContext(request))
