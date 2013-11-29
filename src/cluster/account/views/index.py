# -*- coding:utf-8 -*-
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.base import Template
from django.template.loader import render_to_string
from cluster.account.forms import SignInForm
from cluster.account.management.forms import IntroPageForm
from cluster.account.management.models import IntroPageContent
from cluster.feedback.forms import ContactForm
from cluster.news.models import News, Link

__author__ = 'M.Y'


def index(request):
    login_form = SignInForm()
    links_list = Link.objects.all().order_by('order')
    has_submited = False
    if request.method == 'POST':
        contact_form = ContactForm(request.POST, prefix='contact')
        if contact_form.is_valid():
            contact_form.save()
            has_submited = True
            contact_form = ContactForm(prefix='contact')
    else:
        contact_form = ContactForm(prefix='contact')
    template = Template(IntroPageContent.get_instance().content)
    context = RequestContext(request, {'login_form': login_form, 'has_submited': has_submited, 'news_content': News.get_html(),
                                       'links_list': links_list, 'contact_form': contact_form})
    return HttpResponse(template.render(context))
