# -*- coding:utf-8 -*-
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db import transaction
from cluster.account.account.models import Cluster
from cluster.account.personal_info.models import EducationalResume, SoftwareSkill, LanguageSkill, \
    ExecutiveResearchProject, Invention, Publication
from cluster.project.models import Domain
from cluster.registration.forms import ClusterForm, RegisterForm, ClusterMemberForm, ClusterDomainForm, ResumeForm, \
    PublicationForm, InventionForm, ExecutiveResearchProjectForm, LanguageSkillForm, SoftwareSkillForm

__author__ = 'M.Y'


class RegisterHandler(object):
    def __init__(self, http_request, cluster_id):
        self.http_request = http_request
        self.http_method = self.http_request.method
        self.cluster_id = cluster_id
        self.cluster = None
        if self.cluster_id:
            self.cluster = Cluster.objects.get(id=cluster_id)

    def initial_forms(self):
        self.__init_cluster_form()
        if self.http_request.method == 'POST':
            self.register_form = RegisterForm(prefix='register', data=self.http_request.POST)
            self.resume_formset = ResumeForm(prefix='resume', data=self.http_request.POST,
                                             queryset=EducationalResume.objects.none())
            self.publication_formset = PublicationForm(prefix='publication', data=self.http_request.POST,
                                                       queryset=Publication.objects.none())
            self.invention_formset = InventionForm(prefix='invention', data=self.http_request.POST,
                                                   queryset=Invention.objects.none())
            self.executive_research_formset = ExecutiveResearchProjectForm(prefix='executive_research',
                                                                           data=self.http_request.POST,
                                                                           queryset=ExecutiveResearchProject.objects.none())
            self.language_skill_formset = LanguageSkillForm(prefix='language_skill', data=self.http_request.POST,
                                                            queryset=LanguageSkill.objects.none())
            self.software_skill_formset = SoftwareSkillForm(prefix='software_skill', data=self.http_request.POST,
                                                            queryset=SoftwareSkill.objects.none())
        else:
            self.register_form = RegisterForm(prefix='register')
            self.resume_formset = ResumeForm(prefix='resume', queryset=EducationalResume.objects.none())
            self.publication_formset = PublicationForm(prefix='publication', queryset=Publication.objects.none())
            self.invention_formset = InventionForm(prefix='invention', queryset=Invention.objects.none())
            self.executive_research_formset = ExecutiveResearchProjectForm(prefix='executive_research',
                                                                           queryset=ExecutiveResearchProject.objects.none())
            self.language_skill_formset = LanguageSkillForm(prefix='language_skill',
                                                            queryset=LanguageSkill.objects.none())
            self.software_skill_formset = SoftwareSkillForm(prefix='software_skill',
                                                            queryset=SoftwareSkill.objects.none())

    def __init_cluster_form(self):
        if self.http_method == 'POST':
            self.cluster_form = ClusterForm(prefix='cluster', data=self.http_request.POST)
            if not self.cluster:
                self.cluster_member_formset = ClusterMemberForm(prefix='cluster_member', data=self.http_request.POST)
            self.cluster_domain_formset = ClusterDomainForm(prefix='cluster_domain', data=self.http_request.POST,
                                                            queryset=Domain.objects.none() if not self.cluster else Domain.objects.filter(
                                                                clusters=self.cluster))
        else:
            self.cluster_form = ClusterForm(prefix='cluster')
            if not self.cluster:
                self.cluster_member_formset = ClusterMemberForm(prefix='cluster_member')
            self.cluster_domain_formset = ClusterDomainForm(prefix='cluster_domain',
                                                            queryset=Domain.objects.none() if not self.cluster else Domain.objects.filter(
                                                                clusters=self.cluster))

        if self.cluster:
            self.cluster_form.fields['is_cluster'].initial = 1
            self.cluster_form.fields['name'].initial = self.cluster.name
            self.cluster_form.fields['name'].widget.attrs.update({'readonly': 'readonly'})
            self.cluster_form.fields['institute'].initial = self.cluster.institute
            self.cluster_form.fields['institute'].widget.attrs.update({'readonly': 'readonly'})
            for form in self.cluster_domain_formset.forms:
                for field in form.fields:
                    form.fields[field].widget.attrs.update({'readonly': 'readonly'})
            self.cluster_member_formset = None

    def __save_cluster(self, member):
        if not self.cluster:
            is_cluster = self.cluster_form.cleaned_data.get('is_cluster')
            if is_cluster:
                name = self.cluster_form.cleaned_data.get('name')
                institute = self.cluster_form.cleaned_data.get('institute')
                cluster = Cluster.objects.create(name=name, institute=institute, head=member)

                member.cluster = cluster

                cluster_domains = self.cluster_domain_formset.save()
                cluster.domains = cluster_domains

                members_emails = []
                for form in self.cluster_member_formset.forms:
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
        else:
            member.cluster = self.cluster

    def is_valid_forms(self):
        if self.http_request.method == 'POST':
            if self.cluster:
                if self.register_form.is_valid() and self.resume_formset.is_valid() \
                    and self.publication_formset.is_valid() and self.invention_formset.is_valid() \
                    and self.executive_research_formset.is_valid() and self.language_skill_formset.is_valid() and \
                        self.software_skill_formset.is_valid():
                    return True
            else:
                if self.cluster_form.is_valid() and self.register_form.is_valid() \
                    and self.cluster_member_formset.is_valid() and self.cluster_domain_formset.is_valid() \
                    and self.resume_formset.is_valid() and self.publication_formset.is_valid() \
                    and self.invention_formset.is_valid() and self.executive_research_formset.is_valid() and \
                        self.language_skill_formset.is_valid() and self.software_skill_formset.is_valid():
                    return True

        return False

    @transaction.commit_on_success
    def save_forms(self):
        first_name = self.register_form.cleaned_data.get('first_name')
        last_name = self.register_form.cleaned_data.get('last_name')
        username = self.register_form.cleaned_data.get('username')
        email = self.register_form.cleaned_data.get('email')

        user = User.objects.create(first_name=first_name, last_name=last_name, username=username, email=email, )
        member = self.register_form.save(commit=False)
        member.user = user

        self.__save_cluster(member)
        member.save()

        resumes = self.resume_formset.save(commit=False)
        for resume in resumes:
            resume.cluster_member = member
            resume.save()

        publications = self.publication_formset.save(commit=False)
        for publication in publications:
            publication.cluster_member = member
            publication.save()

        inventions = self.invention_formset.save(commit=False)
        for invention in inventions:
            invention.cluster_member = member
            invention.save()

        executive_researches = self.executive_research_formset.save(commit=False)
        for executive_research in executive_researches:
            executive_research.cluster_member = member
            executive_research.save()

        language_skills = self.language_skill_formset.save(commit=False)
        for language_skill in language_skills:
            language_skill.cluster_member = member
            language_skill.save()

        software_skills = self.software_skill_formset.save(commit=False)
        for software_skill in software_skills:
            software_skill.cluster_member = member
            software_skill.save()

    def get_context(self):
        c = {
            'cluster_form': self.cluster_form,
            'register_form': self.register_form,
            'cluster_member_formset': self.cluster_member_formset,
            'cluster_domain_formset': self.cluster_domain_formset,
            'resume_formset': self.resume_formset,
            'publication_formset': self.publication_formset,
            'invention_formset': self.invention_formset,
            'executive_research_formset': self.executive_research_formset,
            'language_skill_formset': self.language_skill_formset,
            'software_skill_formset': self.software_skill_formset,
            'cluster': self.cluster,
        }
        return c
