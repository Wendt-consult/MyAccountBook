from django.db import models
from django.contrib.auth.models import User
# from app.other_constants import state_list
from django.db.models.signals import post_save
from django.dispatch import receiver

from app.models.users_model import *

from app.other_constants import customize_list,user_constants

from uuid import uuid4
import os

#=========================================================================================
# customize module name
#=========================================================================================
#
class CustomizeModuleName(models.Model):

    user = models.ForeignKey(
        User,
        db_index = True,
        on_delete = models.CASCADE,
        null = True,
        blank = True,
    )

    customize_name = models.IntegerField(
        db_index=True,
        choices=customize_list.customize_name,
        null=True,
        blank=True,
    )
    

    def __str__(self):
        return "{} - ({})".format(self.user,self.customize_name) 

#=========================================================================================
# customize contact names
#=========================================================================================
#
class CustomizeContactView(models.Model):

    customize_view_name = models.ForeignKey(
        CustomizeModuleName,
        on_delete=models.CASCADE,
        null = False,
        blank = False,
    )

    contact_name = models.IntegerField(
        db_index = True,
        choices = user_constants.IS_NUM_CHOICE,
        default = 0,
        null = True,
        blank = True,
    )

    contact_org_name = models.IntegerField(
        db_index = True,
        choices = user_constants.IS_NUM_CHOICE,
        default = 0,
        null = True,
        blank = True,
    )

    contact_email = models.IntegerField(
        db_index = True,
        choices = user_constants.IS_NUM_CHOICE,
        default = 0,
        null = True,
        blank = True,
    )

    contact_phone = models.IntegerField(
        db_index = True,
        choices = user_constants.IS_NUM_CHOICE,
        default = 0,
        null = True,
        blank = True,
    )

#=========================================================================================
# customize product names
#=========================================================================================
#

class CustomizeProductView(models.Model):

    customize_view_name = models.ForeignKey(
        CustomizeModuleName,
        on_delete=models.CASCADE,
        null = False,
        blank = False,
    )

    product_sku = models.IntegerField(
        db_index = True,
        choices = user_constants.IS_NUM_CHOICE,
        default = 0,
        null = True,
        blank = True,
    )

    product_type = models.IntegerField(
        db_index = True,
        choices = user_constants.IS_NUM_CHOICE,
        default = 0,
        null = True,
        blank = True,
    )

    product_name = models.IntegerField(
        db_index = True,
        choices = user_constants.IS_NUM_CHOICE,
        default = 0,
        null = True,
        blank = True,
    )

    product_hsn = models.IntegerField(
        db_index = True,
        choices = user_constants.IS_NUM_CHOICE,
        default = 0,
        null = True,
        blank = True,
    )

    product_description = models.IntegerField(
        db_index = True,
        choices = user_constants.IS_NUM_CHOICE,
        default = 0,
        null = True,
        blank = True,
    )

    product_selling_price = models.IntegerField(
        db_index = True,
        choices = user_constants.IS_NUM_CHOICE,
        default = 0,
        null = True,
        blank = True,
    )

    product_Purchase_price = models.IntegerField(
        db_index = True,
        choices = user_constants.IS_NUM_CHOICE,
        default = 0,
        null = True,
        blank = True,
    )

#=========================================================================================
# customize credit_note names
#=========================================================================================
#

class CustomizeCreditView(models.Model):

    customize_view_name = models.ForeignKey(
        CustomizeModuleName,
        on_delete=models.CASCADE,
        null = False,
        blank = False,
    )

    credit_note = models.IntegerField(
        db_index = True,
        choices = user_constants.IS_NUM_CHOICE,
        default = 0,
        null = True,
        blank = True,
    )

    credit_name = models.IntegerField(
        db_index = True,
        choices = user_constants.IS_NUM_CHOICE,
        default = 0,
        null = True,
        blank = True,
    )

    credit_reference = models.IntegerField(
        db_index = True,
        choices = user_constants.IS_NUM_CHOICE,
        default = 0,
        null = True,
        blank = True,
    )

    credit_date = models.IntegerField(
        db_index = True,
        choices = user_constants.IS_NUM_CHOICE,
        default = 0,
        null = True,
        blank = True,
    )

    credit_amount = models.IntegerField(
        db_index = True,
        choices = user_constants.IS_NUM_CHOICE,
        default = 0,
        null = True,
        blank = True,
    )

#=========================================================================================
# customize purchase order names
#=========================================================================================
#

class CustomizePurchaseView(models.Model):

    customize_view_name = models.ForeignKey(
        CustomizeModuleName,
        on_delete=models.CASCADE,
        null = False,
        blank = False,
    )

    purchase_number = models.IntegerField(
        db_index = True,
        choices = user_constants.IS_NUM_CHOICE,
        default = 0,
        null = True,
        blank = True,
    )

    purchase_reference = models.IntegerField(
        db_index = True,
        choices = user_constants.IS_NUM_CHOICE,
        default = 0,
        null = True,
        blank = True,
    )

    purchase_vendor = models.IntegerField(
        db_index = True,
        choices = user_constants.IS_NUM_CHOICE,
        default = 0,
        null = True,
        blank = True,
    )

    purchase_status = models.IntegerField(
        db_index = True,
        choices = user_constants.IS_NUM_CHOICE,
        default = 0,
        null = True,
        blank = True,
    )

    purchase_total = models.IntegerField(
        db_index = True,
        choices = user_constants.IS_NUM_CHOICE,
        default = 0,
        null = True,
        blank = True,
    )

    purchase_date = models.IntegerField(
        db_index = True,
        choices = user_constants.IS_NUM_CHOICE,
        default = 0,
        null = True,
        blank = True,
    )
#=========================================================================================
# customize purchase order names
#=========================================================================================
#
class CustomizeExpenseView(models.Model):

    customize_view_name = models.ForeignKey(
        CustomizeModuleName,
        on_delete=models.CASCADE,
        null = False,
        blank = False,
    )

    
    expense_vocher = models.IntegerField(
        db_index = True,
        choices = user_constants.IS_NUM_CHOICE,
        default = 0,
        null = True,
        blank = True,
    )

    expense_date = models.IntegerField(
        db_index = True,
        choices = user_constants.IS_NUM_CHOICE,
        default = 0,
        null = True,
        blank = True,
    )

    expense_vendor = models.IntegerField(
        db_index = True,
        choices = user_constants.IS_NUM_CHOICE,
        default = 0,
        null = True,
        blank = True,
    )

    expense_payment = models.IntegerField(
        db_index = True,
        choices = user_constants.IS_NUM_CHOICE,
        default = 0,
        null = True,
        blank = True,
    )

    expense_method = models.IntegerField(
        db_index = True,
        choices = user_constants.IS_NUM_CHOICE,
        default = 0,
        null = True,
        blank = True,
    )

    expense_amount = models.IntegerField(
        db_index = True,
        choices = user_constants.IS_NUM_CHOICE,
        default = 0,
        null = True,
        blank = True,
    )

#=========================================================================================
# customize invoice order names
#=========================================================================================
#

class CustomizeInvoiceView(models.Model):

    customize_view_name = models.ForeignKey(
        CustomizeModuleName,
        on_delete=models.CASCADE,
        null = False,
        blank = False,
    )

    invoice_number = models.IntegerField(
        db_index = True,
        choices = user_constants.IS_NUM_CHOICE,
        default = 0,
        null = True,
        blank = True,
    )

    invoice_customer = models.IntegerField(
        db_index = True,
        choices = user_constants.IS_NUM_CHOICE,
        default = 0,
        null = True,
        blank = True,
    )

    invoice_date = models.IntegerField(
        db_index = True,
        choices = user_constants.IS_NUM_CHOICE,
        default = 0,
        null = True,
        blank = True,
    )

    invoice_due_date = models.IntegerField(
        db_index = True,
        choices = user_constants.IS_NUM_CHOICE,
        default = 0,
        null = True,
        blank = True,
    )

    invoice_status = models.IntegerField(
        db_index = True,
        choices = user_constants.IS_NUM_CHOICE,
        default = 0,
        null = True,
        blank = True,
    )

    invoice_amount = models.IntegerField(
        db_index = True,
        choices = user_constants.IS_NUM_CHOICE,
        default = 0,
        null = True,
        blank = True,
    )