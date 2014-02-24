# -*- coding: utf-8 -*-
from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from cluster.news.models import News

__author__ = 'hamed'

def news_detail(request,news_id):
    try:
        news = News.objects.get(id=int(news_id))
    except Exception:
        return Http404()
    return render_to_response('news.html', {'news':news},
                          context_instance=RequestContext(request))


def archive(request):
    news_list = News.objects.filter(archived=True).order_by('-publish_date')
    return render_to_response('archive.html', {'news_list':news_list},
                          context_instance=RequestContext(request))
