# -*- coding:utf-8 -*-
from django.contrib import messages
from django.shortcuts import render_to_response
from django.template import RequestContext
from cluster.account.forms import SignInForm
from cluster.feedback.forms import ContactForm
from cluster.news.models import News, Link

__author__ = 'M.Y'


def index(request):
    login_form = SignInForm()
    news_list = News.objects.all().order_by('-publish_date')
    links_list = Link.objects.all().order_by('order')
    if request.method == 'POST':
        contact_form = ContactForm(request.POST, prefix='contact')
        if contact_form.is_valid():
            contact_form.save()
            has_submited = True
            contact_form = ContactForm(prefix='contact')
    else:
        has_submited = False
        contact_form = ContactForm(prefix='contact')
    return render_to_response('intro.html',
                              {'login_form': login_form,'has_submited':has_submited, 'news_list': news_list,'links_list': links_list, 'contact_form': contact_form},
                              context_instance=RequestContext(request))
