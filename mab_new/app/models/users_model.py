from django.db import models
from django.contrib.auth.models import User
from app.other_constants import *
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.crypto import get_random_string

from app.models.contacts_model import *
from app.models.accounts_model import *

#==========================================================================
#   CHANGE LOGO FILE NAMES
#==========================================================================
#
def logo_rename(instance, filename):

    upload_path = 'logos'
    ext = filename.split('.')[-1]
    return  os.path.join(upload_path,'{}.{}'.format(uuid4().hex, ext))


#==================================================================
# Create instances on User Creation
#==================================================================
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        pro = Profile.objects.create(user=instance)
        pro.app_id = 'APK-'+get_random_string(length=10)
        pro.save()

        organisation = Organisations.objects.create(user=instance)
        organisation.save()


#**************************************************************************
# User Organisation Basic Details
#**************************************************************************

class Organisations(models.Model):
    user = models.ForeignKey(
        User,
        db_index = True,
        on_delete = models.CASCADE,
        null = True,
        blank = True,
    ) 
        
    organisation_name = models.CharField(
        max_length = 250,
        db_index = True,
        blank = False,
        null = False,
    )

    organisation_legal_name = models.CharField(
        max_length = 250,
        db_index = True,
        blank = False,
        null = False,
    )

    logo = models.FileField(
        null = True,
        blank = True,
        upload_to = logo_rename,
    )
    
    organisation_description = models.TextField(
        null = True,
        blank = True,
    )

    line_of_business = models.IntegerField(
        default = 1,
        null = True,
        blank = True,
        choices = user_constants.LINE_OF_ORGANISATION,
    )

    organisation_type = models.IntegerField(
        db_index = True,
        choices = user_constants.ORGANIZATION_TYPE,
        default = 1,
    )

    organisation_pan = models.CharField(
        max_length = 10,
        db_index = True,
        blank = True,
        null = True,
    )

    organisation_cin = models.CharField(
        max_length= 21,
        db_index = True,
        null = True,
        blank = True,
    )
    
    print_info_voucher = models.CharField(
        max_length = 250,
        db_index = True,
        blank = True,
        null = True,
    )

    terms_and_condition = models.CharField(
        max_length = 400,
        db_index = True,
        blank = True,
        null = True,
    )

    purchase_terms_and_condition = models.CharField(
        max_length = 400,
        db_index = True,
        blank = True,
        null = True,
    )

    purchase_note = models.CharField(
        max_length = 400,
        db_index = True,
        blank = True,
        null = True,
    )

    def __str__(self):
        return self.organisation_name

    class META:
        verbose_name_plural = 'organisation_tbl'


#**************************************************************************
#   USER'S PROFILE DETAILS
#**************************************************************************
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, db_index = True,)
    
    app_id = models.CharField(
        max_length = 30,
        db_index = True,
        blank = True,
        null = True,
    )
    
    display_name = models.CharField(
        max_length = 250,
        blank = False,
        db_index = True,
        null = True,
    )

    salutation = models.IntegerField(
        db_index = True,
        default = 0,
        choices = user_constants.SALUTATIONS,
        blank = True,
    )

    customer_type = models.IntegerField(
        db_index = True,
        choices = user_constants.CUSTOMER_TYPE,
        default = 1,
        blank = True,
    )

    phone = models.CharField(
        max_length = 30,
        db_index = True,
        blank = True,
        null = True,
    )

    fax = models.CharField(
        max_length = 30,
        db_index = True,
        blank = True,
        null = True,
    )    
    
    pan = models.CharField(
        max_length = 12,
        blank = False,
        db_index = True,
        null = True,
    )

    website = models.CharField(
        max_length = 250,
        db_index = True,
        blank = True,
        null = True,
    )
    
    facebook = models.CharField(
        max_length = 250,
        db_index = True,
        blank = True,
        null = True,
    )
    
    twitter = models.CharField(
        max_length = 250,
        db_index = True,
        blank = True,
        null = True,
    )
    
    skype = models.CharField(
        max_length = 250,
        db_index = True,
        blank = True,
        null = True,
    )
    
    linkedin = models.CharField(
        max_length = 250,
        db_index = True,
        blank = True,
        null = True,
    )

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'user_profile_tbl'

#**************************************************************************
#   USER'S ACCOUNT DETAILS
#**************************************************************************
class User_Account_Details(models.Model):

    is_user = models.BooleanField(
        default = False,
        db_index = True,
        choices = user_constants.IS_TRUE,
    )

    user = models.ForeignKey(
        User,
        blank = True,
        null = True, 
        on_delete = models.CASCADE,
        db_index = True,
    )

    contact = models.ForeignKey(
        Contacts,
        db_index = True,
        null = True,
        blank = True,
        on_delete = models.CASCADE
    )

    account_number = models.CharField(
        max_length = 250,
        blank = True,
        db_index = True,
        null = True,
    )

    account_holder_name = models.CharField(
        max_length = 250,
        blank = True,
        db_index = True,
        null = True,
    )

    ifsc_code = models.CharField(
        max_length = 20,
        blank = True,
        db_index = True,
        null = True,
    )

    bank_name = models.CharField(
        max_length = 250,
        db_index = True,
        blank = True,
        null = True,
    )

    bank_branch_name = models.CharField(
        max_length = 250,
        db_index = True,
        blank = True,
        null = True,
    )

    created_on = models.DateTimeField(
        auto_now = True,
        db_index = True,
        null = True,
    )

    updated_on = models.DateTimeField(
        auto_now = False,
        db_index = True,
        null = True,
    )

    class Meta:
        verbose_name_plural = 'user_account_details_tbl'


#**************************************************************************
#   EMAIL ADDRESSES OF CONTACTS
#   A CONTACT/USER CAN HAVE MULTIPLE MAIL ADDRESSES
#**************************************************************************
class User_Email_Details(models.Model):

    is_user = models.BooleanField(
        default = False,
        db_index = True,
        choices = user_constants.IS_TRUE,
    )

    user = models.ForeignKey(
        User,
        blank = True,
        null = True, 
        on_delete = models.CASCADE,
        db_index = True,
    )

    contact = models.ForeignKey(
        Contacts,
        db_index = True,
        null = True,
        blank = True,
        on_delete = models.CASCADE
    )
    
    email = models.EmailField(
        blank = False, 
        null = True, 
        db_index = True,
    )

    is_official = models.BooleanField(
        db_index = True,
        choices = user_constants.IS_TRUE,
        default = True,
    )

    is_personal = models.BooleanField(
        db_index = True,
        choices = user_constants.IS_TRUE,
        default = True,
    )

    created_on = models.DateTimeField(
        auto_now = True,
        db_index = True,
        null = True,
    )

    updated_on = models.DateTimeField(
        auto_now = False,
        db_index = True,
        null = True,
    )

    def is_official_full(self):
        if self.is_official:
            return "YES"
        return "NO" 

    def is_personal_full(self):
        if self.is_personal:
            return "YES"
        return "NO" 

    class Meta:
        verbose_name_plural = 'user_email_tbl'


#**************************************************************************
#   Tax Details OF users
#   A user CAN HAVE only one tax detail
#**************************************************************************

class User_Tax_Details(models.Model):
    
    is_user = models.BooleanField(
        db_index = True,
        default = False,
        choices = user_constants.IS_TRUE,
    )
    
    user = models.ForeignKey(
        User,
        db_index = True,
        on_delete = models.CASCADE,
        null = True,
        blank = True,
    )

    contact = models.ForeignKey(
        Contacts,
        db_index = True,
        on_delete = models.CASCADE,
        null = True,
        blank = True,
    )
    
    is_organisation = models.BooleanField(
        db_index = True,
        default = False,
        choices = user_constants.IS_TRUE,
    )
    
    organisation = models.ForeignKey(
        Organisations,
        db_index = True,
        on_delete = models.CASCADE,
        null = True,
        blank = True,
    )

    pan = models.CharField(
        max_length = 10,
        db_index = True,
        blank = True,
        null = True,
    )

    gstin = models.CharField(
        max_length = 100,
        db_index = True,
        blank = True,
        null = True,
    )

    gst_reg_type = models.IntegerField(
        db_index = True,
        default = 0,
        choices = user_constants.GST_REG_TYPE,
        blank = True,
        null = True,
    )

    business_reg_no = models.CharField(
        max_length = 15,
        blank = True,
        null = True,
        db_index = True,
    )

    tax_reg_no = models.CharField(
        max_length = 15,
        blank = True,
        null = True,
        db_index = True,
    )

    cst_reg_no = models.CharField(
        max_length = 15,
        blank = True,
        null = True,
        db_index = True,
    )

    tds = models.IntegerField(
        db_index = True,
        null = True,
        blank = True,
        default = 0.00,
    )

    preferred_currency = models.CharField(
        max_length = 5,
        db_index = True,
        default="INR",
        choices = currency_list.CURRENCY_CHOICES,
        blank = True,
        null = True,
    )

    opening_balance = models.CharField(
        max_length = 250,
        blank = True,
        null = True,
        db_index = True,
        default = 0.00,
    )

    as_of = models.DateTimeField(
        auto_now = True,
        db_index = True,
        null = True,
    )

    preferred_payment_method = models.IntegerField(
        null = True,
        blank = True,
        db_index = True,
        choices = payment_constants.PREFERRED_PAYMENT_TYPE,
        default = 0
    )

    preferred_delivery = models.IntegerField(
        default = 0,
        db_index = True,
        choices = payment_constants.PREFERRED_DELIVERY,
        null = True,
        blank = True,
    )

    invoice_terms = models.IntegerField(
        null = True,
        blank = True,
        db_index = True,
        choices = payment_constants.PAYMENT_DAYS,
    )

    bills_terms = models.IntegerField(
        null = True,
        blank = True,
        db_index = True,
        choices = payment_constants.PAYMENT_DAYS,
    )

    class META:
        verbose_name_plural = 'user_tax_details_tbl'



#**************************************************************************
#   ADDRESSES OF USERs
#   A User CAN HAVE MULTIPLE ADDRESSES
#**************************************************************************

class User_Address_Details(models.Model):

    is_user = models.BooleanField(
        db_index = True,
        default = False,
        choices = user_constants.IS_TRUE,
    )

    user = models.ForeignKey(
        User,
        db_index = True,
        on_delete = models.CASCADE,
        null = True,
        blank = True,
    )

    contact = models.ForeignKey(
        Contacts,
        db_index = True,
        on_delete = models.CASCADE,
        null = True,
        blank = True,
    )

    is_organisation = models.BooleanField(
        db_index = True,
        default = False,
        choices = user_constants.IS_TRUE,
    )
    
    default_address = models.BooleanField(
        db_index = True,
        default = False,
        choices = user_constants.IS_TRUE,
        blank = True,
        null = True,
    )
    
    address_tag = models.TextField(
        blank = True,
        null = True,
    )
    
    organisation = models.ForeignKey(
        Organisations,
        db_index = True,
        on_delete = models.CASCADE,
        null = True,
        blank = True,
    )
    
    organisation_tax = models.ForeignKey(
        User_Tax_Details,
        db_index = True,
        on_delete = models.CASCADE,
        null = True,
        blank = True,
    )    

    contact_person = models.CharField(
        blank = True,
        null = True,
        max_length = 250,
    )

    flat_no = models.CharField(
        max_length = 250,
        blank = True,
        null = True,
        db_index = True,
    )

    street = models.CharField(
        max_length = 250,
        blank = True,
        null = True,
        db_index = True,
    )

    city = models.CharField(
        max_length = 250,
        blank = True,
        null = True,
        db_index = True,
    )

    state = models.CharField(
        max_length = 250,
        blank = True,
        null = True,
        db_index = True,
        choices = country_list.STATE_LIST_CHOICES,
    )

    country = models.CharField(
        max_length = 5,
        blank = True,
        null = True,
        db_index = True,
        choices = country_list.COUNTRIES_LIST_CHOICES,
        default = 'IN',
    )

    pincode = models.CharField(
        max_length = 250,
        blank = True,
        null = True,
        db_index = True,
    )

    is_shipping_address_diff = models.IntegerField(
        db_index = True,
        choices = user_constants.IS_NUM_CHOICE,
        default = 0,
        null = True,
        blank = True,
    ) 
    
    is_billing_address = models.IntegerField(
        db_index = True,
        choices = user_constants.IS_NUM_CHOICE,
        default = 1,
        null = True,
        blank = True,
    ) 

    is_shipping_address = models.IntegerField(
        db_index = True,
        choices = user_constants.IS_NUM_CHOICE,
        default = 1,
        null = True,
        blank = True,
    )

    # address_belong = models.IntegerField(
    #     db_index = True,
    #     null = True,
    #     blank = True,
    # )

    created_on = models.DateTimeField(
        auto_now = True,
        db_index = True,
        null = True,
    )

    updated_on = models.DateTimeField(
        auto_now = False,
        db_index = True,
        null = True,
    )    

    def __str__(self):
        return str(self.flat_no)+", "+str(self.street)+", "+str(self.city)

    def complete_billing_address(self):
        return self.flat_no +", "+self.street

    def is_billing_address_full(self):
        if self.is_billing_address:
            return "YES"
        return "NO"

    def is_shipping_address_full(self):
        if self.is_shipping_address:
            return "YES"
        return "NO"

    def same_billing_shipping_address_full(self):
        if self.is_billing_address == self.is_shipping_address:
            return "YES"
        return "NO"

    class Meta:
        verbose_name_plural = 'user_address_details_tbl'
        
##########################################################
# User Organisation Other details
#########################################################
class Organisation_Contact(models.Model):

    organisation = models.ForeignKey(
        Organisations,
        db_index = True,
        on_delete = models.CASCADE,
        null = True,
        blank = True,
    ) 
    
    phone = models.CharField(
        max_length = 50,
        db_index = True,
        blank = False,
        null = False,
    )
    
    email = models.CharField(
        max_length = 250,
        blank = True, 
        null = False, 
        db_index = False,
    )

    website = models.CharField(
        max_length = 250,
        db_index = True,
        blank = True,
        null = True,
    )
    
    fax = models.CharField(
        max_length = 50,
        db_index = True,
        blank = True,
        null = True,
    )

    skype = models.CharField(
        max_length = 250,
        db_index = True,
        blank = True,
        null = True,
    )

    linkedin = models.CharField(
        max_length = 250,
        db_index = True,
        blank = True,
        null = True,
    )

    facebook = models.CharField(
        max_length = 250,
        db_index = True,
        blank = True,
        null = True,
    )
    
    
    class META:
        verbose_name_plural = 'organisation_contact_tbl'
    



##########################################################
# User Organisation Other details
#########################################################
class Organisation_Info(models.Model):  
    
    organisation = models.ForeignKey(
        Organisations,
        db_index = True,
        on_delete = models.CASCADE,
        null = True,
        blank = True,
    ) 
    
    organisation_type = models.BooleanField(
        db_index = True,
        choices = user_constants.IS_TRUE,
        default = False,
    )

    organisation_name = models.BooleanField(
        db_index = True,
        choices = user_constants.IS_TRUE,
        default = False,
    )

    organisation_legal_name = models.BooleanField(
        db_index = True,
        choices = user_constants.IS_TRUE,
        default = False,
    )
    
    organisation_info = models.BooleanField(
        db_index = True,
        choices = user_constants.IS_TRUE,
        default = False,
    )
    
    line_of_business = models.BooleanField(
        db_index = True,
        choices = user_constants.IS_TRUE,
        default = False,
    )

    logo = models.BooleanField(
        db_index = True,
        choices = user_constants.IS_TRUE,
        default = False,
    )
    
    pan = models.BooleanField(
        db_index = True,
        choices = user_constants.IS_TRUE,
        default = False,
    )

    gstin = models.BooleanField(
        db_index = True,
        choices = user_constants.IS_TRUE,
        default = False,
    )

    gst_reg_type = models.BooleanField(
        db_index = True,
        choices = user_constants.IS_TRUE,
        default = False,
    )
    
    cin = models.BooleanField(
        db_index = True,
        choices = user_constants.IS_TRUE,
        default = False,
    )

    description = models.BooleanField(
        db_index = True,
        choices = user_constants.IS_TRUE,
        default = False,
    )
    
    flat_no = models.BooleanField(
        db_index = True,
        choices = user_constants.IS_TRUE,
        default = False,
    )

    street = models.BooleanField(
        db_index = True,
        choices = user_constants.IS_TRUE,
        default = False,
    )

    city = models.BooleanField(
        db_index = True,
        choices = user_constants.IS_TRUE,
        default = False,
    )

    state = models.BooleanField(
        db_index = True,
        choices = user_constants.IS_TRUE,
        default = False,
    )

    country = models.BooleanField(
        db_index = True,
        choices = user_constants.IS_TRUE,
        default = False,
    )

    pincode = models.BooleanField(
        db_index = True,
        choices = user_constants.IS_TRUE,
        default = False,
    )
    
    email = models.BooleanField(
        db_index = True,
        choices = user_constants.IS_TRUE,
        default = False,
    )
    
    phone = models.BooleanField(
        db_index = True,
        choices = user_constants.IS_TRUE,
        default = False,
    )
    
    fax = models.BooleanField(
        db_index = True,
        choices = user_constants.IS_TRUE,
        default = False,
    )
    
    website = models.BooleanField(
        db_index = True,
        choices = user_constants.IS_TRUE,
        default = False,
    )
    
    facebook = models.BooleanField(
        db_index = True,
        choices = user_constants.IS_TRUE,
        default = False,
    )
    
    twitter = models.BooleanField(
        db_index = True,
        choices = user_constants.IS_TRUE,
        default = False,
    )
    
    skype = models.BooleanField(
        db_index = True,
        choices = user_constants.IS_TRUE,
        default = False,
    )
    
    linkedin = models.BooleanField(
        db_index = True,
        choices = user_constants.IS_TRUE,
        default = False,
    )