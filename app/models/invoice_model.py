from django.db import models
from django.contrib.auth.models import User
# from app.other_constants import state_list
from django.db.models.signals import post_save
from django.dispatch import receiver

from app.models.users_model import *
from app.models.products_model import *
from app.models.contacts_model import *
from app.models.purchase_model import *
from app.other_constants import payment_constants
from app.other_constants.user_constants import *
# from app.models.invoice_model import *
from uuid import uuid4
import os


#**************************************************************************
#   PURCHASE_ORDER DATA
#**************************************************************************
class InvoiceModel(models.Model):
    
    TYPE = (
        ('off', 'off'),
        ('on', 'on'),
    )

    SAVE_TYPES = (
        (1, 'save_send'),
        (2, 'save_close'),
        (3, 'save_draft'),
        (4, 'save_print'),
        (5, 'save_new'),
    )

    user = models.ForeignKey(User, on_delete = models.CASCADE, db_index = True, null = True,)

    invoice_customer = models.ForeignKey(
        Contacts, 
        on_delete = models.SET_NULL, 
        db_index = True,
        null = True,
        blank = True,
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

    purchase_order_number = models.CharField(
        max_length = 100,
        db_index = True,
        blank=True,
        null=True,
    ) 

    invoice_number = models.CharField(
        max_length = 100,
        db_index = True,
        blank=True,
        null=True,
    ) 

    invoice_check = models.CharField(
        db_index = True,
        max_length=4,
        default = 'off',
        choices = TYPE,
        blank=True,
        null=True,
    )

    save_type = models.IntegerField(        
        db_index = True,
        default = 2,
        choices = SAVE_TYPES,
    )

    invoice_date = models.DateField(
        auto_now=False,
        auto_now_add=False, 
        db_index = True,
        blank= False,
        null= False,
    )

    invoice_type_new = models.CharField(
        db_index = True,
        max_length=4,
        default = 'off',
        choices = TYPE,
    )

    invoice_type_recurring = models.CharField(
        db_index = True,
        max_length=4,
        default = 'off',
        choices = TYPE,
    )

    invoice_new_pay_terms = models.CharField(
        max_length = 100,
        db_index = True,
        blank=True,
        null=True,
    ) 

    invoice_new_due_date = models.DateField(
        auto_now=False,
        auto_now_add=False, 
        db_index = True,
        blank= True,
        null= True,
    )

    invoice_recurring_start_date = models.DateField(
        auto_now=False,
        auto_now_add=False, 
        db_index = True,
        blank= True,
        null= True,
    )

    invoice_recurring_count = models.IntegerField(
        default=0,
        db_index = True,
        blank=True,
        null=True,
    )

    invoice_recurring_end_date = models.DateField(
        auto_now=False,
        auto_now_add=False, 
        db_index = True,
        blank= True,
        null= True,
    )

    invoice_recurring_repeat = models.IntegerField(
        db_index = True,
        blank=True,
        null=True,
    ) 

    invoice_recurring_frequency = models.CharField(
        max_length = 100,
        db_index = True,
        blank=True,
        null=True,
    ) 

    invoice_recurring_advance = models.CharField(
        max_length=15,
        db_index = True,
        blank=True,
        null=True,
    )

    invoice_recurring_pay = models.CharField(
        max_length=50,
        db_index = True,
        blank=True,
        null=True,
    )

    invoice_salesperson =  models.CharField(
        max_length=10,
        db_index = True,
        null = True,
        blank = True,
    )

    invoice_state_supply = models.CharField(
        max_length=15,
        db_index = True,
        null = True,
        blank = True,
    )

    invoice_status =  models.IntegerField(
        default = 0,
        db_index = True,
        blank = True,
        null = True,
        choices = payment_constants.PAYMENT_STATUS
    )
    inovice_over_due_count = models.IntegerField(
        default = 0,
        db_index = True,
        blank = True,
        null = True,
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
        max_length=20,
        db_index = True,
        blank = True,
        null = True,
    )

    total_discount = models.CharField(
        max_length=20,
        db_index = True,
        blank = True,
        null = True,
    )

    shipping_charges = models.CharField(
        max_length=20,
        db_index = True,
        blank = True,
        null = True,
    )

    total_amount = models.CharField(
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

    is_cs_gst = models.BooleanField(
        db_index = True,
        choices = user_constants.IS_TRUE,
        default = True,
        blank = True,
        null = True,
    )

    cgst = models.CharField(
        max_length=30,
        db_index = True,
        blank = True,
        null = True,
    )

    sgst= models.CharField(
        max_length=30,
        db_index = True,
        blank = True,
        null = True,
    )

    igst= models.CharField(
        max_length=30,
        db_index = True,
        blank = True,
        null = True,
    )

    invoice_org_gst_num = models.CharField(
        max_length=30,
        db_index = True,
        blank = True,
        null = True,
    )

    invoice_org_gst_type =  models.CharField(
        max_length=2,
        db_index = True,
        blank = True,
        null = True,
    )

    invoice_org_gst_state =  models.CharField(
        max_length=5,
        db_index = True,
        blank = True,
        null = True,
    )

    invoice_delete_status = models.IntegerField(
        db_index = True,
        default=0,
        blank = False,
        null = False,
    )    
    def __str__(self):
        return "{} - {}".format(self.invoice_customer,self.id) 

    class Meta:
        verbose_name_plural = 'invoice_tbl'

#**************************************************************************
#   ADD INVOICE ITEM'S DATA
#**************************************************************************

class Invoice_Line_Items(models.Model):       

    user = models.ForeignKey(User, on_delete = models.CASCADE, db_index = True, null = True,)

    invoice_item_list = models.ForeignKey(
        InvoiceModel,
        db_index = True,
        blank = True,
        null = True,
        on_delete = models.CASCADE,
    ) 

    is_header = models.BooleanField(
        db_index = True,
        choices = user_constants.IS_TRUE,
        default = True,
        blank = True,
        null = True,
    )

    header_name = models.CharField(
        db_index = True,
        max_length=250,
        blank = True,
        null=True
    )
    
    header_number_count = models.CharField(
        db_index = True,
        max_length=10,
        blank = True,
        null=True
    )

    header_subtotal = models.CharField(
        db_index = True,
        max_length=15,
        blank = True,
        null=True
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

    account = models.ForeignKey(
        AccGroups,
        on_delete = models.SET_NULL,
        db_index = True,
        blank = True,
        null = True,
    )

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

    amount_inc = models.CharField(
        max_length=11,
        db_index = True,
        blank = True,
        null = True,
    )

    
    def __str__(self):
        return "{} ({})".format(self.invoice_item_list,self.product) 

    class Meta:
        verbose_name_plural = 'invoice_items_tbl'