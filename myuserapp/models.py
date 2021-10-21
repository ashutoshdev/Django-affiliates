from django.contrib.auth.models import User
from django.db.models import *
from djrichtextfield.models import RichTextField


class Profile(Model):
    user = ForeignKey(User, on_delete=CASCADE, blank=True, null=True)
    contact_person = TextField(max_length=500, blank=False, null=False)
    company_name_or_payee_name = TextField(max_length=500, blank=False, null=False)
    mobile_number = TextField(null=False, blank=False)
    phone = TextField(null=False, blank=True)
    country = TextField(max_length=50, blank=False)
    state = TextField(max_length=50, blank=True)
    city = TextField(max_length=50, blank=False)
    address = TextField(max_length=1000, blank=False)
    zip = TextField(max_length=50, blank=False)
    business_type = TextField(max_length=5000, blank=False)
    refer_by = TextField(max_length=500, blank=True)
    your_referral_code = TextField(max_length=500, blank=True)
    isVerified = BooleanField(default=False)
    status = BooleanField(default=True)
    isDeleted = BooleanField(default=False)
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)
    created_by = ForeignKey(User, related_name='user_created_by', on_delete=CASCADE, blank=True, null=True)
    updated_by = ForeignKey(User, related_name='user_updated_by', on_delete=CASCADE, blank=True, null=True)

    # @receiver(post_save, sender=User)
    # def update_user_profile(sender, instance, created, **kwargs):
    #     if created:
    #         Profile.objects.create(user=instance)
    #         print('User has been successfully created....')
    #     instance.profile.save()


class PaymentSettings(Model):
    user = ForeignKey(User, on_delete=CASCADE, blank=True, null=True)
    payment_method = TextField(max_length=50, blank=False, null=False , default='Cheque')
    bank_account_number = IntegerField(null=False, blank=False)
    payment_frequency = TextField(max_length=500, blank=False, default='Monthly')
    bank_name = TextField(max_length=500, blank=False)
    pan_no = TextField(max_length=100, blank=True)
    branch_name = TextField(max_length=100, blank=False)
    ifsc_code = TextField(max_length=100, blank=False)
    zip = TextField(max_length=100, blank=False)
    business_type = TextField(max_length=100, blank=False)
    isVerified = BooleanField(default=False)
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)
    created_by = ForeignKey(User, related_name='payment_created_by', on_delete=CASCADE, blank=True, null=True)
    updated_by = ForeignKey(User, related_name='payment_updated_by', on_delete=CASCADE, blank=True, null=True)


class Websites(Model):
    user = ForeignKey(User, on_delete=CASCADE, blank=True, null=True)
    website_address = TextField(max_length=500, blank=False, null=False)
    isVerified = BooleanField(default=False)
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)
    created_by = ForeignKey(User, related_name='website_created_by', on_delete=CASCADE, blank=True, null=True)
    updated_by = ForeignKey(User, related_name='website_updated_by', on_delete=CASCADE, blank=True, null=True)

    def __str__(self):
        return self.website_address

banner_position = [
    ('top', 'top'),
    ('side', 'side'),
    ('middle', 'middle'),
    ('bottom', 'bottom'),
]

class BannerCategory(Model):
    name = TextField(max_length=500, blank=False, null=False)
    status = BooleanField(default=False)
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)
    created_by = ForeignKey(User, related_name='banner_cat_created_by', on_delete=CASCADE, blank=True, null=True)
    updated_by = ForeignKey(User, related_name='banner_cat_updated_by', on_delete=CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name


class Banners(Model):
    banner_category = ForeignKey(BannerCategory, on_delete=CASCADE, blank=True, null=True)
    status = BooleanField(default=False)
    banner_image = ImageField(upload_to='banner/')
    banner_name = TextField(max_length=500, blank=False, null=False)
    url = TextField(max_length=500, blank=True, null=True)
    banner_position = TextField(default='', choices=banner_position, blank=True, null=True, verbose_name='banner_position')
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)
    created_by = ForeignKey(User, related_name='banner_created_by', on_delete=CASCADE, blank=True, null=True)
    updated_by = ForeignKey(User, related_name='banner_updated_by', on_delete=CASCADE, blank=True, null=True)

    def __str__(self):
        return self.banner_name


class Page(Model):
    title = TextField(default='', blank=False, null=False, verbose_name='title')
    pagerole = TextField(default='', blank=False, null=False, verbose_name='pagerole')
    description = RichTextField(default='', blank=True, null=True, verbose_name='description')
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)
    created_by = ForeignKey(User, related_name='page_created_by', on_delete=CASCADE, blank=True, null=True)
    updated_by = ForeignKey(User, related_name='page_updated_by', on_delete=CASCADE, blank=True, null=True)


class Contact(Model):
    first_name = TextField(default='', blank=False, null=False, verbose_name='first_name')
    last_name = TextField(default='', blank=False, null=False, verbose_name='last_name')
    email = TextField(default='', blank=False, null=False, verbose_name='email')
    phone = TextField(default='', blank=False, null=False, verbose_name='phone')
    message = TextField(default='', blank=True, null=True, verbose_name='message')
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)


class ContactEmail(Model):
    email = TextField(default='', blank=False, null=False, verbose_name='email')
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)


class Testimonials(Model):
    title = TextField(default='', blank=False, null=False, verbose_name='title')
    name = TextField(default='', blank=False, null=False, verbose_name='name')
    link = TextField(default='', blank=False, null=False, verbose_name='link')
    description = RichTextField(default='', blank=True, null=True, verbose_name='description')
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)
    created_by = ForeignKey(User, related_name='testimonials_created_by', on_delete=CASCADE, blank=True, null=True)
    updated_by = ForeignKey(User, related_name='testimonials_updated_by', on_delete=CASCADE, blank=True, null=True)


class Snippet(Model):
    title = CharField(max_length=80)
    slug = SlugField(blank=True, null=True)
    body = TextField()

def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

def get_absolute_url(self):
        return f'/{self.slug}'


class LeadDetail(Model):
    user = ForeignKey(User, on_delete=CASCADE, blank=True, null=True)
    position =  TextField(default='', choices=banner_position, blank=True, null=True, verbose_name='banner_position')
    ip = TextField(default='127.0.0.1', blank=False, null=False, verbose_name='ip')
    banner = ForeignKey(Banners, on_delete=CASCADE, blank=True, null=True)
    lead = IntegerField(default=1, verbose_name='lead')
    referred = TextField(default='127.0.0.1', blank=True, null=True, verbose_name='referred')
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)
    created_by = ForeignKey(User, related_name='LeadDetail_created_by', on_delete=CASCADE, blank=True, null=True)
    updated_by = ForeignKey(User, related_name='LeadDetail_updated_by', on_delete=CASCADE, blank=True, null=True)


class GenerateForm(Model):
    user = ForeignKey(User, on_delete=CASCADE, blank=True, null=True)
    website =TextField(default='', blank=False, null=False, verbose_name='website')
    name = TextField(default='', blank=False, null=False, verbose_name='name')
    title = TextField(default='', blank=False, null=False, verbose_name='title')
    category = TextField(default='', blank=False, null=False, verbose_name='category')
    locations = TextField(default='', blank=False, null=False, verbose_name='locations')
    width = TextField(default='', blank=False, null=False, verbose_name='width')
    height = TextField(default='', blank=False, null=False, verbose_name='height')
    border = TextField(default='', blank=False, null=False, verbose_name='border')
    title_background = TextField(default='', blank=False, null=False, verbose_name='title_background')
    title_text_color = TextField(default='', blank=False, null=False, verbose_name='title_text_color')
    thank_you_url = TextField(default='', blank=False, null=False, verbose_name='thank_you_url')
    body_text_background = TextField(default='', blank=False, null=False, verbose_name='body_text_background')
    body_text_color = TextField(default='', blank=False, null=False, verbose_name='body_text_color')
    script = TextField(default='', blank=False, null=False, verbose_name='script')
    isDeleted = BooleanField(default=False)
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)
    created_by = ForeignKey(User, related_name='GenerateForm_created_by', on_delete=CASCADE, blank=True, null=True)
    updated_by = ForeignKey(User, related_name='GenerateForm_updated_by', on_delete=CASCADE, blank=True, null=True)


class LeadCommission(Model):
    parent_lead_rate = TextField(default='0', blank=False, null=False, verbose_name='parent_lead_rate')
    child_lead_rate = TextField(default='0', blank=False, null=False, verbose_name='child_lead_rate')
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)
    created_by = ForeignKey(User, related_name='LeadCommission_created_by', on_delete=CASCADE, blank=True, null=True)
    updated_by = ForeignKey(User, related_name='LeadCommission_updated_by', on_delete=CASCADE, blank=True, null=True)


class GenerateFormOrder(Model):
    source = TextField(default='0', blank=True, null=True, verbose_name='source')
    user = ForeignKey(User, on_delete=CASCADE, blank=True, null=True)
    orderid = TextField(default='0', blank=True, null=True, verbose_name='orderid')
    total_amount = TextField(default='0', blank=True, null=True, verbose_name='total_amount')
    email = TextField(default='0', blank=True, null=True, verbose_name='email')
    phone = TextField(default='0', blank=True, null=True, verbose_name='phone')
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)
    created_by = ForeignKey(User, related_name='GenerateFormOrder_created_by', on_delete=CASCADE, blank=True, null=True)
    updated_by = ForeignKey(User, related_name='GenerateFormOrder_updated_by', on_delete=CASCADE, blank=True, null=True)


class GenerateButton(Model):
    user = ForeignKey(User, on_delete=CASCADE, blank=True, null=True)
    website =TextField(default='', blank=False, null=False, verbose_name='website')
    name = TextField(default='', blank=False, null=False, verbose_name='name')
    title = TextField(default='', blank=False, null=False, verbose_name='title')
    category = TextField(default='', blank=False, null=False, verbose_name='category')
    locations = TextField(default='', blank=False, null=False, verbose_name='locations')
    width = TextField(default='', blank=False, null=False, verbose_name='width')
    height = TextField(default='', blank=False, null=False, verbose_name='height')
    border = TextField(default='', blank=False, null=False, verbose_name='border')
    title_background = TextField(default='', blank=False, null=False, verbose_name='title_background')
    title_text_color = TextField(default='', blank=False, null=False, verbose_name='title_text_color')
    size = TextField(default='', blank=False, null=False, verbose_name='size')
    css = TextField(default='', blank=False, null=False, verbose_name='script')
    isDeleted = BooleanField(default=False)
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)
    created_by = ForeignKey(User, related_name='GenerateButton_created_by', on_delete=CASCADE, blank=True, null=True)
    updated_by = ForeignKey(User, related_name='GenerateButton_updated_by', on_delete=CASCADE, blank=True, null=True)


class GenerateQueryForm(Model):
    user = ForeignKey(User, on_delete=CASCADE, blank=True, null=True)
    website =TextField(default='', blank=False, null=False, verbose_name='website')
    f_name = TextField(default='', blank=False, null=False, verbose_name='f_name')
    f_title = TextField(default='', blank=False, null=False, verbose_name='f_title')
    f_description = TextField(default='', blank=False, null=False, verbose_name='f_description')
    name = TextField(default='', blank=True, null=True, verbose_name='name')
    email =TextField(default='', blank=True, null=True, verbose_name='email')
    phone = TextField(default='', blank=True, null=True, verbose_name='phone')
    query = TextField(default='', blank=True, null=True, verbose_name='Query')
    crm_url = TextField(default='', blank=True, null=True, verbose_name='crm_url')
    width = TextField(default='', blank=False, null=False, verbose_name='width')
    label_color = TextField(default='', blank=False, null=False, verbose_name='label_color')
    border = TextField(default='', blank=False, null=False, verbose_name='border')
    title_text_color = TextField(default='', blank=False, null=False, verbose_name='title_text_color')
    title_background_description = TextField(default='', blank=False, null=False, verbose_name='title_background')
    body_text_background = TextField(default='', blank=False, null=False, verbose_name='body_text_background')
    submit_text_color = TextField(default='', blank=False, null=False, verbose_name='submit_text_color')
    submit_text_border = TextField(default='', blank=False, null=False, verbose_name='submit_text_border')
    lead_source = TextField(default='', blank=False, null=False, verbose_name='lead_source')
    thank_you = TextField(default='', blank=False, null=False, verbose_name='thank_you')
    isDeleted = BooleanField(default=False)
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)
    created_by = ForeignKey(User, related_name='GenerateQueryForm_created_by', on_delete=CASCADE, blank=True, null=True)
    updated_by = ForeignKey(User, related_name='GenerateQueryForm_updated_by', on_delete=CASCADE, blank=True, null=True)