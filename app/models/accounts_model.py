from django.db import models, connection
from django.contrib.auth.models import User
from app.other_constants import *


#
#
#
class MajorHeads(models.Model):
    
    major_head_name = models.CharField(
        max_length = 100,
        unique = True,
    )
    
    is_active = models.BooleanField(
        default = True,
        db_index = True,
        choices = user_constants.IS_TRUE
    )
    
    def __str__(self):
        return self.major_head_name


    @classmethod
    def truncate(cls):
        with connection.cursor() as cursor:
            cursor.execute('TRUNCATE TABLE "{0}" CASCADE'.format(cls._meta.db_table))
            
    @classmethod
    def reset_sqlite_autoinc(cls):
        with connection.cursor() as cursor:
            cursor.execute('UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME="{0}"'.format(cls._meta.db_table))

#
#
#
class AccGroups(models.Model):

    user = models.ForeignKey(
        User,
        db_index = True,
        on_delete = models.CASCADE,
    )

    major_head = models.ForeignKey(      
        MajorHeads,
        on_delete = models.CASCADE,
        db_index = True,
        null = True,
        blank = True,
    )
    
    is_standard = models.BooleanField(
        db_index = True,
        default = True,
        choices = user_constants.IS_TRUE,
    )
    
    group_name = models.CharField(
        max_length = 250,
        blank = True,
        null = True,
    )

    group_info = models.TextField(
        blank = True,
        null = True,
    )

    is_active = models.BooleanField(
        db_index = True,
        default = True,
        choices = user_constants.IS_TRUE,
    )

    def __str__(self):
        return self.group_name

    @classmethod
    def truncate(cls):
        with connection.cursor() as cursor:
            cursor.execute('TRUNCATE TABLE "{0}" CASCADE'.format(cls._meta.db_table))
     
    @classmethod
    def reset_sqlite_autoinc(cls):
        with connection.cursor() as cursor:
            cursor.execute('UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME="{0}"'.format(cls._meta.db_table))    

#
#
#
class AccLedger(models.Model):

    user = models.ForeignKey(
        User,
        db_index = True,
        on_delete = models.CASCADE,
    )

    acc_group = models.CharField(
        max_length = 200,
        db_index = True,
        null = True,
        blank = True,
    ) 

    accounts_name = models.CharField(
        max_length = 250,
        blank = True,
        null = True,
    )

    major_heads = models.ForeignKey(      
        MajorHeads,
        on_delete = models.SET_NULL,
        db_index = True,
        null = True,
        blank = True,
    )

    info_message = models.TextField(
        null = True,
        blank = True,
    )

    description = models.TextField(
        blank = True,
        null = True,
    )

    is_active = models.BooleanField(
        db_index = True,
        default = True,
        choices = user_constants.IS_TRUE,
    )

    def __str__(self):
        return self.accounts_name

