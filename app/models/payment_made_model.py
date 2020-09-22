from django.db import models
from django.contrib.auth.models import User

from app.models.users_model import *
# from app.models.products_model import *
from app.models.purchasentry_model import *
from app.models.expense_model import *
from app.models.contacts_model import *
from app.other_constants import payment_constants

from uuid import uuid4
import os

#**************************************************************************
#   PURCHASE_ENTRY DATA
#**************************************************************************

class PurchasePayment(models.Model):

    TYPE = (
        ('off', 'off'),
        ('on', 'on'),
    )

    SAVE_TYPES = (
        (1, 'save_close'),
        (2, 'save_draft'),
    )

    user = models.ForeignKey(User, on_delete = models.CASCADE, db_index = True, null = True,)

    purchase_entry_reference = models.ForeignKey(
        PurchaseEntry,
        on_delete = models.SET_NULL, 
        db_index = True,
        null = True,
        blank = True,
    )

    expense = models.ForeignKey(
        Expense,
        on_delete = models.SET_NULL, 
        db_index = True,
        null = True,
        blank = True,
    )

    account = models.ForeignKey(
        AccGroups,
        on_delete = models.SET_NULL,
        db_index = True,
        blank = True,
        null = True,
    )

    vendor = models.ForeignKey(
        Contacts, 
        on_delete = models.SET_NULL, 
        db_index = True,
        null = True,
        blank = True,
    )

    payment_number = models.CharField(
        max_length = 100,
        db_index = True,
        blank=True,
        null=True,
    ) 

    payment_number_check = models.CharField(
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

    payment_date = models.DateField(
        auto_now=False,
        auto_now_add=False, 
        db_index = True,
        blank= True,
        null= True,
    )

    payment_reference = models.CharField(
        db_index = True,
        max_length=100,
        blank = True,
        null=True
    )

    payment_mode = models.IntegerField(
        db_index = True,
        blank=True,
        null=True,
        choices = payment_constants.PAYMENT_TYPE,
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

    Amount = models.CharField(
        max_length=20,
        db_index = True,
        blank = True,
        null = True,
    )
    
    def __str__(self):
        return "{} - {}".format(self.vendor,self.id) 

    class Meta:
        verbose_name_plural = 'payment_made_tbl'