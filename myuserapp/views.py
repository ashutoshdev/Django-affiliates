from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from myuserapp.models import Profile, Page, PaymentSettings, Contact, ContactEmail, Websites, Testimonials, Snippet,\
    BannerCategory, GenerateForm, LeadDetail, GenerateFormOrder, GenerateButton, GenerateQueryForm
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, authenticate
from django.shortcuts import get_object_or_404
import random
from random import choice
from string import ascii_lowercase, digits
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from myuserapp.tokens import account_activation_token
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_text
from django.contrib.auth import logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.contrib.auth.decorators import login_required
from django.conf import settings
import requests
from rest_framework.views import APIView
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.decorators import permission_classes
from rest_framework import permissions
from django.http import JsonResponse
from rest_framework.response import Response
import re


class IndexView(TemplateView):
    template_name = 'live_affiliates/index.html'

    def get_context_data(self):
        context = super(IndexView, self).get_context_data()
        # if self.request.user.is_authenticated:
        #     return HttpResponseRedirect('/sale_report')
        # else:
        context['home_widget'] = Page.objects.filter(pagerole='home_widget')
        context['testimonials'] = Testimonials.objects.all()
        context['home_page_phone'] = Page.objects.filter(pagerole='home_page_phone').first()
        context['home_page_email'] = Page.objects.filter(pagerole='home_page_email').first()
        context['home_page_widget_first'] = Page.objects.filter(pagerole='home_page_widget_first').first()
        context['home_page_widget_second'] = Page.objects.filter(pagerole='home_page_widget_second').first()
        context['home_page_widget_third'] = Page.objects.filter(pagerole='home_page_widget_third').first()
        return context

def generate_random_username(length=16, chars=ascii_lowercase + digits, split=4, delimiter='-'):
    username = ''.join([choice(chars) for i in range(length)])

    if split:
        username = delimiter.join([username[start:start + split] for start in range(0, len(username), split)])

    try:
        User.objects.get(username=username)
        return generate_random_username(length=length, chars=chars, split=split, delimiter=delimiter)
    except User.DoesNotExist:
        return username;


class SignupView(TemplateView):
    template_name = 'live_affiliates/pages/signup.html'

    def get_context_data(self):
        context = super(SignupView, self).get_context_data()
        context['home_page_widget_first'] = Page.objects.filter(pagerole='home_page_widget_first').first()
        context['home_page_widget_second'] = Page.objects.filter(pagerole='home_page_widget_second').first()
        context['home_page_widget_third'] = Page.objects.filter(pagerole='home_page_widget_third').first()
        context['testimonials'] = Testimonials.objects.all()
        context['home_page_phone'] = Page.objects.filter(pagerole='home_page_phone').first()
        context['home_page_email'] = Page.objects.filter(pagerole='home_page_email').first()
        request = self.request
        if request.method != 'POST':
            return context

    def post(self, request, *args, **kwargs):
        response = super(SignupView, self).get(request, *args, **kwargs)
        email = request.POST.get('email')
        user = User.objects.filter(
            email=email
        ).first()
        if not user:
            user = User()
            user.email = email
            password = random.randint(9, 999999999)
            user.set_password(password)
            username = user.username = generate_random_username()
            user.is_active = False
            user.save()
            profile = Profile()
            profile.contact_person = request.POST.get('agent_name')
            profile.company_name_or_payee_name = request.POST.get('company')
            profile.mobile_number = request.POST.get('contact_no')
            profile.country = request.POST.get('country')
            profile.refer_by = request.POST.get('refer_by')
            profile.your_referral_code = generate_random_username()
            profile.user = user
            profile.save()
            return HttpResponseRedirect('/signup_success/'+username)

        elif user.is_active:
            return HttpResponseRedirect('/login')
        else:
            messages.success(request, 'User already exits! Please complete your steps!')
            return HttpResponseRedirect('/signup_success/' + user.username)


class SignupSuccessView(TemplateView):
    # login_url = '/'
    template_name = 'live_affiliates/pages/signup_success.html'

    def get_context_data(self, user, *args, **kwargs):
        context = super(SignupSuccessView, self).get_context_data()
        request = self.request
        if request.method != 'POST':
            return context

    def get(self, request, *args, **kwargs):
        response = super(SignupSuccessView, self).get(request, *args, **kwargs)
        username = kwargs['user']
        check_page = User.objects.filter(
            username=username,
            is_active=1
        ).first()
        if check_page:
            messages.success(request, 'User already exits! Please login!')
            return HttpResponseRedirect('/login')

        return response

    def post(self, request, *args, **kwargs):
        super(SignupSuccessView, self).get(request, *args, **kwargs)
        username = kwargs['user']
        user = User.objects.filter(
            username=username
        ).first()
        # print(user)
        if user:
            password = request.POST.get('p1')
            user.set_password(password)
            user.is_active = False
            user.save()
            profile = Profile.objects.filter(
                user=user
            ).first()
            profile.address = request.POST.get('address1')
            profile.city = request.POST.get('city')
            profile.business_type = request.POST.get('businesstype')
            profile.zip = request.POST.get('pin')
            profile.user = user
            profile.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('live_affiliates/pages/acc_active_email.html', {
                'user': profile.contact_person,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            # activation_link = "{0}/activate/{1}/{2}".format(current_site, uid, token)
            # print(activation_link)
            to_email = user.email
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            messages.success(request, to_email)
            return HttpResponseRedirect('/email_verification')

        else:
            messages.success(request, 'User Does not exits!')
            return HttpResponseRedirect('/signup')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        mail_subject = 'Welcome to Affiliates of Atdoorstep'
        message = render_to_string('live_affiliates/pages/welcome_email.html', {
            'username': user.username,
            'email': user.email,
        })
        to_email = user.email
        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        email.send()
        messages.success(request, to_email)
        login(request, user)
        return redirect('/')
    else:
        return HttpResponse('Activation link is invalid!')


@csrf_exempt
@api_view(['POST'])
@permission_classes([])
@authentication_classes([])
def resend_activate_email(request):
    email = request.data.get('email')
    user = User.objects.filter(email=email).first()
    if user:
        profile = Profile.objects.filter(user=user).first()
        current_site = get_current_site(request)
        mail_subject = 'Activate your account.'
        message = render_to_string('live_affiliates/pages/acc_active_email.html', {
            'user': profile.contact_person,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        to_email = user.email
        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        email.send()
        messages.success(request, to_email)
        return HttpResponseRedirect('/email_verification')
    else:
        return HttpResponseRedirect('/signup')


class EmailVerificationView(TemplateView):
    template_name = 'live_affiliates/pages/email_verification.html'


class LoginView(TemplateView):
    template_name = 'live_affiliates/pages/login.html'

    def get_context_data(self):
        context = super(LoginView, self).get_context_data()
        request = self.request

        if request.method != 'POST':
            return context

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        if '@' in username:
            check_user = User.objects.filter(
                email=username
            ).first()
            if check_user:
                username = check_user.username
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/sale_report')
        else:
            messages.success(request, 'Login failed. Try again.')
            return redirect('/login')


class SalesReportView(LoginRequiredMixin, TemplateView):
    login_url = '/'
    template_name = 'live_affiliates/pages/sale_report.html'

    def get_context_data(self):
        context = super(SalesReportView, self).get_context_data()
        request = self.request
        getdataof = self.request.GET.get('getdataof', "this_month")
        page = self.request.GET.get('page', None)
        source = self.request.GET.get('source', None)
        url = settings.API_WEBSITE_URL + '/affiliate-api/v1/booking/bookingByAffId/'+str(request.user.id)
        if getdataof:
            url = url +'?getdataof='+getdataof
        if source:
            url = url +'&source='+source
        if page:
            url = url +'&page='+page
        response = requests.get(url)
        if "page" in request.get_full_path():
            path = request.get_full_path()[:-7]
        elif "getdataof" not in request.get_full_path():
            path = request.get_full_path()+'?getdataof='+getdataof
        else:
            path = request.get_full_path()
        context['all_booking'] = response.json()
        context['path'] = path
        context['websites'] = Websites.objects.filter(user=request.user)
        return context


class BannersView(LoginRequiredMixin, TemplateView):
    login_url = '/'
    template_name = 'live_affiliates/pages/banners.html'

    def get_context_data(self):
        context = super(BannersView, self).get_context_data()
        context['banner_category'] = BannerCategory.objects.filter(status=True)
        context['my_url'] = settings.MY_WEBSITE_URL
        return context



class PaymentDetailsView(LoginRequiredMixin, TemplateView):
    login_url = '/'
    template_name = 'live_affiliates/pages/payment_details.html'


class WebsitesView(LoginRequiredMixin, TemplateView):
    login_url = '/'
    template_name = 'live_affiliates/pages/websites.html'

    def get_context_data(self):
        context = super(WebsitesView, self).get_context_data()
        request = self.request
        context['user'] = request.user
        context['websites'] = Websites.objects.filter(user=request.user)
        return context

    def post(self, request, *args, **kwargs):
        super(WebsitesView, self).get(request, *args, **kwargs)
        website = Websites()
        website_address = request.POST.get('website')
        url = re.compile(r"https?://(www\.)?")
        website_address = url.sub('', website_address).strip().strip('/')
        website.website_address = website_address
        website.user = request.user
        website.save()
        messages.success(request, 'Website added successfully')
        return HttpResponseRedirect('/websites')


class MyAccountView(LoginRequiredMixin, TemplateView):
    login_url = '/'
    template_name = 'live_affiliates/pages/account.html'

    def get_context_data(self):
        context = super(MyAccountView, self).get_context_data()
        request = self.request
        context['user'] = request.user
        context['profile'] = Profile.objects.filter(user=request.user).first()
        context['payment'] = PaymentSettings.objects.filter(user=request.user).first()
        return context


class GenerateFormView(LoginRequiredMixin, TemplateView):
    login_url = '/'
    template_name = 'live_affiliates/pages/generate_form.html'

    def get_context_data(self):
        context = super(GenerateFormView, self).get_context_data()
        request = self.request
        response = requests.get(settings.API_WEBSITE_URL+'/affiliate-api/v1/categories/parentCategories')
        context['cat'] = response.json()
        response = requests.get(settings.API_WEBSITE_URL + '/affiliate-api/v1/booking/cityList')
        context['cities'] = response.json()
        context['websites'] = Websites.objects.filter(user=request.user)
        context['g_form'] = GenerateForm.objects.filter(user=request.user,isDeleted=False).last()
        return context

    def post(self, request, *args, **kwargs):
        super(GenerateFormView, self).get(request, *args, **kwargs)
        generate_form = GenerateForm()
        generate_form.website = request.POST.get('website')
        generate_form.category = request.POST.getlist('category[]')
        generate_form.locations = request.POST.getlist('locations[]')
        generate_form.title = request.POST.get('title')
        generate_form.name = request.POST.get('name')
        generate_form.width = request.POST.get('width')
        generate_form.height = request.POST.get('height')
        generate_form.border = request.POST.get('border')
        generate_form.title_background = request.POST.get('title_background')
        generate_form.title_text_color = request.POST.get('title_text_color')
        generate_form.body_text_background = request.POST.get('body_text_background')
        generate_form.body_text_color = request.POST.get('body_text_color')
        generate_form.thank_you_url = request.POST.get('thank_you_url')
        generate_form.user = request.user
        generate_form.save()
        messages.success(request, 'Data Updated successfully')
        return HttpResponseRedirect('/generate_form')


class GenerateFormListView(LoginRequiredMixin, TemplateView):
    login_url = '/'
    template_name = 'live_affiliates/pages/generate_form_list.html'

    def get_context_data(self):
        context = super(GenerateFormListView, self).get_context_data()
        request = self.request
        context['g_forms'] = GenerateForm.objects.filter(user=request.user,isDeleted=False)
        return context


    def post(self, request, *args, **kwargs):
        super(GenerateFormListView, self).get(request, *args, **kwargs)
        id  = request.POST.get('id')
        button = GenerateForm.objects.get(pk=id)
        button.isDeleted =True
        button.save()
        messages.success(request, 'Data Deleted successfully')
        return HttpResponseRedirect('/generate_form_list')


class GenerateFormPreviewView(LoginRequiredMixin, TemplateView):
    login_url = '/'
    template_name = 'live_affiliates/pages/generate_form_edit.html'

    def get_context_data(self, wid):
        context = super(GenerateFormPreviewView, self).get_context_data()
        request = self.request
        context['g_forms'] = wid
        return context


class GenerateFormEditView(LoginRequiredMixin, TemplateView):
    login_url = '/'
    template_name = 'live_affiliates/pages/generate_form_view.html'

    def get_context_data(self, wid):
        context = super(GenerateFormEditView, self).get_context_data()
        request = self.request
        try:
            g_form = GenerateForm.objects.get(id=wid)
        except:
            g_form = None
        response = requests.get(settings.API_WEBSITE_URL + '/affiliate-api/v1/categories/parentCategories')
        context['cat'] = response.json()
        response = requests.get(settings.API_WEBSITE_URL + '/affiliate-api/v1/booking/cityList')
        context['cities'] = response.json()
        context['websites'] = Websites.objects.filter(user=request.user)
        context['g_form'] = g_form
        return context

    def post(self, request, *args, **kwargs):
        super(GenerateFormEditView, self).get(request, *args, **kwargs)
        wid = kwargs.get('wid')
        try:
            generate_form = GenerateForm.objects.get(id=wid)
        except:
            generate_form = GenerateForm.objects.get(id=wid)
        if generate_form: 
            generate_form.website = request.POST.get('website')
            generate_form.category = request.POST.getlist('category[]')
            generate_form.locations = request.POST.getlist('locations[]')
            generate_form.title = request.POST.get('title')
            generate_form.name = request.POST.get('name')
            generate_form.width = request.POST.get('width')
            generate_form.height = request.POST.get('height')
            generate_form.border = request.POST.get('border')
            generate_form.title_background = request.POST.get('title_background')
            generate_form.title_text_color = request.POST.get('title_text_color')
            generate_form.body_text_background = request.POST.get('body_text_background')
            generate_form.body_text_color = request.POST.get('body_text_color')
            generate_form.thank_you_url = request.POST.get('thank_you_url')
            generate_form.user = request.user
            generate_form.save()
            messages.success(request, 'Data Updated successfully')
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            messages.success(request, 'Generate Form Not Found')
            return redirect(request.META.get('HTTP_REFERER'))


class GenerateButtonView(LoginRequiredMixin, TemplateView):
    login_url = '/'
    template_name = 'live_affiliates/pages/generate_button.html'

    def get_context_data(self):
        context = super(GenerateButtonView, self).get_context_data()
        request = self.request
        response = requests.get(settings.API_WEBSITE_URL + '/affiliate-api/v1/categories/parentCategories')
        context['cat'] = response.json()
        response = requests.get(settings.API_WEBSITE_URL + '/affiliate-api/v1/booking/cityList')
        context['cities'] = response.json()
        context['websites'] = Websites.objects.filter(user=request.user)
        context['g_form'] = GenerateButton.objects.filter(user=request.user).last()
        return context

    def post(self, request, *args, **kwargs):
        super(GenerateButtonView, self).get(request, *args, **kwargs)
        generate_form = GenerateButton()
        generate_form.website = request.POST.get('website')
        generate_form.category = request.POST.get('category')
        generate_form.locations = request.POST.get('locations')
        generate_form.title = request.POST.get('title')
        generate_form.name = request.POST.get('name')
        generate_form.width = request.POST.get('width')
        generate_form.height = request.POST.get('height')
        generate_form.border = request.POST.get('border')
        generate_form.size = request.POST.get('size')
        generate_form.title_background = request.POST.get('title_background')
        generate_form.title_text_color = request.POST.get('title_text_color')
        generate_form.user = request.user
        generate_form.save()
        messages.success(request, 'Data Updated successfully')
        return HttpResponseRedirect('/generate_button')


class GenerateButtonEditView(LoginRequiredMixin, TemplateView):
    login_url = '/'
    template_name = 'live_affiliates/pages/generate_button_view.html'

    def get_context_data(self, wid):
        context = super(GenerateButtonEditView, self).get_context_data()
        request = self.request
        try:
            g_form = GenerateButton.objects.get(id=wid)
        except:
            g_form = None
        response = requests.get(settings.API_WEBSITE_URL + '/affiliate-api/v1/categories/parentCategories')
        context['cat'] = response.json()
        response = requests.get(settings.API_WEBSITE_URL + '/affiliate-api/v1/booking/cityList')
        context['cities'] = response.json()
        context['websites'] = Websites.objects.filter(user=request.user)
        context['g_form'] = g_form
        return context

    def post(self, request, *args, **kwargs):
        super(GenerateButtonEditView, self).get(request, *args, **kwargs)
        wid = kwargs.get('wid')
        try:
            generate_form = GenerateButton.objects.get(id=wid)
        except:
            generate_form = GenerateButton.objects.get(id=wid)
        if generate_form: 
            generate_form.website = request.POST.get('website')
            generate_form.category = request.POST.get('category')
            generate_form.locations = request.POST.get('locations')
            generate_form.title = request.POST.get('title')
            generate_form.name = request.POST.get('name')
            generate_form.width = request.POST.get('width')
            generate_form.height = request.POST.get('height')
            generate_form.border = request.POST.get('border')
            generate_form.size = request.POST.get('size')
            generate_form.title_background = request.POST.get('title_background')
            generate_form.title_text_color = request.POST.get('title_text_color')
            generate_form.user = request.user
            generate_form.save()
            messages.success(request, 'Data Updated successfully')
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            messages.success(request, 'Generate Form Not Found')
            return redirect(request.META.get('HTTP_REFERER'))


class GenerateButtonListView(LoginRequiredMixin, TemplateView):
    login_url = '/'
    template_name = 'live_affiliates/pages/generate_button_list.html'

    def get_context_data(self):
        context = super(GenerateButtonListView, self).get_context_data()
        request = self.request
        context['g_forms'] = GenerateButton.objects.filter(user=request.user,isDeleted=False)
        return context

    def post(self, request, *args, **kwargs):
        super(GenerateButtonListView, self).get(request, *args, **kwargs)
        id  = request.POST.get('id')
        button = GenerateButton.objects.get(pk=id)
        button.isDeleted =True
        button.save()
        messages.success(request, 'Data Deleted successfully')
        return HttpResponseRedirect('/generate_button_list')


class ReportLeadView(LoginRequiredMixin, TemplateView):
    login_url = '/'
    template_name = 'live_affiliates/pages/report_lead.html'

    def get_context_data(self):
        context = super(ReportLeadView, self).get_context_data()
        request = self.request
        context['websites'] = Websites.objects.filter(user=request.user)
        return context


class MyReferralView(LoginRequiredMixin, TemplateView):
    login_url = '/'
    template_name = 'live_affiliates/pages/myreferral.html'

    def get_context_data(self):
        context = super(MyReferralView, self).get_context_data()
        request = self.request
        profile = Profile.objects.filter(user=request.user).first()
        context['allusrs'] = Profile.objects.filter(refer_by=profile.your_referral_code)
        return context


@csrf_exempt
def logout_view(request):
    logout(request)
    return redirect('/')


@csrf_exempt
def privacy(request):
    context = {}
    page = Page.objects.filter(pagerole='privacy')
    if page.count() != 0:
        context['page'] = page
    return render(request, 'live_affiliates/pages/pages.html', context)


@csrf_exempt
def about(request):
    context = {}
    page = Page.objects.filter(pagerole='about')
    if page.count() != 0:
        context['page'] = page
    return render(request, 'live_affiliates/pages/pages.html', context)


@csrf_exempt
def term_and_condition(request):
    context = {}
    page = Page.objects.filter(pagerole='term_and_condition')
    if page.count() != 0:
        context['page'] = page
    return render(request, 'live_affiliates/pages/pages.html', context)


@csrf_exempt
def step_to_use(request):
    context = {}
    page = Page.objects.filter(pagerole='step_to_use')
    if page.count() != 0:
        context['page'] = page
    return render(request, 'live_affiliates/pages/pages.html', context)


@csrf_exempt
def faq(request):
    context = {}
    page = Page.objects.filter(pagerole='step_to_use')
    if page.count() != 0:
        context['page'] = page
    return render(request, 'live_affiliates/pages/faq.html', context)


@csrf_exempt
def advantages_and_benefits(request):
    context = {}
    page = Page.objects.filter(pagerole='advantages_and_benefits')
    if page.count() != 0:
        context['page'] = page
    return render(request, 'live_affiliates/pages/pages.html', context)


@csrf_exempt
def why_join(request):
    context = {}
    page = Page.objects.filter(pagerole='why_join')
    if page.count() != 0:
        context['page'] = page
    return render(request, 'live_affiliates/pages/pages.html', context)


class ReferralSignupView(TemplateView):
    template_name = 'live_affiliates/pages/signup.html'

    def get_context_data(self, referral, *args, **kwargs):
        context = super(ReferralSignupView, self).get_context_data(**kwargs)
        request = self.request
        if referral:
            context['referral'] = referral
        if request.method != 'POST':
            return context


@csrf_exempt
@login_required(login_url='/signup')
@api_view(['POST'])
def change_password_myaccount(request):
    user = request.user
    if user:
        password = request.POST.get('password', False)
        conf_password = request.POST.get('conf_password', False)
        username = request.POST.get('username', False)
        if password != conf_password:
            messages.success(request, 'Password and Confirm Password does not match!')
        elif username:
            u = User.objects.exclude(id=user.id).filter(username=username)
            if u:
                messages.success(request, 'Username already exits! Please choose other username')
            else:
                if password:
                    user.set_password(password)
                user.username = username
                user.save()
            messages.success(request, 'Data Updated successfully')
        return HttpResponseRedirect('/myaccount')
    else:
        return HttpResponseRedirect('/signup')


@csrf_exempt
@login_required(login_url='/signup')
@api_view(['POST'])
def change_personal_info_myaccount(request):
    user = request.user
    if user:
        profile = Profile.objects.get(user=user)
        profile.contact_person = request.POST.get('contact_person', False)
        profile.address = request.POST.get('address', False)
        profile.city = request.POST.get('city', False)
        profile.state = request.POST.get('state', False)
        profile.zip = request.POST.get('zip', False)
        profile.mobile_number = request.POST.get('mobile_number', False)
        profile.phone = request.POST.get('phone', False)
        profile.save()
        messages.success(request, 'Data Updated successfully')
        return HttpResponseRedirect('/myaccount')
    else:
        return HttpResponseRedirect('/signup')


@csrf_exempt
@login_required(login_url='/signup')
@api_view(['POST'])
def change_payment_settings_myaccount(request):
    user = request.user
    if user:
        payment_setting = PaymentSettings.objects.filter(user=user)
        if not payment_setting:
            payment_setting = PaymentSettings()
            payment_setting.user = user
        else:
            payment_setting = PaymentSettings.objects.get(user=user)
        payment_setting.pan_no = request.POST.get('pan_no', False)
        payment_setting.bank_account_number = request.POST.get('bank_account_number', False)
        payment_setting.bank_name = request.POST.get('bank_name', False)
        payment_setting.branch_name = request.POST.get('branch_name', False)
        payment_setting.ifsc_code = request.POST.get('ifsc_code', False)
        payment_setting.save()
        messages.success(request, 'Data Updated successfully')
        return HttpResponseRedirect('/myaccount')
    else:
        return HttpResponseRedirect('/signup')


class ContactUsView(TemplateView):
    template_name = 'live_affiliates/pages/contact.html'

    def get_context_data(self):
        context = super(ContactUsView, self).get_context_data()
        context['contact_thanks_message'] = Page.objects.filter(pagerole='contact_thanks_message').first()
        context['contact_us_address'] = Page.objects.filter(pagerole='contact_us_address').first()
        return context

    def post(self, request, *args, **kwargs):
        super(ContactUsView, self).get(request, *args, **kwargs)
        contact = Contact()
        contact.first_name = request.POST.get('first_name')
        contact.last_name = request.POST.get('last_name')
        contact.email = request.POST.get('email')
        contact.phone = request.POST.get('phone')
        contact.message = request.POST.get('message')
        contact.save()
        mail_subject = 'Contact Us'
        message = render_to_string('live_affiliates/pages/contact_email_template.html', {
            'first_name': contact.first_name,
            'last_name': contact.last_name,
            'email': contact.email,
            'phone': contact.phone,
            'message': contact.message,
        })
        t_eml = ContactEmail.objects.first()
        to_email = t_eml.email
        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        email.send()
        messages.success(request, 'Message sent successfully')
        return HttpResponseRedirect('/contact')


@csrf_exempt
def handler404(request, exception):
    return render(request, 'live_affiliates/404.html', status=404)


@csrf_exempt
def handler500(request):
    return render(request, 'live_affiliates/500.html', status=500)


def snippet_detail(request, slug):
    snippet = get_object_or_404(Snippet, slug=slug)
    return HttpResponse(f'the detailview for slug of {slug}')


# class WidgetJsView(TemplateView):
#     template_name = 'live_affiliates/js/widget.js'

    # def get_context_data(self):
    #     context = super(TrackerJsView, self).get_context_data()
    #
    #     tracker = Tracking.get_tracker(self.request)
    #     context['placeholders'] = json.dumps(
    #         BannerPlaceholderSerializer(BannerPlaceholder.get_placeholders(self.request, tracker), many=True).data)
    #     return context
    #
    # def get(self, request, *args, **kwargs):
    #     response = super(TrackerJsView, self).get(request, *args, **kwargs)
    #     response['Content-type'] = 'text/javascript;charset=UTF-8'
    #     return response


@csrf_exempt
@api_view(['POST'])
@permission_classes([])
@authentication_classes([])
def widget_check_auth(request):
        uid= request.POST.get('key') or None
        wid = request.POST.get('wid') or None
        data = {}
        if wid and wid is not None:
            check_data = GenerateForm.objects.filter(pk=int(wid), user=int(uid)).values('website', 'title', 'width', 'height',\
                                                                                        'border', 'title_background', 'title_text_color',\
                                                                                        'body_text_background', 'body_text_color', 'category',\
                                                                                        'thank_you_url', 'user', 'locations')
            data = list(check_data)
        return JsonResponse(data, safe=False, status=HTTP_200_OK)


@csrf_exempt
@api_view(['POST'])
@permission_classes([])
@authentication_classes([])
def insert_banner_details(request):
        lead_details = LeadDetail()
        lead_details.user_id = request.POST.get('aff_id')  # check user then insert
        lead_details.position = request.POST.get('position')
        lead_details.ip = request.POST.get('ip')
        lead_details.banner_id = request.POST.get('bid') # check banner then insert
        lead_details.referred = request.POST.get('referrer')
        if lead_details:
            lead_details.save()
            return Response("ok", status=HTTP_200_OK)


@csrf_exempt
@api_view(['POST'])
@permission_classes([])
@authentication_classes([])
def generate_form_order_api(request):
        # print(request.POST)
        generate_form_order = GenerateFormOrder()
        generate_form_order.user_id = request.POST.get('aff_id')  # check user then insert
        generate_form_order.source = request.POST.get('source')
        generate_form_order.orderid = request.POST.get('orderid')
        generate_form_order.total_amount = request.POST.get('total_amount') # check banner then insert
        generate_form_order.email = request.POST.get('email')
        generate_form_order.phone = request.POST.get('phone')
        if generate_form_order:
            generate_form_order.save()
            return Response("ok", status=HTTP_200_OK)


class GenerateQueryFormView(LoginRequiredMixin, TemplateView):
    login_url = '/'
    template_name = 'live_affiliates/pages/generate_query_form.html'

    def get_context_data(self):
        context = super(GenerateQueryFormView, self).get_context_data()
        request = self.request
        context['websites'] = Websites.objects.filter(user=request.user)
        context['g_form'] = GenerateQueryForm.objects.filter(user=request.user,isDeleted=False).last()
        return context

    def post(self, request, *args, **kwargs):
        super(GenerateQueryFormView, self).get(request, *args, **kwargs)
        print(request.POST)
        generate_form = GenerateQueryForm()
        generate_form.website = request.POST.get('website')
        generate_form.f_name = request.POST.get('f_name')
        generate_form.f_title = request.POST.get('f_title')
        generate_form.f_description = request.POST.get('f_description')
        generate_form.name = request.POST.get('name')
        generate_form.phone = request.POST.get('phone')
        generate_form.lead_source = request.POST.get('lead_source')
        generate_form.email = request.POST.get('email')
        generate_form.query = request.POST.get('query')
        generate_form.crm_url = request.POST.get('crm_url')
        generate_form.width = request.POST.get('width')
        generate_form.label_color = request.POST.get('label_color')
        generate_form.border = request.POST.get('border')
        generate_form.thank_you = request.POST.get('thank_you_url')
        generate_form.title_background_description = request.POST.get('title_background_description')
        generate_form.title_text_color = request.POST.get('title_text_color')
        generate_form.body_text_background = request.POST.get('body_text_background')
        generate_form.submit_text_color = request.POST.get('submit_text_color')
        generate_form.submit_text_border = request.POST.get('submit_text_border')
        generate_form.user = request.user
        generate_form.save()
        messages.success(request, 'Data Updated successfully')
        return HttpResponseRedirect('/generate_query_form')



@csrf_exempt
@api_view(['POST'])
@permission_classes([])
@authentication_classes([])
def generate_form_order_api_aaa(request):
        print(request.data)
        return Response("ok", status=HTTP_200_OK)


@csrf_exempt
def testpage(request):
    context = {}
    return render(request, 'live_affiliates/pages/testpage.html', context)


