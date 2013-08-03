# Create your views here.
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from cluster.registration.forms import RegisterForm


def register(request, cluster_id=None):
    register_form = RegisterForm()
    return render_to_response('registration/register.html', {'register_form': register_form},
                              context_instance=RequestContext(request))