from django.db import models
from django.contrib.auth.models import User
from app.models.contacts_model import *
from app.models.collects_model import *
from app.models.users_model import *
from app.models.products_model import *

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
#   Journal entry
#**************************************************************************

class JournalEntry(models.Model):

    JOURNAL_TYPE = (
        ('off', 'off'),
        ('on', 'on'),
    )

    SAVE_TYPES = (
        (1, 'save_close'),
        (2, 'save_draft'),
        (3, 'save_downaload'),
    )
    user = models.ForeignKey(User, on_delete = models.CASCADE, db_index = True, null = True,)
    
    journalentry_number = models.CharField(
        max_length = 100,
        db_index = True,
        blank=True,
        null=True,

    ) 

    save_type = models.IntegerField(        
        db_index = True,
        default = 1,
        choices = SAVE_TYPES,
    )

    journalentry_number_check = models.CharField(
        db_index = True,
        max_length=4,
        default = 'off',
        choices = JOURNAL_TYPE,
        
    )          

    journalentry_date = models.DateField(
        auto_now=False,
        auto_now_add=False, 
        db_index = True,
        blank= False,
        null= False,
    )
    journalentry_refrence = models.CharField(
        db_index = True,
        max_length=100,
        blank = True,
        null=True
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

    total_amount_debit = models.CharField(
        max_length=20,
        db_index = True,
        blank = True,
        null = True,
    )

    total_amount_credit = models.CharField(
        max_length=20,
        db_index = True,
        blank = True,
        null = True,
    )

    journal_delete_status = models.IntegerField(
        db_index = True,
        default=0,
        blank = False,
        null = False,
    )
    
    def __str__(self):
        return "{} - {}".format(self.journalentry_number,self.id) 

    class Meta:
        verbose_name_plural = 'journal_entry_tbl'
#**************************************************************************
#   ADD ITEM'S DATA
#**************************************************************************

class JournalEntry_Items(models.Model):   

    user = models.ForeignKey(User, on_delete = models.CASCADE, db_index = True, null = True,)

    journalentry = models.ForeignKey(JournalEntry,
        db_index = True,
        blank = True,
        null = True,
        on_delete = models.CASCADE,    
    )

    accounts_items = models.ForeignKey(
        MajorHeads,
        db_index = True,
        blank = True,
        null = True,
        on_delete = models.CASCADE,
    )

    description =  models.TextField(
        db_index = True,
        max_length=250,
        blank = True,
        null=True
    )

    journal_entry_customer = models.ForeignKey(
        Contacts, 
        on_delete = models.SET_NULL, 
        db_index = True,
        null = True,
        blank = True,
    )

    debit = models.CharField(
        max_length=10,
        db_index = True,
        blank = True,
        null = True,
    )

    credit = models.CharField(
        max_length=10,
        db_index = True,
        blank = True,
        null = True,
    )

    def __str__(self):
        return "{} ({})".format(self.journalentry,self.id) 

    class Meta:
        verbose_name_plural = 'journalentry_items_tbl'