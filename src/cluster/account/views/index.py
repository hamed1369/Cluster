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
from cluster.account.views.accounts import get_statistics
from cluster.feedback.forms import ContactForm
from cluster.news.models import News, Link
from cluster.project.models import Project

__author__ = 'M.Y'


def index(request):
    login_form = SignInForm()

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
    projects = Project.get_projects_content(request)
    statistics = get_statistics(request)
    links = Link.get_links_content(request)
    context = RequestContext(request, {'login_form': login_form, 'has_submited': has_submited,'projects':projects, 'news_content': News.get_html(),
                                       'links': links, 'contact_form': contact_form,'statistics':statistics})
    #return HttpResponse(template.render(context))
    # return HttpResponse(template.render(context))
    return render_to_response('intro.html',context)