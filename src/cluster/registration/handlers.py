# -*- coding:utf-8 -*-
from django.contrib.auth.models import User
from django.db import transaction
from cluster.account.account.models import Cluster, Member
from cluster.account.personal_info.models import EducationalResume, SoftwareSkill, LanguageSkill, \
    ExecutiveResearchProject, Invention, Publication
from cluster.project.models import Domain
from cluster.registration.forms import ClusterForm, RegisterForm, ClusterMemberForm, ClusterDomainForm, ResumeForm, \
    PublicationForm, InventionForm, ExecutiveResearchProjectForm, LanguageSkillForm, SoftwareSkillForm
from cluster.utils.messages import MessageServices

__author__ = 'M.Y'


class ClusterHandler(object):
    def __init__(self, http_request, cluster_id=None):
        self.http_request = http_request
        self.http_method = self.http_request.method
        self.cluster_id = cluster_id
        self.cluster = cluster_id
        if self.cluster_id:
            self.cluster = Cluster.objects.get(id=cluster_id)
        try:
            self.member = self.http_request.user.member
        except Member.DoesNotExist:
            self.member = None

    def initial_forms(self, member=None, check_post=True):
        self.__init_cluster_form(check_post)
        if self.http_request.method == 'POST' and self.http_request.POST.get('register-submit') and check_post:
            self.register_form = RegisterForm(prefix='register', data=self.http_request.POST, instance=member)
            self.resume_formset = ResumeForm(prefix='resume', data=self.http_request.POST,
                                             queryset=EducationalResume.objects.filter(cluster_member=member))
            self.publication_formset = PublicationForm(prefix='publication', data=self.http_request.POST,
                                                       queryset=Publication.objects.filter(cluster_member=member))
            self.invention_formset = InventionForm(prefix='invention', data=self.http_request.POST,
                                                   queryset=Invention.objects.filter(cluster_member=member))
            self.executive_research_formset = ExecutiveResearchProjectForm(prefix='executive_research',
                                                                           data=self.http_request.POST,
                                                                           queryset=ExecutiveResearchProject.objects.filter(
                                                                               cluster_member=member))
            self.language_skill_formset = LanguageSkillForm(prefix='language_skill', data=self.http_request.POST,
                                                            queryset=LanguageSkill.objects.filter(
                                                                cluster_member=member))
            self.software_skill_formset = SoftwareSkillForm(prefix='software_skill', data=self.http_request.POST,
                                                            queryset=SoftwareSkill.objects.filter(
                                                                cluster_member=member))
        else:
            self.register_form = RegisterForm(prefix='register', instance=member)
            self.resume_formset = ResumeForm(prefix='resume',
                                             queryset=EducationalResume.objects.filter(cluster_member=member))
            self.publication_formset = PublicationForm(prefix='publication',
                                                       queryset=Publication.objects.filter(cluster_member=member))
            self.invention_formset = InventionForm(prefix='invention',
                                                   queryset=Invention.objects.filter(cluster_member=member))
            self.executive_research_formset = ExecutiveResearchProjectForm(prefix='executive_research',
                                                                           queryset=ExecutiveResearchProject.objects.filter(
                                                                               cluster_member=member))
            self.language_skill_formset = LanguageSkillForm(prefix='language_skill',
                                                            queryset=LanguageSkill.objects.filter(
                                                                cluster_member=member))
            self.software_skill_formset = SoftwareSkillForm(prefix='software_skill',
                                                            queryset=SoftwareSkill.objects.filter(
                                                                cluster_member=member))

    def __init_cluster_form(self, check_post):
        self.cluster_member_formset = None
        if self.http_method == 'POST' and self.http_request.POST.get('register-submit') and check_post:
            self.cluster_form = ClusterForm(prefix='cluster', data=self.http_request.POST)
            if not self.cluster:
                self.cluster_member_formset = ClusterMemberForm(prefix='cluster_member', data=self.http_request.POST)
                ClusterDomainForm.extra = 1
                self.cluster_domain_formset = ClusterDomainForm(prefix='cluster_domain', data=self.http_request.POST, )
        else:
            self.cluster_form = ClusterForm(prefix='cluster')
            if not self.cluster:
                self.cluster_member_formset = ClusterMemberForm(prefix='cluster_member')
                ClusterDomainForm.extra = 1
                self.cluster_domain_formset = ClusterDomainForm(prefix='cluster_domain', )

        if self.cluster:
            is_head = self.cluster.head == self.member
            self.cluster_form.fields['is_cluster'].initial = True
            self.cluster_form.fields['institute'].initial = self.cluster.institute
            self.cluster_form.fields['name'].initial = self.cluster.name

            domains = self.cluster.domains.all()
            domains_count = domains.count()
            ClusterDomainForm.extra = domains_count
            if is_head and self.http_method == 'POST' and self.http_request.POST.get('register-submit'):
                self.cluster_domain_formset = ClusterDomainForm(prefix='cluster_domain', data=self.http_request.POST)
            else:
                self.cluster_domain_formset = ClusterDomainForm(prefix='cluster_domain', )
            for i in range(domains_count):
                domain = domains[i]
                self.cluster_domain_formset.forms[i].init_by_domain(domain, is_head)

            member_users = self.cluster.users.all()
            users_count = member_users.count()
            ClusterMemberForm.extra = users_count
            if is_head and self.http_method == 'POST' and self.http_request.POST.get('register-submit'):
                self.cluster_member_formset = ClusterMemberForm(prefix='cluster_member', data=self.http_request.POST)
            else:
                self.cluster_member_formset = ClusterMemberForm(prefix='cluster_member')
            for i in range(users_count):
                user = member_users[i]
                self.cluster_member_formset.forms[i].init_by_member(user, is_head)

            if not is_head:
                self.cluster_domain_formset.readonly = True
                self.cluster_member_formset.readonly = True
                self.cluster_form.fields['name'].widget.attrs.update({'readonly': 'readonly'})
                self.cluster_form.fields['institute'].widget.attrs.update({'readonly': 'readonly'})

    def __save_cluster(self, member):
        if not self.cluster:
            is_cluster = self.cluster_form.cleaned_data.get('is_cluster')
            if is_cluster == 'True':
                name = self.cluster_form.cleaned_data.get('name')
                institute = self.cluster_form.cleaned_data.get('institute')
                cluster = Cluster.objects.create(name=name, institute=institute, head=member)

                member.cluster = cluster

                cluster_domains = []
                for form in self.cluster_domain_formset.forms:
                    domain_choice = form.cleaned_data.get('domain_choice')
                    new_domain_name = form.cleaned_data.get('new_domain_name')
                    if not domain_choice and new_domain_name:
                        domain_choice = Domain.objects.create(name=new_domain_name)
                    if domain_choice:
                        cluster_domains.append(domain_choice)
                        # cluster_domains = self.cluster_domain_formset.save()
                cluster.domains = cluster_domains

                users = []
                for form in self.cluster_member_formset.forms:
                    if form.is_valid():
                        first_name = form.cleaned_data.get('first_name')
                        last_name = form.cleaned_data.get('last_name')
                        email = form.cleaned_data.get('email')
                        password = User.objects.make_random_password()
                        user = User.objects.create(first_name=first_name, last_name=last_name, username=email,
                                                   email=email)
                        user.set_password(password)
                        user.save()
                        users.append(user)
                        message = MessageServices.get_registration_message(cluster, user, email, password)
                        MessageServices.send_message(subject=u"ثبت نام خوشه %s" % cluster.name,
                                                     message=message,
                                                     user=user, cluster=cluster)
                users.append(member.user)

                cluster.users = users
        else:
            member.cluster = self.cluster
            #TODO : SAVE MEMBER CHANGES
            if self.cluster.head == self.member:
                name = self.cluster_form.cleaned_data.get('name')
                institute = self.cluster_form.cleaned_data.get('institute')
                self.cluster.name = name
                self.cluster.institute = institute

                self.cluster.domains.filter(confirmed=False).delete()
                cluster_domains = []
                for form in self.cluster_domain_formset.forms:
                    if form not in self.cluster_domain_formset.deleted_forms:
                        domain_choice = form.cleaned_data.get('domain_choice') or form.fields['domain_choice'].initial
                        new_domain_name = form.cleaned_data.get('new_domain_name') or form.fields['new_domain_name'].initial
                        if not domain_choice and new_domain_name:
                            domain_choice = Domain.objects.create(name=new_domain_name)
                        if domain_choice:
                            cluster_domains.append(domain_choice)
                self.cluster.domains = cluster_domains
                self.cluster.save()

    def is_valid_forms(self):
        validate = False
        if self.http_request.method == 'POST' and self.http_request.POST.get('register-submit'):
            if self.cluster:
                if self.register_form.is_valid() and self.resume_formset.is_valid() \
                    and self.publication_formset.is_valid() and self.invention_formset.is_valid() \
                    and self.executive_research_formset.is_valid() and self.language_skill_formset.is_valid() and \
                        self.software_skill_formset.is_valid():
                    validate = True
                if self.cluster.head == self.member:
                    if self.cluster_form.is_valid() and self.cluster_domain_formset.is_valid() and \
                            self.cluster_member_formset.is_valid():
                        validate = True
                    else:
                        validate = False
            else:
                if self.cluster_form.is_valid() and self.register_form.is_valid() \
                    and self.cluster_member_formset.is_valid() \
                    and self.resume_formset.is_valid() and self.publication_formset.is_valid() \
                    and self.invention_formset.is_valid() and self.executive_research_formset.is_valid() and \
                        self.language_skill_formset.is_valid() and self.software_skill_formset.is_valid():
                    validate = True
                else:
                    validate = False
                if self.cluster_form.is_valid() and self.cluster_form.cleaned_data.get('is_cluster') == 'True':
                    if self.cluster_domain_formset.is_valid():
                        domains = []
                        for form in self.cluster_domain_formset.forms:
                            domain = form.cleaned_data.get('domain_choice')
                            if domain:
                                if domain in domains:
                                    form._errors['domain_choice'] = form.error_class(
                                        [u"حوزه انتخاب شده تکراری است."])
                                    validate = False
                                else:
                                    domains.append(form.cleaned_data.get('domain_choice'))
                    else:
                        validate = False
        return validate

    @transaction.commit_on_success
    def save_forms(self):
        member = self.register_form.save(commit=False,
                                         user=self.http_request.user if not self.http_request.user.is_anonymous() else None)

        member.save()
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

    def has_permission(self):
        if self.cluster:
            try:
                self.cluster.users.get(id=self.http_request.user.id)
                try:
                    if self.member and self.member.cluster == self.cluster:
                        return u"شما قبلا در این خوشه ثبت نام کردید."
                except Member.DoesNotExist:
                    pass
            except User.DoesNotExist:
                return u"شما جزو اعضای این خوشه نیستید."
        return ''
