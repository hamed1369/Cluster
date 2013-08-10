# -*- coding:utf-8 -*-
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.db import transaction
from django.forms.formsets import formset_factory
from django.forms.models import modelformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from cluster.account.account.models import Cluster
from cluster.account.personal_info.models import EducationalResume, Publication, Invention, \
    ExecutiveResearchProject, LanguageSkill, SoftwareSkill
from cluster.project.models import Domain
from cluster.registration.forms import ClusterForm, RegisterForm, MemberForm

CLusterMemberForm = formset_factory(MemberForm)
ClusterDomainForm = modelformset_factory(Domain, exclude=('confirmed', ))

ResumeForm = modelformset_factory(EducationalResume, exclude=('cluster_member', ))
PublicationForm = modelformset_factory(Publication, exclude=('cluster_member', ))
InventionForm = modelformset_factory(Invention, exclude=('cluster_member', ))
ExecutiveResearchProjectForm = modelformset_factory(ExecutiveResearchProject, exclude=('cluster_member', ))
LanguageSkillForm = modelformset_factory(LanguageSkill, exclude=('cluster_member', ))
SoftwareSkillForm = modelformset_factory(SoftwareSkill, exclude=('cluster_member', ))


@transaction.commit_on_success
def register(request, cluster_id=None):
    if request.method == 'POST':
        cluster_form = ClusterForm(prefix='cluster', data=request.POST)
        register_form = RegisterForm(prefix='register', data=request.POST)
        cluster_member_formset = CLusterMemberForm(prefix='cluster_member', data=request.POST)
        cluster_domain_formset = ClusterDomainForm(prefix='cluster_domain', data=request.POST)
        resume_formset = ResumeForm(prefix='resume', data=request.POST)
        publication_formset = PublicationForm(prefix='publication', data=request.POST)
        invention_formset = InventionForm(prefix='invention', data=request.POST)
        executive_research_formset = ExecutiveResearchProjectForm(prefix='executive_research', data=request.POST)
        language_skill_formset = LanguageSkillForm(prefix='language_skill', data=request.POST)
        software_skill_formset = SoftwareSkillForm(prefix='software_skill', data=request.POST)
        if cluster_form.is_valid() and register_form.is_valid() \
            and cluster_member_formset.is_valid() and cluster_domain_formset.is_valid() \
            and resume_formset.is_valid() and publication_formset.is_valid() \
            and invention_formset.is_valid() and executive_research_formset.is_valid() \
            and language_skill_formset.is_valid() and software_skill_formset.is_valid():
            first_name = register_form.cleaned_data.get('first_name')
            last_name = register_form.cleaned_data.get('last_name')
            username = register_form.cleaned_data.get('username')
            email = register_form.cleaned_data.get('email')

            user = User.objects.create(first_name=first_name, last_name=last_name, username=username, email=email, )
            member = register_form.save(commit=False)
            member.user = user
            member.save()

            is_cluster = cluster_form.cleaned_data.get('is_cluster')
            if is_cluster:
                name = cluster_form.cleaned_data.get('name')
                institute = cluster_form.cleaned_data.get('institute')
                cluster = Cluster.objects.create(name=name, institute=institute, head=member)

                member.cluster = cluster

                cluster_domains = cluster_domain_formset.save()
                cluster.domains = cluster_domains

                members_emails = []
                for form in cluster_member_formset.forms:
                    if form.is_valid():
                        first_name = form.cleaned_data.get('first_name')
                        last_name = form.cleaned_data.get('last_name')
                        email = form.cleaned_data.get('email')
                        user = User.objects.create(first_name=first_name, last_name=last_name, username=email,
                                                   email=email, )
                        user.save()
                        members_emails.append(email)
                try:
                    send_mail(subject=u"ثبت نام خوشه", message=u"<a></a>", from_email='mymy47@gmail.com',
                              recipient_list=members_emails)
                except Exception:
                    pass

            resumes = resume_formset.save(commit=False)
            for resume in resumes:
                resume.cluster_member = member
                resume.save()

            publications = publication_formset.save(commit=False)
            for publication in publications:
                publication.cluster_member = member
                publication.save()

            inventions = invention_formset.save(commit=False)
            for invention in inventions:
                invention.cluster_member = member
                invention.save()

            executive_researches = executive_research_formset.save(commit=False)
            for executive_research in executive_researches:
                executive_research.cluster_member = member
                executive_research.save()

            language_skills = language_skill_formset.save(commit=False)
            for language_skill in language_skills:
                language_skill.cluster_member = member
                language_skill.save()

            software_skills = software_skill_formset.save(commit=False)
            for software_skill in software_skills:
                software_skill.cluster_member = member
                software_skill.save()

            messages.success(request, u"ثبت نام شما با موفقیت انجام شد.")
            return HttpResponseRedirect(reverse('login'))

    else:
        cluster_form = ClusterForm(prefix='cluster')
        register_form = RegisterForm(prefix='register')
        cluster_member_formset = CLusterMemberForm(prefix='cluster_member')
        cluster_domain_formset = ClusterDomainForm(prefix='cluster_domain')
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
        'cluster_domain_formset': cluster_domain_formset,
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