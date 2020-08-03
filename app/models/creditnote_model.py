from django.db import models
from django.contrib.auth.models import User
from app.other_constants import state_list
from django.db.models.signals import post_save
from django.dispatch import receiver

from app.models.users_model import *
from app.models.products_model import *
from app.models.contacts_model import *
from app.models.invoice_model import *
from uuid import uuid4
import os

#==========================================================================
#   CHANGE PRODUCT FILE NAMES
#==========================================================================
#
def attachments_rename(instance, filename):

    upload_path = 'creditnotes'
    return  os.path.join(upload_path,'{}/{}'.format(uuid4().hex, filename))

#**************************************************************************
#   CREDITNOTE'S DATA
#**************************************************************************
class CreditNode(models.Model):
    
    SAVE_TYPES = (
        (1, 'save_send'),
        (2, 'save_close'),
        (3, 'save_draft'),
    )

    CREDIT_TYPE = (
        ('off', 'off'),
        ('on', 'on'),
    )

    user = models.ForeignKey(User, on_delete = models.CASCADE, db_index = True, null = True,)

    contact_name = models.ForeignKey(
        Contacts, 
        on_delete = models.SET_NULL, 
        db_index = True,
        null = True,
        blank = True,
    )

    save_type = models.IntegerField(        
        db_index = True,
        default = 2,
        choices = SAVE_TYPES,
    )

    email = models.CharField(
        max_length = 500,
        blank = True,
        null = True,
    )
    cc_email =  models.CharField(
        max_length = 500,
        blank = True,
        null = True,
    )

    billing_address = models.CharField(
        max_length = 500,
        db_index = True,
        blank=True,
        null=True,
    )

    credit_date = models.DateField(
        auto_now=False,
        auto_now_add=False, 
        db_index = True,
        blank= False,
        null= False,
    )

    state_supply = models.CharField(
        max_length = 100,
        db_index = True,
        blank=True,
        null=True,
    )

    invoice_refrence = models.CharField(
        db_index = True,
        max_length=100,
        blank = True,
        null=True
    )
    credit_number = models.CharField(
        max_length = 100,
        db_index = True,
        blank=True,
        null=True,

    ) 

    creditnote_number_check = models.CharField(
        db_index = True,
        max_length=4,
        default = 'off',
        choices = CREDIT_TYPE,
    )

    amount = models.CharField(
        db_index = True,
        max_length=10,
        blank = True,
        null=True
    )

    description =  models.CharField(
        db_index = True,
        max_length=400,
        blank = True,
        null=True
    )

    terms_and_condition = models.CharField(
        max_length = 400,
        blank = True, 
        null = True, 
        db_index = True,
    )

    Note = models.CharField(
        max_length = 400,
        blank = True, 
        null = True, 
        db_index = True,
    )

    attachements = models.FileField(
        upload_to = attachments_rename,
        db_index = True,
        blank = True,
        null = True,
    )

    sub_total = models.CharField(
        default = 0.0,
        max_length=20,
        db_index = True,
        blank = True,
        null = True,
    )
    cgst_5 = models.CharField(
        max_length=30,
        db_index = True,
        blank = True,
        null = True,
    )

    igst_5 = models.CharField(
        max_length=30,
        db_index = True,
        blank = True,
        null = True,
    )

    sgst_5 = models.CharField(
        max_length=30,
        db_index = True,
        blank = True,
        null = True,
    )

    cgst_12 = models.CharField(
        max_length=30,
        db_index = True,
        blank = True,
        null = True,
    )

    igst_12 = models.CharField(
        max_length=30,
        db_index = True,
        blank = True,
        null = True,
    )

    sgst_12 = models.CharField(
        max_length=30,
        db_index = True,
        blank = True,
        null = True,
    )

    cgst_18 = models.CharField(
        max_length=30,
        db_index = True,
        blank = True,
        null = True,
    )

    igst_18 = models.CharField(
        max_length=30,
        db_index = True,
        blank = True,
        null = True,
    )

    sgst_18 = models.CharField(
        max_length=30,
        db_index = True,
        blank = True,
        null = True,
    )

    cgst_28 = models.CharField(
        max_length=30,
        db_index = True,
        blank = True,
        null = True,
    )

    igst_28 = models.CharField(
        max_length=30,
        db_index = True,
        blank = True,
        null = True,
    )

    sgst_28 = models.CharField(
        max_length=30,
        db_index = True,
        blank = True,
        null = True,
    )

    cgst_other = models.CharField(
        max_length=30,
        db_index = True,
        blank = True,
        null = True,
    )

    igst_other = models.CharField(
        max_length=30,
        db_index = True,
        blank = True,
        null = True,
    )

    sgst_other = models.CharField(
        max_length=30,
        db_index = True,
        blank = True,
        null = True,
    )
    total = models.CharField(
        max_length=30,
        db_index = True,
        blank = True,
        null = True,
    )

    creditnote_org_gst_num = models.CharField(
        max_length=30,
        db_index = True,
        blank = True,
        null = True,
    )

    creditnote_org_gst_type =  models.CharField(
        max_length=2,
        db_index = True,
        blank = True,
        null = True,
    )

    creditnote_org_gst_state =  models.CharField(
        max_length=5,
        db_index = True,
        blank = True,
        null = True,
    )

    def __str__(self):
        return "{} - {}".format(self.contact_name,self.id) 

    class Meta:
        verbose_name_plural = 'creditnote_tbl'
#**************************************************************************
#   ADD ITEM'S DATA
#**************************************************************************

class creditnote_Items(models.Model):       

    user = models.ForeignKey(User, on_delete = models.CASCADE, db_index = True, null = True,)

    credit_inventory = models.ForeignKey(
        CreditNode,
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

    description =  models.CharField(
        db_index = True,
        max_length=250,
        blank = True,
        null=True
    )

    product_type = models.CharField(
        max_length = 10,
        db_index = True,
        blank = True,
        null = True,
    )

    # currency =  models.CharField(
    #     max_length=10,
    #     db_index = True,
    #     blank = True,
    #     null = True,
    # )

    price = models.CharField(
        max_length=50,
        db_index = True,
        blank = True,
        null = True,
    )

    unit = models.CharField(
        max_length=100,
        db_index = True,
        blank = True,
        null = True,
    )

    quantity = models.CharField(
        max_length=10,
        db_index = True,
        blank = True,
        null = True,
    )

    discount_type = models.CharField(
        max_length=10,
        db_index = True,
        blank = True,
        null = True,
    )

    discount = models.CharField(
        max_length=11,
        db_index = True,
        blank = True,
        null = True,
    )

    tax = models.CharField(
        max_length=11,
        db_index = True,
        blank = True,
        null = True,
    )

    tax_amount = models.CharField(
        max_length=11,
        db_index = True,
        blank = True,
        null = True,
    )

    cgst_amount = models.CharField(
        max_length=11,
        db_index = True,
        blank = True,
        null = True,
    )

    sgst_amount = models.CharField(
        max_length=11,
        db_index = True,
        blank = True,
        null = True,
    )

    igst_amount = models.CharField(
        max_length=11,
        db_index = True,
        blank = True,
        null = True,
    )

    amount = models.CharField(
        max_length=11,
        db_index = True,
        blank = True,
        null = True,
    )

    
    def __str__(self):
        return "{} ({})".format(self.credit_inventory,self.product) 

    class Meta:
        verbose_name_plural = 'creditnote_item_tbl'