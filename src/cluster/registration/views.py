# -*- coding:utf-8 -*-
from django.forms.formsets import formset_factory
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from cluster.registration.forms import RegisterForm, MemberForm, EducationalResumeForm, PublicationForm, \
    InventionForm, ExecutiveResearchProjectForm, LanguageSkillForm, SoftwareSkillForm, ClusterForm


def register(request, cluster_id=None):
    cluster_form = ClusterForm()
    register_form = RegisterForm()
    cluster_member_formset = formset_factory(MemberForm)
    resume_formset = formset_factory(EducationalResumeForm)
    publication_formset = formset_factory(PublicationForm)
    invention_formset = formset_factory(InventionForm)
    executive_research_formset = formset_factory(ExecutiveResearchProjectForm)
    language_skill_formset = formset_factory(LanguageSkillForm)
    software_skill_formset = formset_factory(SoftwareSkillForm)

    c = {
        'cluster_form': cluster_form,
        'register_form': register_form,
        'cluster_member_formset': cluster_member_formset,
        'resume_formset': resume_formset,
        'publication_formset': publication_formset,
        'invention_formset': invention_formset,
        'executive_research_formset': executive_research_formset,
        'language_skill_formset': language_skill_formset,
        'software_skill_formset': software_skill_formset,
    }
    return render_to_response('registration/register.html',
                              c,
                              context_instance=RequestContext(request))