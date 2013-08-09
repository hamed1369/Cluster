# -*- coding:utf-8 -*-
from django.core.mail import send_mail
from django.forms.formsets import formset_factory
from django.forms.models import modelformset_factory
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from cluster.account.personal_info.models import EducationalResume, Publication, Invention, \
    ExecutiveResearchProject, LanguageSkill, SoftwareSkill
from cluster.registration.forms import ClusterForm, RegisterForm, MemberForm

CLusterMemberForm = formset_factory(MemberForm)
ResumeForm = modelformset_factory(EducationalResume, exclude=('cluster_member', ))
PublicationForm = modelformset_factory(Publication, exclude=('cluster_member', ))
InventionForm = modelformset_factory(Invention, exclude=('cluster_member', ))
ExecutiveResearchProjectForm = modelformset_factory(ExecutiveResearchProject, exclude=('cluster_member', ))
LanguageSkillForm = modelformset_factory(LanguageSkill, exclude=('cluster_member', ))
SoftwareSkillForm = modelformset_factory(SoftwareSkill, exclude=('cluster_member', ))


def register(request, cluster_id=None):
    if request.method == 'POST':
        cluster_form = ClusterForm(prefix='cluster', data=request.POST)
        if cluster_form.is_valid():
            pass
        register_form = RegisterForm(prefix='register', data=request.POST)
        if register_form.is_valid():
            pass
        cluster_member_formset = CLusterMemberForm(prefix='cluster_member', data=request.POST)
        if cluster_member_formset.is_valid():
            pass
        resume_formset = ResumeForm(prefix='resume', data=request.POST)
        if resume_formset.is_valid():
            pass
        publication_formset = PublicationForm(prefix='publication', data=request.POST)
        if publication_formset.is_valid():
            pass
        invention_formset = InventionForm(prefix='invention', data=request.POST)
        if invention_formset.is_valid():
            pass
        executive_research_formset = ExecutiveResearchProjectForm(prefix='executive_research', data=request.POST)
        if executive_research_formset.is_valid():
            pass
        language_skill_formset = LanguageSkillForm(prefix='language_skill', data=request.POST)
        if language_skill_formset.is_valid():
            pass
        software_skill_formset = SoftwareSkillForm(prefix='software_skill', data=request.POST)
        if software_skill_formset.is_valid():
            pass
    else:
        cluster_form = ClusterForm(prefix='cluster')
        register_form = RegisterForm(prefix='register')
        cluster_member_formset = CLusterMemberForm(prefix='cluster_member')
        resume_formset = ResumeForm(prefix='resume')
        publication_formset = PublicationForm(prefix='publication')
        invention_formset = InventionForm(prefix='invention')
        executive_research_formset = ExecutiveResearchProjectForm(prefix='executive_research')
        language_skill_formset = LanguageSkillForm(prefix='language_skill')
        software_skill_formset = SoftwareSkillForm(prefix='software_skill')

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