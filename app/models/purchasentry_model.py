from django.db import models
from django.contrib.auth.models import User
# from django.db.models.signals import post_save
# from django.dispatch import receiver

from app.models.users_model import *
from app.models.products_model import *
from app.models.contacts_model import *
from app.models.purchase_model import *
from app.other_constants import payment_constants

from uuid import uuid4
import os

#**************************************************************************
#   PURCHASE_ENTRY DATA
#**************************************************************************

class PurchaseEntry(models.Model):

    TYPE = (
        ('off', 'off'),
        ('on', 'on'),
    )

    SAVE_TYPES = (
        (1, 'save_close'),
        (2, 'save_draft'),
    )

    user = models.ForeignKey(User, on_delete = models.CASCADE, db_index = True, null = True,)

    vendor = models.ForeignKey(
        Contacts, 
        on_delete = models.SET_NULL, 
        db_index = True,
        null = True,
        blank = True,
    )

    purchase_entry_number = models.CharField(
        max_length = 100,
        db_index = True,
        blank=True,
        null=True,
    ) 

    purchase_number_check = models.CharField(
        db_index = True,
        max_length=4,
        default = 'off',
        choices = TYPE,
        blank=True,
        null=True,
    )

    save_type = models.IntegerField(        
        db_index = True,
        default = 1,
        choices = SAVE_TYPES,
    )

    purchase_entry_date = models.DateField(
        auto_now=False,
        auto_now_add=False, 
        db_index = True,
        blank= False,
        null= False,
    )

    purchase_entry_refrence = models.CharField(
        db_index = True,
        max_length=100,
        blank = True,
        null=True
    )

    purchase_entry_pay_terms = models.CharField(
        max_length = 100,
        db_index = True,
        blank=True,
        null=True,
    ) 

    purchase_entry_due_date = models.DateField(
        auto_now=False,
        auto_now_add=False, 
        db_index = True,
        blank= True,
        null= True,
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

    freight_charges = models.CharField(
        max_length=20,
        db_index = True,
        blank = True,
        null = True,
    )

    advance = models.CharField(
        max_length=20,
        db_index = True,
        blank = True,
        null = True,
    )

    total = models.CharField(
        max_length=20,
        db_index = True,
        blank = True,
        null = True,
    )

    balance_due = models.CharField(
        max_length=20,
        db_index = True,
        blank = True,
        null = True,
    )

    total_balance = models.CharField(
        max_length=20,
        db_index = True,
        blank = True,
        null = True,
    )

    connect_purchase_order = models.CharField(
        max_length=5,
        default= 'NO',
        db_index = True,
        blank = True,
        null = True,
    )

    purchase_order = models.ForeignKey(
        PurchaseOrder,
        on_delete=models.CASCADE,
        db_index = True,
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

    is_cs_gst = models.BooleanField(
        db_index = True,
        choices = user_constants.IS_TRUE,
        default = True,
        blank = True,
        null = True,
    )

    purchase_org_gst_num = models.CharField(
        max_length=30,
        db_index = True,
        blank = True,
        null = True,
    )

    purchase_org_gst_type =  models.CharField(
        max_length=2,
        db_index = True,
        blank = True,
        null = True,
    )

    purchase_org_gst_state =  models.CharField(
        max_length=5,
        db_index = True,
        blank = True,
        null = True,
    )

    purchase_delete_status = models.IntegerField(
        db_index = True,
        default=0,
        blank = False,
        null = False,
    )

    entry_status =  models.IntegerField(
        db_index = True,
        blank = True,
        null = True,
        choices = payment_constants.purchase_entry_status
    )
    
    entry_date_count = models.IntegerField(
        db_index=True,
        default=0,
        blank=True,
        null=True,
    )
    def __str__(self):
        return "{} - {}".format(self.vendor,self.id) 

    class Meta:
        verbose_name_plural = 'purchase_entry_tbl'
#**************************************************************************
#   ADD INVOICE ITEM'S DATA
#**************************************************************************

class PurchaseEntryItems(models.Model):       

    user = models.ForeignKey(User, on_delete = models.CASCADE, db_index = True, null = True,)

    purchase_entry_list = models.ForeignKey(
        PurchaseEntry,
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
        return "{} ({})".format(self.purchase_entry_list,self.product) 

    class Meta:
        verbose_name_plural = 'purchase_entry_items_tbl'