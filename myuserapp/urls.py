from django.urls import include, path
from django.conf.urls import url
from myuserapp.views import IndexView, SignupView, SignupSuccessView, EmailVerificationView, LoginView, SalesReportView,\
    BannersView, PaymentDetailsView, WebsitesView, MyAccountView, GenerateFormView, ReportLeadView, MyReferralView,\
    ReferralSignupView, ContactUsView, GenerateFormListView, GenerateFormPreviewView, GenerateButtonView, GenerateButtonListView,\
    GenerateFormEditView, GenerateQueryFormView, GenerateButtonEditView
from myuserapp import views
from django.views.generic import TemplateView
from django.contrib.auth.views import (
    PasswordChangeView, PasswordChangeDoneView,
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
)

app_name = 'myuserapp' # Important

urlpatterns = [
    path('', IndexView.as_view(),  name='index'),
    path('login', LoginView.as_view(), name='login'),
    path('signup', SignupView.as_view(), name='signup'),
    path('signup_success/<user>', SignupSuccessView.as_view(), name='signup_success'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    path('email_verification', EmailVerificationView.as_view(),  name='email_verification'),
    path('resend_activate_email', views.resend_activate_email,  name='resend_activate_email'),
    path('sale_report', SalesReportView.as_view(),  name='sale_report'),
    path('banners', BannersView.as_view(),  name='banners'),
    path('payment_details', PaymentDetailsView.as_view(),  name='payment_details'),
    path('logout', views.logout_view, name='logout'),
    path('websites', WebsitesView.as_view(),  name='websites'),
    path('myaccount', MyAccountView.as_view(),  name='myaccount'),
    path('generate_button', GenerateButtonView.as_view(),  name='generate_button'),
    path('generate_button_edit/<wid>', GenerateButtonEditView.as_view(),  name='generate_button_edit'),
    path('generate_form', GenerateFormView.as_view(),  name='generate_form'),
    path('generate_form_list', GenerateFormListView.as_view(),  name='generate_form_list'),
    path('generate_button_list', GenerateButtonListView.as_view(),  name='generate_button_list'),
    path('generate_form_view/<wid>', GenerateFormPreviewView.as_view(),  name='generate_form_view'),
    path('generate_form_edit/<wid>', GenerateFormEditView.as_view(),  name='generate_form_edit'),
    path('report_lead', ReportLeadView.as_view(),  name='report_lead'),
    path('my_referral', MyReferralView.as_view(),  name='my_referral'),
    path('password_change/', PasswordChangeView.as_view(success_url='/password_change/done/'), name="password_change"),
    path('password_change/done/', PasswordChangeDoneView.as_view(), name="password_change_done"),
    path('password_reset/', PasswordResetView.as_view(success_url='/password_reset/done'), name="password_reset"),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(success_url='/reset/done/'),
         name="password_reset_confirm"),
    path('reset/done/', PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    path('privacy/', views.privacy, name='privacy'),
    # path('404', TemplateView.as_view(template_name="live_affiliates/404.html"), name='404'),
    path('referralsignup/<referral>', ReferralSignupView.as_view(), name='referralsignup'),
    path('change_password_myaccount', views.change_password_myaccount, name='change_password_myaccount'),
    path('change_personal_info_myaccount', views.change_personal_info_myaccount, name='change_personal_info_myaccount'),
    path('change_payment_settings_myaccount', views.change_payment_settings_myaccount, name='change_payment_settings_myaccount'),
    path('contact', ContactUsView.as_view(), name='contact'),
    path('about/', views.about, name='about'),
    path('term/', views.term_and_condition, name='term_and_condition'),
    path('steps/', views.step_to_use, name='step_to_use'),
    path('faq/', views.faq, name='faq'),
    path('advantages_and_benefits/', views.advantages_and_benefits, name='advantages_and_benefits'),
    path('why_join/', views.why_join, name='why_join'),
    path('testpage/', views.testpage, name='testpage'),
    # path('js/widget.js', WidgetJsView.as_view(), name='widget-js'),
    path('api/v1/auth', views.widget_check_auth),
    path('api/v1/bannerApi', views.insert_banner_details),
    path('api/v1/generateFormOrderApi', views.generate_form_order_api),
    path('generate_query_form/', GenerateQueryFormView.as_view(),  name='generate_query_form'),
    path('generate_form_order_api_aaa', views.generate_form_order_api_aaa,  name='generate_form_order_api_aaa'),
    path('<slug:slug>/', views.snippet_detail),
]
