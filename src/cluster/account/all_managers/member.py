# -*- coding: utf-8 -*-
from django import forms
from cluster.account.account.models import Member, Cluster
from cluster.account.actions import EditMemberAction, SendMemberMessage, ShowMemberAction
from cluster.utils.forms import ClusterBaseModelForm, ClusterFilterModelForm
from cluster.utils.manager.action import ShowAction, DeleteAction, ConfirmAction
from cluster.utils.manager.main import ObjectsManager, ManagerColumn
from cluster.utils.messages import MessageServices
from cluster.utils.permissions import PermissionController

__author__ = 'M.Y'


class MemberForm(ClusterFilterModelForm):
    class Meta:
        model = Member
        fields = ('cluster', 'national_code', 'military_status', 'foundation_of_elites')

    def __init__(self, *args, **kwargs):
        super(MemberForm, self).__init__(*args, **kwargs)
        self.fields['first_name'] = forms.CharField(label=u"نام", required=False)
        self.fields['last_name'] = forms.CharField(label=u"نام خانوادگی", required=False)
        self.fields['cluster'] = forms.ModelMultipleChoiceField(queryset=Cluster.objects.filter(), label=u"خوشه")
        self.fields['foundation_of_elites'] = forms.NullBooleanField(required=False, label=u"عضویت در بنیاد ملی نخبگان")
        self.fields['foundation_of_elites'].widget.choices = ((u'1', u"--- همه ---"),
                                                              (u'2', u"بله"),
                                                              (u'3', u"خیر"))


class MemberActionForm(ClusterBaseModelForm):
    class Meta:
        model = Member
        exclude = ('is_confirmed', 'user')

    def __init__(self, *args, **kwargs):
        super(MemberActionForm, self).__init__(*args, **kwargs)
        self.fields['national_code'].required = True
        self.fields['birth_date'].required = True
        self.fields['residence_city'].required = True
        self.fields['mobile'].required = True
        self.fields['address'].required = True
        self.fields['domain'].required = True
        self.fields['gender'].required = True
        self.fields['full_name'] = forms.CharField(initial=unicode(self.instance.user), label=u"نام و نام خانوادگی",
                                                   required=False)
        self.fields.keyOrder.remove('full_name')
        self.fields.keyOrder.insert(0, 'full_name')


class MemberManager(ObjectsManager):
    manager_name = u"members"
    manager_verbose_name = u"مدیریت  افراد"
    filter_form = MemberForm
    auto_width = False
    filter_handlers = (
        ('first_name', 'str', 'user__first_name'),
        ('last_name', 'str', 'user__last_name'),
        ('cluster', 'm2m'),
        ('national_code', 'this'),
        ('military_status', 'this'),
        ('foundation_of_elites', 'null_bool'),
    )
    actions = [ShowMemberAction(), EditMemberAction(), SendMemberMessage()]

    def get_all_data(self):
        return Member.objects.filter()

    def get_columns(self):
        columns = [
            ManagerColumn('full_name', u"نام و نام خانوادگی", '200', True),
            ManagerColumn('cluster', u"خوشه", '150', True, True),
            ManagerColumn('gender', u"جنسیت", '40'),
            ManagerColumn('national_code', u"کد ملی", '80'),
            ManagerColumn('birth_date', u"تاریخ تولد", '80'),
            ManagerColumn('residence_city', u"شهر محل اقامت", '80'),
            ManagerColumn('mobile', u"تلفن همراه", '70', True, True),
            ManagerColumn('military_status', u"وضعیت نظام وظیفه", '80'),
            ManagerColumn('foundation_of_elites', u"عضویت در بنیاد ملی نخبگان", '80'),
            ManagerColumn('created_on', u"تاریخ ثبت نام", '80'),
            ManagerColumn('is_confirmed', u"تایید شده", '60'),
            ManagerColumn('last_uni', u"آخرین محل تحصیل", '80', True),
            ManagerColumn('last_end_year', u"سال فارغ التحصیلی", '80', True),
            ManagerColumn('last_field', u"رشته تحصیلی", '80', True),
            ManagerColumn('last_orientation', u"گرایش", '80', True),
        ]
        return columns

    def get_excel_columns(self):
        columns = [
            ManagerColumn('first_name', u"نام", '10', True),
            ManagerColumn('last_name', u"نام خانوادگی", '10', True),
            ManagerColumn('username', u"نام کاربری", '7', True),
            ManagerColumn('email', u"پست الکترونیک", '10', True),
            ManagerColumn('last_login', u"تاریخ آخرین ورود", '7', True),
            ManagerColumn('cluster', u"خوشه", '10', True, True),
            ManagerColumn('uni', u"دانشگاه", '10', True),
            ManagerColumn('gender', u"جنسیت", '5'),
            ManagerColumn('national_code', u"کد ملی", '10'),
            ManagerColumn('birth_date', u"تاریخ تولد", '10'),
            ManagerColumn('residence_city', u"شهر محل اقامت", '10'),
            ManagerColumn('telephone', u"تلفن ثابت", '10'),
            ManagerColumn('mobile', u"تلفن همراه", '10', True, True),
            #ManagerColumn('essential_telephone', u"تلفن ضروری", '10'),
            ManagerColumn('address', u"آدرس", '10'),
            ManagerColumn('employment_status', u"وضعیت شغلی", '10'),
            ManagerColumn('organization', u"محل کار", '10'),
            ManagerColumn('military_status', u"وضعیت نظام وظیفه", '15'),
            ManagerColumn('military_place', u"محل خدمت", '10'),
            ManagerColumn('exemption_type', u"نوع معافیت", '10'),
            ManagerColumn('foundation_of_elites', u"عضویت در بنیاد ملی نخبگان", '10'),
            ManagerColumn('arbiter_interest', u"آیا تمایل به داوری نیز دارید؟", '10'),
            ManagerColumn('created_on', u"تاریخ ثبت نام", '10'),
            ManagerColumn('is_confirmed', u"تایید شده", '10'),
            ManagerColumn('last_uni', u"آخرین محل تحصیل", '10', True),
            ManagerColumn('last_end_year', u"سال فارغ التحصیلی", '10', True),
            ManagerColumn('last_field', u"رشته تحصیلی", '10', True),
            ManagerColumn('last_orientation', u"گرایش", '10', True),
        ]
        return columns

    def get_full_name(self, data):
        return unicode(data.user)

    def get_first_name(self, data):
        return unicode(data.user.first_name)

    def get_last_name(self, data):
        return unicode(data.user.last_name)

    def get_username(self, data):
        return unicode(data.user.username)

    def get_email(self, data):
        return unicode(data.user.email)

    def get_last_login(self, data):
        return data.user.last_login

    def can_view(self):
        if PermissionController.is_admin(self.http_request.user):
            return True
        return False

    def get_cluster(self, data):
        if data.cluster:
            link = u"/clusters/actions/?t=action&n=edit_cluster&i=%s" % data.cluster.id
            return u"""<a onClick="MyWindow=window.open('%s','خوشه/فرد',width=800,height=600); return false;"href='#' class="jqgrid-a">%s</a>""" % (
                link, unicode(data.cluster))
        return u"""بدون خوشه"""

    def get_uni(self, data):
        if data.cluster:
            return data.cluster.institute
        return None

    def get_mobile(self, data):
        if data.mobile:
            return "<span style='direction:ltr;float: left;'>+%s</span>" % data.mobile.replace('-', '')

    def get_last_uni(self, data):
        resumes = data.educational_resumes.all().order_by('-end_year')
        if resumes:
            return resumes[0].institution

    def get_last_end_year(self, data):
        resumes = data.educational_resumes.all().order_by('-end_year')
        if resumes:
            return resumes[0].end_year

    def get_last_field(self, data):
        resumes = data.educational_resumes.all().order_by('-end_year')
        if resumes:
            return resumes[0].field

    def get_last_orientation(self, data):
        resumes = data.educational_resumes.all().order_by('-end_year')
        if resumes:
            return resumes[0].orientation


class NoClusterMemberActionForm(ClusterFilterModelForm):
    class Meta:
        model = Member
        fields = ('national_code', 'military_status', 'foundation_of_elites')

    def __init__(self, *args, **kwargs):
        super(NoClusterMemberActionForm, self).__init__(*args, **kwargs)
        self.fields['first_name'] = forms.CharField(label=u"نام", required=False)
        self.fields['last_name'] = forms.CharField(label=u"نام خانوادگی", required=False)
        self.fields['foundation_of_elites'] = forms.NullBooleanField(required=False, label=u"عضویت در بنیاد ملی نخبگان")
        self.fields['foundation_of_elites'].widget.choices = ((u'1', u"--- همه ---"),
                                                              (u'2', u"بله"),
                                                              (u'3', u"خیر"))


def member_confirm_change(instance, confirm):
    if confirm is True:
        message_body = u"عضویت شما تایید شد.\n هم اکنون شما میتوانید در سامانه فعالیت داشته باشید."
        message = MessageServices.get_title_body_message(u"تایید عضویت", message_body)
    elif confirm is False:
        if instance.gender == 1:
            message_body = u"آقای "
        else:
            message_body = u"خانم "
        message_body += u"%s ضمن قدردانی از بذل توجه شما به این موسسه و ثبت نام در سامانه، متاسفانه عضویت شما در سامانه مورد موافقت موسسه قرار نگرفته است.  با آرزوی موفقیت و سلامتی برای شما دوست عزیز." % unicode(
            instance)
        message = MessageServices.get_title_body_message(u"رد عضویت", message_body)
    else:
        message_body = u"وضعیت عضویت شما به نامشخص تغییر یافت."
        message = MessageServices.get_title_body_message(u"تغییر وضعیت عضویت", message_body)
    MessageServices.send_message(u"تغییر وضعیت عضویت", message, instance.user)
    #SMSService.send_sms(message_body, [instance.mobile])
    #if confirm is False:
    #    instance.delete()


class NoClusterMemberManager(MemberManager):
    manager_name = u"no_cluster_members"
    manager_verbose_name = u"مدیریت  افراد بدون خوشه"
    filter_form = NoClusterMemberActionForm

    actions = [ShowAction(MemberActionForm), DeleteAction(),
               ConfirmAction('is_confirmed', on_change_event=member_confirm_change)]

    def get_all_data(self):
        return Member.objects.filter(cluster__isnull=True)

    def get_full_name(self,data):
        link = u"/members/actions/?t=action&n=edit_member&i=%s" % data.id
        return u"""<a onClick="MyWindow=window.open('%s','خوشه/فرد',width=800,height=600); return false;"href='#' class="jqgrid-a">%s</a>""" % (
            link, unicode(data.user))

    def get_columns(self):
        columns = [
            ManagerColumn('full_name', u"نام و نام خانوادگی", '200', True,True),
            ManagerColumn('cluster', u"خوشه", '150', True, True),
            ManagerColumn('gender', u"جنسیت", '40'),
            ManagerColumn('national_code', u"کد ملی", '80'),
            ManagerColumn('birth_date', u"تاریخ تولد", '80'),
            ManagerColumn('residence_city', u"شهر محل اقامت", '80'),
            ManagerColumn('mobile', u"تلفن همراه", '70', True, True),
            ManagerColumn('military_status', u"وضعیت نظام وظیفه", '80'),
            ManagerColumn('foundation_of_elites', u"عضویت در بنیاد ملی نخبگان", '80'),
            ManagerColumn('created_on', u"تاریخ ثبت نام", '80'),
            ManagerColumn('is_confirmed', u"تایید شده", '60'),
            ManagerColumn('last_uni', u"آخرین محل تحصیل", '80', True),
            ManagerColumn('last_end_year', u"سال فارغ التحصیلی", '80', True),
            ManagerColumn('last_field', u"رشته تحصیلی", '80', True),
            ManagerColumn('last_orientation', u"گرایش", '80', True),
        ]
        return columns

    filter_handlers = (
        ('first_name', 'str', 'user__first_name'),
        ('last_name', 'str', 'user__last_name'),
        ('national_code', 'this'),
        ('military_status', 'this'),
        ('foundation_of_elites', 'null_bool'),
    )

