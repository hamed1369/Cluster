# -*- coding:utf-8 -*-
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from cluster.feedback.forms import FeedbackForm
from cluster.utils.permissions import PermissionController


@login_required
def send_feedback(request):
    if not PermissionController.is_member(request.user) and not PermissionController.is_arbiter(request.user):
        raise Http404()

    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.creator = request.user
            feedback.save()
            messages.success(request, u"نظر یا پیشنهاد شما با موفقیت ارسال شد.")
            return render_to_response('show_message.html', {}, context_instance=RequestContext(request))
    else:
        form = FeedbackForm()
    return render_to_response('feedback/feedback.html',
                              {'form': form},
                              context_instance=RequestContext(request))