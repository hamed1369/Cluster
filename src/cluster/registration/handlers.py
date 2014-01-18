# -*- coding:utf-8 -*-
from django.contrib.auth.models import User
from django.db import transaction
from cluster.account.account.models import Cluster, Member, Domain
from cluster.account.personal_info.models import EducationalResume, SoftwareSkill, LanguageSkill, \
    ExecutiveResearchProject, Invention, Publication
from cluster.registration.forms import ClusterForm, RegisterForm, ClusterMemberForm, ClusterDomainForm, \
    PublicationForm, InventionForm, ExecutiveResearchProjectForm, LanguageSkillForm, SoftwareSkillForm, \
    get_resume_formset
from cluster.utils.messages import MessageServices

__author__ = 'M.Y'


class ClusterHandler(object):
    def __init__(self, http_request, cluster_id=None, has_cluster=True, has_register=True, member=None):
        self.http_request = http_request
        self.http_method = self.http_request.method
        self.cluster_id = cluster_id
        self.cluster = cluster_id
        self.has_cluster = has_cluster
        self.has_register = has_register
        if self.cluster_id:
            self.cluster = Cluster.objects.get(id=cluster_id)
        if member:
            self.member = member
        else:
            try:
                self.member = self.http_request.user.member
            except (Member.DoesNotExist, AttributeError):
                self.member = None
            except AttributeError:
                self.member = None
        self.cluster_form = None
        self.cluster_domain_formset = None
        self.cluster_member_formset = None
        self.register_form = None
        self.resume_formset = None
        self.publication_formset = None
        self.invention_formset = None
        self.executive_research_formset = None
        self.language_skill_formset = None
        self.software_skill_formset = None

    def initial_forms(self, member=None, check_post=True):
        if self.has_cluster:
            self.__init_cluster_form(check_post)
        if self.has_register:
            self.__init_register_form(member or self.member, check_post)

    def __init_register_form(self, member, check_post):
        ResumeForm = get_resume_formset(member)
        if self.http_request.method == 'POST' and self.http_request.POST.get('register-submit') and check_post:
            self.register_form = RegisterForm(prefix='register', data=self.http_request.POST,
                                              files=self.http_request.FILES, instance=member,
                                              has_cluster=self.has_cluster, user=self.http_request.user)
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
            # self.language_skill_formset = LanguageSkillForm(prefix='language_skill', data=self.http_request.POST,
            #                                                 queryset=LanguageSkill.objects.filter(
            #                                                     cluster_member=member))
            # self.software_skill_formset = SoftwareSkillForm(prefix='software_skill', data=self.http_request.POST,
            #                                                 queryset=SoftwareSkill.objects.filter(
            #                                                     cluster_member=member))
        else:
            self.register_form = RegisterForm(prefix='register', instance=member, has_cluster=self.has_cluster,
                                              user=self.http_request.user)
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
        if self.resume_formset:
            self.resume_formset.forms[0].empty_permitted = False

    def __init_cluster_form(self, check_post):
        self.cluster_member_formset = None
        if self.http_method == 'POST' and self.http_request.POST.get('register-submit') and check_post:
            self.cluster_form = ClusterForm(prefix='cluster', data=self.http_request.POST,
                                            http_request=self.http_request)
            if not self.cluster:
                self.cluster_member_formset = ClusterMemberForm(prefix='cluster_member', data=self.http_request.POST)
                ClusterDomainForm.extra = 1
                self.cluster_domain_formset = ClusterDomainForm(prefix='cluster_domain', data=self.http_request.POST, )
        else:
            self.cluster_form = ClusterForm(prefix='cluster', http_request=self.http_request)
            if not self.cluster:
                self.cluster_member_formset = ClusterMemberForm(prefix='cluster_member')
                ClusterDomainForm.extra = 1
                self.cluster_domain_formset = ClusterDomainForm(prefix='cluster_domain', )

        if self.cluster:
            self.cluster_form.fields['is_cluster'].initial = True
            self.cluster_form.fields['is_cluster'].required = False
            is_head = self.cluster.head == self.member
            self.cluster_form.fields['is_cluster'].initial = True
            self.cluster_form.fields['institute'].initial = self.cluster.institute
            self.cluster_form.fields['name'].initial = self.cluster.name

            domains = self.cluster.domains.all()
            domains_count = domains.count()
            if domains:
                ClusterDomainForm.extra = domains_count
            if is_head and self.http_method == 'POST' and self.http_request.POST.get('register-submit') and check_post:
                self.cluster_domain_formset = ClusterDomainForm(prefix='cluster_domain', data=self.http_request.POST)
            else:
                self.cluster_domain_formset = ClusterDomainForm(prefix='cluster_domain', )
            for i in range(domains_count):
                domain = domains[i]
                self.cluster_domain_formset.forms[i].init_by_domain(domain, is_head)

            members = self.cluster.members.exclude(user__id=self.http_request.user.id)
            users_count = members.count()
            if members:
                ClusterMemberForm.extra = users_count
            if is_head and self.http_method == 'POST' and self.http_request.POST.get('register-submit') and check_post:
                self.cluster_member_formset = ClusterMemberForm(prefix='cluster_member', data=self.http_request.POST)
            else:
                self.cluster_member_formset = ClusterMemberForm(prefix='cluster_member')
            for i in range(users_count):
                member = members[i]
                self.cluster_member_formset.forms[i].init_by_member(member, is_head)

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

                members = []
                for form in self.cluster_member_formset.forms:
                    if form.is_valid():
                        first_name = form.cleaned_data.get('first_name')
                        last_name = form.cleaned_data.get('last_name')
                        email = form.cleaned_data.get('email')
                        domain = form.cleaned_data.get('domain')
                        password = User.objects.make_random_password()
                        user = User.objects.create(first_name=first_name, last_name=last_name, username=email,
                                                   email=email)
                        user.set_password(password)
                        user.save()
                        try:
                            domain = cluster.domains.get(id=int(domain))
                        except (Domain.DoesNotExist, ValueError):
                            try:
                                domain = cluster.domains.get(name=domain)
                            except Domain.DoesNotExist:
                                domain = None
                        temp_member = Member.objects.create(user=user, domain=domain)
                        members.append(temp_member)
                        message = MessageServices.get_registration_message(cluster, user, email, password)
                        MessageServices.send_message(subject=u"ثبت نام خوشه %s" % cluster.name,
                                                     message=message,
                                                     user=user, cluster=cluster)
                members.append(member)

                cluster.members = members
        else:
            member.cluster = self.cluster
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
                        new_domain_name = form.cleaned_data.get('new_domain_name') or form.fields[
                            'new_domain_name'].initial
                        if not domain_choice and new_domain_name:
                            domain_choice = Domain.objects.create(name=new_domain_name)
                        if domain_choice:
                            cluster_domains.append(domain_choice)
                self.cluster.domains = cluster_domains

                members = []
                for form in self.cluster_member_formset.forms:
                    if form not in self.cluster_member_formset.deleted_forms:
                        if form.is_valid():
                            first_name = form.cleaned_data.get('first_name')
                            last_name = form.cleaned_data.get('last_name')
                            email = form.cleaned_data.get('email')
                            domain = form.cleaned_data.get('domain')
                            try:
                                domain = self.cluster.domains.get(id=int(domain))
                            except (Domain.DoesNotExist, ValueError, TypeError):
                                try:
                                    domain = self.cluster.domains.get(name=domain)
                                except Domain.DoesNotExist:
                                    domain = None
                            if 'member_id' in form.fields:
                                member_id = form.fields['member_id'].initial
                            else:
                                member_id = None
                            if member_id:
                                try:
                                    member_temp = self.cluster.members.get(id=member_id)
                                    if first_name:
                                        member_temp.user.first_name = first_name
                                    if last_name:
                                        member_temp.user.last_name = last_name
                                    if email:
                                        member_temp.user.email = email
                                    if domain:
                                        member_temp.domain = domain
                                    member_temp.user.save()
                                    member_temp.save()
                                    members.append(member_temp)
                                except Member.DoesNotExist:
                                    pass
                            else:
                                if email:
                                    password = User.objects.make_random_password()
                                    user = User.objects.create(first_name=first_name, last_name=last_name,
                                                               username=email,
                                                               email=email)
                                    user.set_password(password)
                                    user.save()
                                    member_temp = Member.objects.create(user=user, domain=domain)
                                    members.append(member_temp)
                                    message = MessageServices.get_registration_message(self.cluster, user, email,
                                                                                       password)
                                    MessageServices.send_message(subject=u"ثبت نام خوشه %s" % self.cluster.name,
                                                                 message=message,
                                                                 user=user, cluster=self.cluster)

                for form in self.cluster_member_formset.deleted_forms:
                    if form.is_valid():
                        member_id = form.cleaned_data.get('member_id')
                        if member_id:
                            try:
                                member_temp = self.cluster.members.get(id=member_id)
                                message = MessageServices.get_delete_member_message(self.cluster, member_temp.user)
                                MessageServices.send_message(subject=u"حذف از خوشه %s" % self.cluster.name,
                                                             message=message,
                                                             user=member_temp.user, cluster=self.cluster)
                                user = member_temp.user
                                member_temp.delete()
                                user.delete()
                            except Member.DoesNotExist:
                                pass
                members.append(member)

                self.cluster.members = members

                self.cluster.save()

    def is_valid_forms(self):
        validate = False
        if self.http_request.method == 'POST' and self.http_request.POST.get('register-submit'):
            if self.has_cluster and self.has_register:
                if self.cluster:
                    if self.register_form.is_valid() and self.resume_formset.is_valid() \
                        and self.publication_formset.is_valid() and self.invention_formset.is_valid() \
                        and self.executive_research_formset.is_valid():
                        validate = True
                    else:
                        validate = False
                    if self.cluster.head == self.member:
                        if self.cluster_form.is_valid() and self.cluster_domain_formset.is_valid() and \
                                self.cluster_member_formset.is_valid():
                            pass
                        else:
                            validate = False
                else:
                    if self.cluster_form.is_valid() and self.register_form.is_valid() \
                        and self.cluster_member_formset.is_valid() \
                        and self.resume_formset.is_valid() and self.publication_formset.is_valid() \
                        and self.invention_formset.is_valid() and self.executive_research_formset.is_valid():
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
            else:
                if self.has_register:
                    if self.register_form.is_valid() and self.resume_formset.is_valid() and self.publication_formset.is_valid() \
                        and self.invention_formset.is_valid() and self.executive_research_formset.is_valid():
                        validate = True
                elif self.has_cluster:
                    if self.cluster_form.is_valid() and self.cluster_domain_formset.is_valid() and \
                            self.cluster_member_formset.is_valid():
                        validate = True

        return validate

    def save_only_cluster(self, member):
        self.__save_cluster(member)

    @transaction.commit_on_success
    def save_forms(self):
        user = None
        if self.has_cluster:
            user = self.http_request.user if not self.http_request.user.is_anonymous() else None

        is_cluster = False
        if self.cluster_form:
            if self.member and self.member.cluster and self.member.cluster.head and self.member.cluster.head != self.member:
                is_cluster = False
            else:
                is_cluster = self.cluster_form.cleaned_data.get('is_cluster')
        else:
            is_cluster = False

        member = self.register_form.save(
            commit=False,
            user=user, is_cluster=is_cluster
        )

        member.save()
        if self.has_cluster:
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

        # language_skills = self.language_skill_formset.save(commit=False)
        # for language_skill in language_skills:
        #     language_skill.cluster_member = member
        #     language_skill.save()
        #
        # software_skills = self.software_skill_formset.save(commit=False)
        # for software_skill in software_skills:
        #     software_skill.cluster_member = member
        #     software_skill.save()

        return member

    def get_context(self):
        cluster = self.cluster if self.has_cluster else None
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
            'cluster': cluster,
            'member': self.member
        }
        return c

    def has_permission(self):
        if self.cluster:
            try:
                self.cluster.members.get(user__id=self.http_request.user.id)
                try:
                    if self.member and self.member.cluster == self.cluster and self.member.national_code:
                        return u"شما قبلا در این خوشه ثبت نام کردید."
                except Member.DoesNotExist:
                    pass
            except Member.DoesNotExist:
                return u"شما جزو اعضای این خوشه نیستید."
        return ''

    def set_all_readonly(self):
        if self.cluster_form:
            for field in self.cluster_form.fields:
                self.cluster_form.fields[field].widget.attrs.update({'readonly': 'readonly', 'disabled': 'disabled'})
        if self.register_form:
            for field in self.register_form.fields:
                self.register_form.fields[field].widget.attrs.update({'readonly': 'readonly', 'disabled': 'disabled'})

        if self.cluster_member_formset:
            self.cluster_member_formset.readonly = True
            for form in self.cluster_member_formset.forms:
                for field in form.fields:
                    form.fields[field].widget.attrs.update({'readonly': 'readonly', 'disabled': 'disabled'})
        if self.cluster_domain_formset:
            self.cluster_domain_formset.readonly = True
            for form in self.cluster_domain_formset.forms:
                for field in form.fields:
                    form.fields[field].widget.attrs.update({'readonly': 'readonly', 'disabled': 'disabled'})
        if self.resume_formset:
            self.resume_formset.readonly = True
            for form in self.resume_formset.forms:
                for field in form.fields:
                    form.fields[field].widget.attrs.update({'readonly': 'readonly', 'disabled': 'disabled'})
        if self.publication_formset:
            self.publication_formset.readonly = True
            for form in self.publication_formset.forms:
                for field in form.fields:
                    form.fields[field].widget.attrs.update({'readonly': 'readonly', 'disabled': 'disabled'})
        if self.invention_formset:
            self.invention_formset.readonly = True
            for form in self.invention_formset.forms:
                for field in form.fields:
                    form.fields[field].widget.attrs.update({'readonly': 'readonly', 'disabled': 'disabled'})
        if self.executive_research_formset:
            self.executive_research_formset.readonly = True
            for form in self.executive_research_formset.forms:
                for field in form.fields:
                    form.fields[field].widget.attrs.update({'readonly': 'readonly', 'disabled': 'disabled'})
        if self.language_skill_formset:
            self.language_skill_formset.readonly = True
            for form in self.language_skill_formset.forms:
                for field in form.fields:
                    form.fields[field].widget.attrs.update({'readonly': 'readonly', 'disabled': 'disabled'})
        if self.software_skill_formset:
            self.software_skill_formset.readonly = True
            for form in self.software_skill_formset.forms:
                for field in form.fields:
                    form.fields[field].widget.attrs.update({'readonly': 'readonly', 'disabled': 'disabled'})
