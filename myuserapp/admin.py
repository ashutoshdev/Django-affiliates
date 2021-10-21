from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.db.models import Count, Max
# from metatags.admin import MetaTagInline
from myuserapp.models import Page, Contact, ContactEmail, Testimonials, Banners, Websites, BannerCategory, Profile,\
    PaymentSettings, LeadDetail, LeadCommission, GenerateFormOrder, GenerateForm

admin.site.register(GenerateForm)
@admin.register(Page)
class PageAdmin(ModelAdmin):
    list_display = ['title', 'pagerole']
    fields = ['title', 'description', 'pagerole']
    # inlines = (MetaTagInline,)


@admin.register(ContactEmail)
class ContactEmailAdmin(ModelAdmin):
    list_display = ['email']
    fields = ['email']


@admin.register(Contact)
class ContactAdmin(ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'phone', 'message']
    fields = ['first_name', 'last_name', 'email', 'phone', 'message']


@admin.register(Testimonials)
class TestimonialsAdmin(ModelAdmin):
    list_display = ['title', 'name']
    fields = ['title', 'description', 'name', 'link']


@admin.register(Websites)
class WebsitesAdmin(ModelAdmin):
    list_display = ['user', 'website_address']
    fields = ['user', 'website_address', 'isVerified']


@admin.register(BannerCategory)
class BannerCategoryAdmin(ModelAdmin):
    list_display = ['name', 'status', 'created']
    fields = ['name', 'status']


@admin.register(Banners)
class BannersAdmin(ModelAdmin):
    list_display = ['banner_name', 'banner_image', 'banner_position', 'status', 'banner_category']
    fields = ['banner_name', 'url', 'banner_image', 'banner_position', 'status', 'banner_category']


@admin.register(Profile)
class ProfileAdmin(ModelAdmin):
    list_display = ['user', 'contact_person', 'company_name_or_payee_name', 'created']
    fields = ['user', 'contact_person', 'company_name_or_payee_name', 'mobile_number', 'phone', 'country', 'state', \
              'city', 'address', 'zip', 'business_type', 'refer_by', 'your_referral_code']


@admin.register(PaymentSettings)
class PaymentSettingsAdmin(ModelAdmin):
    list_display = ['user', 'payment_method', 'bank_account_number', 'created']
    fields = ['user', 'payment_method', 'bank_account_number', 'payment_frequency', 'bank_name', 'pan_no', 'branch_name',\
              'ifsc_code', 'zip', 'business_type']


@admin.register(LeadDetail)
class LeadDetailAdmin(ModelAdmin):
    list_display = ['user', 'position', 'ip', 'referred', 'created']
    fields = ['user', 'position', 'ip', 'banner', 'referred', 'lead']


@admin.register(LeadCommission)
class LeadCommissionAdmin(ModelAdmin):
    list_display = ['parent_lead_rate', 'child_lead_rate', 'created']
    fields = ['parent_lead_rate', 'child_lead_rate']


@admin.register(GenerateFormOrder)
class GenerateFormOrderAdmin(ModelAdmin):
    list_display = ['source', 'user', 'orderid', 'total_amount', 'email', 'phone', 'created']
    fields = ['source', 'user', 'orderid', 'total_amount', 'email', 'phone']