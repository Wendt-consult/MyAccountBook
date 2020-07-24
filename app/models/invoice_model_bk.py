from django.db import models
from django.contrib.auth.models import User
from app.models.contacts_model import *
from app.models.collects_model import *
from app.models.users_model import *
from app.models.products_model import *

from uuid import uuid4
import os

#==========================================================================
#   CHANGE LOGO FILE NAMES
#==========================================================================
#
def logo_rename(instance, filename):

    upload_path = 'logos'
    ext = filename.split('.')[-1]
    return  os.path.join(upload_path,'{}.{}'.format(uuid4().hex, ext))

#==========================================================================
#   CHANGE ATTACHMENT FILE NAMES
#==========================================================================
#
def attachment_file_rename(instance, filename):

    upload_path = 'invoice_attachments'
    ext = filename.split('.')[-1]
    return  os.path.join(upload_path,'{}.{}'.format(uuid4().hex, ext))


#==========================================================================
#   USER INVOICE DESIGN MODEL
#==========================================================================
#
class Invoice_Templates(models.Model):

    DESIGN_STYLES = (
        (1, 'GREEN TEMPLATE'),
        (2, 'ORANGE TEMPLATE'),
        (3, 'BLUE TEMPLATE'),
        (4, 'WHITE TEMPLATE'),
        (5, 'GREY TEMPLATE'),
        (6, 'CUSTOM TEMPLATE')
    )

    IS_ACTIVE = ((True, 'YES'), (False, 'NO'))

    USER_NAME_ON_TEMPLATE = (
        (True, 'USE USER FIRSTNAME LASTNAME'),
        (False,'USE CUSTOM USERNAME'),
    )

    user = models.ForeignKey(
        User, 
        db_index = True, 
        on_delete = models.CASCADE,
        null = True,
        blank = True,
    )

    template_name = models.CharField(
        max_length = 250,
        db_index = True,
        null = False,
        blank = False,
    )

    design_number = models.IntegerField(        
        db_index = True,
        default = 1,
        choices = DESIGN_STYLES,
    )

    logo = models.FileField(
        null = True,
        blank = True,
        upload_to = logo_rename,
    )

    header_bgcolor = models.CharField(
        max_length = 20,
        null = True,
        blank = True,
        default = "#FFFFFF",
    )

    header_fgcolor = models.CharField(
        max_length = 20,
        null = True,
        blank = True,
        default = "#000000",
    )

    other_design_colors = models.CharField(
        max_length = 20,
        blank =  True,
        null = True,
        default = "#FFFFFF",
    )

    is_active = models.BooleanField(
        db_index = True,
        choices =  IS_ACTIVE,
        default = True,
    )

    user_display_name = models.BooleanField(
        db_index = True,
        choices = USER_NAME_ON_TEMPLATE,
        default = True,
    )

    user_custom_name = models.CharField(
        max_length = 250,
        blank = True,
        null = True,
    )

    user_phone = models.CharField(
        max_length = 30,
        blank = True,
        null = True,
    )

    user_email = models.CharField(
        max_length = 250,
        blank = True,
        null = True,
    )

    billing_address = models.ForeignKey(
        User_Address_Details,
        blank = True,
        null = True,
        db_index = True,
        on_delete = models.SET_NULL,
    )

    total_usage = models.IntegerField(
        db_index = True,
        null = True,
        blank = True,
    )

    created_on = models.DateTimeField(
        auto_now = True,
        db_index = True,
    )

    def __str__(self):
        return self.template_name.upper() 


#==========================================================================
#   INVOICE MODEL
#==========================================================================

class InvoiceModel(models.Model):

    invoice_template = models.ForeignKey(
        Invoice_Templates,
        db_index = True,
        null = True,
        blank = True,
        on_delete = models.SET_NULL,
    )

    service_provider = models.ForeignKey(
        User, 
        on_delete = models.SET_NULL, 
        null = True,
        blank = True,
        db_index = True,
    )

    service_recipient = models.ForeignKey(
        Contacts, 
        on_delete = models.SET_NULL, 
        db_index = True,
        null = True,
        blank = True,
    )

    service_recipient_address = models.IntegerField(
        null = True,
        blank = True,
        db_index = True,
    )


    invoice_no = models.CharField(
        max_length = 20,
        db_index = True,
        blank = True,
        null = True,
    )

    invoice_type = models.BooleanField(
        default = False,
        db_index = True,
        blank = True,
        null = True,
        choices = products_constant.INVOICE_TYPE
    )

    provider_state_code = models.CharField(
        max_length = 10,
        null = True,
        blank = True,
        db_index = True,
    ) 

    recipient_state_code = models.CharField(
        max_length = 10,
        null = True,
        blank = True,
        db_index = True,
    ) 

    sac_code = models.CharField(
        max_length = 20,
        null = True,
        blank = True,
        db_index = True,
    ) 

    service_description = models.TextField(
        blank = True,
        null = True,
    )

    collect = models.ForeignKey(
        Collections,
        db_index = True,
        blank = True,
        null = True,
        on_delete = models.CASCADE,
    ) 

    cgst = models.FloatField(
        default = 0,
        db_index = True,
    )

    igst = models.FloatField(
        default = 0,
        db_index = True,
    )

    sgst = models.FloatField(
        default = 0,
        db_index = True,
    )

    total_gst = models.FloatField(
        default = 0,
        db_index = True,
    )

    adjustment = models.IntegerField(
        default = 0,
        db_index = True,
    )

    shipping = models.IntegerField(
        default = 0,
        db_index = True,
    )

    discount = models.IntegerField(
        default = 0,
        db_index = True,
    )

    sales_person = models.ForeignKey(
        Contacts,
        on_delete = models.SET_NULL,
        blank = True,
        null = True,
        related_name = 'sales_person'
    )

    due_date = models.DateField(
        null = True,
        blank = True,
        db_index = True,
    )

    terms_invoice = models.CharField(
        blank = True,
        max_length = 50,
        null = True,
    )

    message = models.TextField(
        null = True,
        blank = True,
    )

    attachments = models.FileField(
        null = True,
        blank = True,
        upload_to = attachments_rename,
    )

    created_on = models.DateTimeField(
        auto_now = True,
        db_index = True,
    )

    start_date = models.DateField(
        null = True,
        blank = True,
        db_index = True,
    )

    frequency = models.IntegerField(
        null = True,
        blank = True,
        choices = products_constant.INVOICE_FREQUENCY
    )

    repeat_for = models.IntegerField(
        null = True,
        blank = True,
        db_index = True,
    )

    subtotal = models.IntegerField(
        default = 0,
        db_index = True,
    )

    subtotal_inc_tax = models.IntegerField(
        default = 0,
        db_index = True,
    )

    total = models.IntegerField(
        default = 0,
        db_index = True,
    )


    class Meta:
        verbose_name_plural = 'invoice_tbl'


#======================================================================================
# PRODUCTS LISTED IN INVOICE
#======================================================================================
#
class InvoiceProducts(models.Model):

    invoice = models.ForeignKey(
        InvoiceModel,
        db_index = True,
        blank = True,
        null = True,
        on_delete = models.CASCADE,
    )        

    product = models.ForeignKey(
        ProductsModel,
        on_delete = models.SET_NULL,
        db_index = True,
        blank = True,
        null = True,
    )

    inventory = models.ForeignKey(
        InventoryProduct,
        on_delete = models.SET_NULL,
        db_index = True,
        null = True,
        blank = True,
    )

    quantity = models.IntegerField(
        db_index = True,
        null = True,
        blank = True,
    )

    class Meta:
        verbose_name_plural = 'invoice_product_tbl'


