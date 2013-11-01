# -*- coding:utf-8 -*-
from django.contrib import messages
from django.shortcuts import render_to_response
from django.template import RequestContext
from cluster.account.forms import SignInForm
from cluster.feedback.forms import ContactForm
from cluster.news.models import News

__author__ = 'M.Y'


def index(request):
    login_form = SignInForm()
    news_list = News.objects.all().order_by('-publish_date')
    if request.method == 'POST':
        contact_form = ContactForm(request.POST, prefix='contact')
        if contact_form.is_valid():
            contact_form.save()
            messages.success(request, u"متن شما برای مدیریت سامانه ارسال شد. باتشکر")
            contact_form = ContactForm(prefix='contact')
    else:
        contact_form = ContactForm(prefix='contact')
    return render_to_response('intro.html',
                              {'login_form': login_form, 'news_list': news_list, 'contact_form': contact_form},
                              context_instance=RequestContext(request))
