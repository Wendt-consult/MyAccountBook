from django.db import models
from django.contrib.auth.models import User
from app.models.contacts_model import Contacts
from app.other_constants import *
  
#=====================================================================
# MULTIPLE COLLECTION METHODS
#=====================================================================
class Collections(models.Model):

    user = models.ForeignKey(
        User,
        on_delete = models.SET_NULL,
        db_index = True,
        blank = True,
        null = True,
    )

    contact = models.ForeignKey(
        Contacts,
        on_delete = models.SET_NULL,
        db_index = True,
        blank = True,
        null = True,
    )

    collection_due_date = models.DateTimeField(
        null = True,
        blank = True,
        db_index = True,
    )

    amount = models.FloatField(
        blank = True,
        null = True,
        db_index = True,
    )

    currency_type = models.CharField(
        max_length = 5,
        db_index = True,
        choices = currency_list.CURRENCY_CHOICES,
    )

    payment_type = models.IntegerField(
        default = 1,
        db_index = True,
        choices = payment_constants.PAYMENT_TYPE,
    )

    collection_status = models.IntegerField(
        default = 1,
        db_index = True,
        choices = payment_constants.COLLECTION_STATUS,
    )

    collection_date = models.DateTimeField(
        null = True,
        blank = True,
        db_index = True,
    )

    created_on = models.DateTimeField(
        db_index = True,
        auto_now_add = True,
        auto_now = False,
    )

    def __str__(self):
        if self.contact is not None:
            return self.contact.contact_name
        else:
            return 'Contact Deleted'
#===================================================================================
#   COLLECT PARTIAL MODEL
#===================================================================================
#
class CollectPartial(models.Model):
    
    user = models.ForeignKey(
        User,
        on_delete = models.SET_NULL,
        db_index = True,
        blank = True,
        null = True,
    )

    collect_part = models.ForeignKey(
        Collections,
        on_delete = models.CASCADE,
        db_index = True,
        null = True,
        blank = True,
    )

    collection_due_date = models.DateTimeField(
        null = True,
        blank = True,
        db_index = True,
    )

    amount = models.FloatField(
        blank = True,
        null = True,
        db_index = True,
    )

    currency_type = models.CharField(
        max_length = 5,
        db_index = True,
        choices = currency_list.CURRENCY_CHOICES,
    )

    payment_type = models.IntegerField(
        default = 1,
        db_index = True,
        choices = payment_constants.PAYMENT_TYPE,
    )

    collection_status = models.IntegerField(
        default = 1,
        db_index = True,
        choices = payment_constants.PARTIAL_COLLECTION_STATUS,
    )

    collection_date = models.DateTimeField(
        null = True,
        blank = True,
        db_index = True,
    )

    created_on = models.DateTimeField(
        db_index = True,
        auto_now_add = True,
        auto_now = False,
    )
    