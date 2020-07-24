from django.db import models
from django.contrib.auth.models import User
from app.other_constants import *
from django.db.models.signals import post_save
from django.dispatch import receiver

from uuid import uuid4
import os

#==========================================================================
#   CHANGE CSV IMPORT FILE NAMES
#==========================================================================
#
def file_rename(instance, filename):

    upload_path = 'contact_csv_imports'
    ext = filename.split('.')[-1]
    return  os.path.join(upload_path,'{}.{}'.format(uuid4().hex, ext))


#==========================================================================
#   CHANGE CSV IMPORT FILE NAMES
#==========================================================================
#
def attachments_rename(instance, filename):

    upload_path = 'contact_attachments'
    ext = filename.split('.')[-1]
    return  os.path.join(upload_path,'{}.{}'.format(uuid4().hex, ext))



#**************************************************************************
#   CONTACT'S DATA
#**************************************************************************
class Contacts(models.Model):

    user = models.ForeignKey(User, on_delete = models.CASCADE, db_index = True, null = True,)

    app_id = models.CharField(
        max_length = 30,
        db_index = True,
        blank = True,
        null = True,
    )

    is_imported_user = models.BooleanField(
        default = False,
        db_index = True,
        choices = user_constants.IS_TRUE,
        blank = True,
    )

    imported_user = models.ForeignKey(
        User,
        related_name = 'imported_user',
        db_index = True,
        blank = True,
        null = True,
        on_delete = models.SET_NULL,
    )

    customer_type = models.IntegerField(
        db_index = True,
        choices = user_constants.CUSTOMER_TYPE,
        default = 1,
        null = True,
        blank = True,
    )

    contact_delete_status = models.IntegerField(
        db_index = True,
        default = 0,
        null = False,
        blank = False,
    )
    is_sub_customer = models.IntegerField(
        choices = user_constants.IS_SUB_CUSTOMER,
        default = 1,
        db_index = True,
        null = True,
        blank = True,
    )

    salutation = models.IntegerField(
        db_index = True,
        default = 0,
        choices = user_constants.SALUTATIONS,
    )

    contact_name = models.CharField(
        max_length = 250,
        blank = False,
        null = False,
        db_index = True,
    )

    display_name = models.CharField(
        max_length = 250,
        blank = True,
        null = True,
        db_index = True,
    )

    organization_type = models.IntegerField(
        db_index = True,
        choices = user_constants.ORGANIZATION_TYPE,
        default = 1,
    )

    organization_name = models.CharField(
        max_length = 250,
        db_index = False,
        blank = True,
        null = True,
    )

    is_msme_reg = models.BooleanField(
        db_index = True,
        choices = user_constants.IS_TRUE,
        default = False,
    )

    email = models.EmailField(
        blank = True, 
        null = True, 
        db_index = True,
    )

    phone_country_code = models.IntegerField(
        db_index = True,
        blank = False,
        choices = user_constants.PHONE_COUNTRY_CODE,
        default = 45,
        null = True,
    )    

    phone = models.CharField(
        max_length = 250,
        db_index = True,
        blank = True,
        null = True,
    )

    website = models.CharField(
        max_length = 250,
        db_index = True,
        blank = True,
        null = True,
    )

    facebook = models.CharField(
        blank = True,
        null = True,
        max_length = 250,
    )

    twitter = models.CharField(
        blank = True,
        null = True,
        max_length = 250,
    )

    is_active = models.BooleanField(
        db_index = True,
        choices =  user_constants.IS_TRUE,
        default = True,
    )    

    notes = models.TextField(
        blank = True,
        null = True,
    )

    attachements = models.FileField(
        upload_to = attachments_rename,
        db_index = True,
        blank = True,
        null = True,
    )
    
    created_on = models.DateTimeField(
        auto_now = True,
        db_index = True,
    ) 

    updated_on = models.DateTimeField(
        auto_now = False,
        db_index = True,
        null = True,
    )
    
    def __str__(self):
        if(self.organization_name is None):
            if not self.is_active:
                return "{} (Inactive)".format(self.contact_name) 
            return "{}".format(self.contact_name) 
        else:
            if not self.is_active:
                return "{} - ({}) (Inactive)".format(self.contact_name,self.organization_name) 
            return "{} - ({})".format(self.contact_name,self.organization_name) 
        return self.contact_name.upper()

    def is_active_value(self):
        if self.is_active:
            return "YES"
        return "NO"  

    class Meta:
        verbose_name_plural = 'contacts_tbl'

#===================================================================================
# CONTACTS FILE UPLOAD 
#===================================================================================

class ContactsFileUpload(models.Model):

    user = models.ForeignKey(
        User,
        db_index = True,
        blank = True,
        null = True,
        on_delete = models.CASCADE,
    )

    csv_file = models.FileField(
        upload_to = file_rename,
        db_index = True,
        blank = True,
        null = True,
    )

    created_date = models.DateTimeField(
        auto_now_add = True,
        auto_now = False,
        db_index = True,
    )

    class Meta:
        verbose_name_plural = 'contacts_fileupload_tbl'
    
#=========================================================================================
# DELETE FILES FROM MEDIA ON DELETING A CSV 
#=========================================================================================
#
@receiver(models.signals.post_delete, sender=ContactsFileUpload)
def image_delete(sender, instance, **kwargs):
    instance.csv_file.delete(False)