from django.db import models
from django.contrib.auth.models import User
# from app.other_constants import state_list
from django.db.models.signals import post_save
from django.dispatch import receiver

from app.models.users_model import *
from app.models.products_model import *
from app.models.contacts_model import *
from app.other_constants import payment_constants
# from app.models.invoice_model import *
from uuid import uuid4
import os


#**************************************************************************
#   PURCHASE_ORDER DATA
#**************************************************************************
class PurchaseOrder(models.Model):
    
    TYPE = (
        ('off', 'off'),
        ('on', 'on'),
    )

    SAVE_TYPES = (
        (1, 'save_send'),
        (2, 'save_close'),
        (3, 'save_draft'),
        (4, 'save_print'),
    )

    user = models.ForeignKey(User, on_delete = models.CASCADE, db_index = True, null = True,)

    vendor = models.ForeignKey(
        Contacts, 
        on_delete = models.SET_NULL, 
        db_index = True,
        null = True,
        blank = True,
    )

    purchase_order_number = models.CharField(
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
        default = 2,
        choices = SAVE_TYPES,
    )

    purchase_order_date = models.DateField(
        auto_now=False,
        auto_now_add=False, 
        db_index = True,
        blank= False,
        null= False,
    )

    purchase_delivery_date = models.DateField(
        auto_now=False,
        auto_now_add=False, 
        db_index = True,
        blank= False,
        null= False,
    )

    purchase_status =  models.IntegerField(
        default = 0,
        db_index = True,
        blank = True,
        null = True,
        choices = payment_constants.purchse_status
    )

    purchase_refrence = models.CharField(
        db_index = True,
        max_length=100,
        blank = True,
        null=True
    )

    delivery_address = models.CharField(
        max_length = 500,
        db_index = True,
        blank=True,
        null=True,
    )

    delivery_state = models.CharField(
        max_length = 10,
        db_index = True,
        blank=True,
        null=True,
    )

    is_organisation_delivary = models.CharField(
        db_index = True,
        max_length=4,
        default = 'off',
        choices = TYPE,
    )

    is_customer_delivary = models.CharField(
        db_index = True,
        max_length=4,
        default = 'off',
        choices = TYPE,
    )

    customer =  models.CharField(
        max_length=10,
        db_index = True,
        null = True,
        blank = True,
    )

    attention = models.CharField(
        db_index = True,
        max_length=100,
        blank = True,
        null=True
    )

    country_code = models.CharField(
        max_length=10,
        db_index = True,
        blank = True,
        null=True
    )
    
    contact_number = models.CharField(
        max_length=10,
        db_index = True,
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

    total_amount = models.CharField(
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

    total_balance = models.CharField(
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

    advance_payment_date = models.DateField(
        auto_now=False,
        auto_now_add=False, 
        db_index = True,
        blank= True,
        null= True,
    )

    advacne_payment_method = models.CharField(
        db_index = True,
        max_length=5,
        choices = payment_constants.PAYMENT_TYPE,
        null = True,
        blank = True,
    )

    advacne_note = models.TextField(
        blank = True,
        null = True,
    )

    def __str__(self):
        return "{} - {}".format(self.vendor,self.id) 

    class Meta:
        verbose_name_plural = 'purchase_order_tbl'
#**************************************************************************
#   PURCHASE ORDER ADVANCE TABLE
#**************************************************************************


#**************************************************************************
#   ADD PURCHASE_ORDER ITEM'S DATA
#**************************************************************************

class Purchase_Items(models.Model):       

    user = models.ForeignKey(User, on_delete = models.CASCADE, db_index = True, null = True,)

    purchase_item_list = models.ForeignKey(
        PurchaseOrder,
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

    
    def __str__(self):
        return "{} ({})".format(self.purchase_item_list,self.product) 

    class Meta:
        verbose_name_plural = 'puchase_items_tbl'