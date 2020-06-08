from django.views import View

from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from django.http import HttpResponse

from app.other_constants import *
from app.models import *

from django.contrib.auth.decorators import user_passes_test

from collections import defaultdict 

from django.db import models, connection


#************************************************************************************
# DATABASE OPERATIONS PAGE
#************************************************************************************
#

def get_db_layouts_details(model_name=None):
    if model_name:
        return 

#
#
#

def truncate_table(cls_ins = None):
    try:
        cls_ins.truncate()        
    except:
        # use for sqlite
        cls_ins.objects.all().delete()
        cls_ins.reset_sqlite_autoinc()
        

#
# Major Heads Data Load

def major_heads_initial_load(update = True):
    
    if update:
        for id, m_head in accounts_constant.LEDGER_ACCOUNT_DICT.items():
            
            try:
                acc = accounts_model.MajorHeads.objects.get(pk = int(id))
                
                acc.major_head_name = m_head
                acc.save()
            except:
                acc = accounts_model.MajorHeads(
                    pk = int(id),
                    major_head_name = m_head
                )
                acc.save()
    else:
        
        truncate_table(cls_ins = accounts_model.MajorHeads)
        
        for id, m_head in accounts_constant.LEDGER_ACCOUNT_DICT.items():
            acc = accounts_model.MajorHeads(
                    pk = int(id),
                    major_head_name = m_head
                )
            acc.save()
            
    return True


#
#
#

def major_heads_groups_initial_load(request):
    
    truncate_table(cls_ins = accounts_model.AccGroups)
    
    acc = accounts_model.MajorHeads.objects.all()
    
    for i in acc:
        
        for id, grp_name in accounts_constant.ACCOUNTS_LEDGER_GROUPS_DICT[i.id].items():
        
            print(id, grp_name)
        
            grp = accounts_model.AccGroups(
                user = request.user,
                major_head = i,
                is_standard = True,
                group_name = grp_name,
                group_info = grp_name+" "+"Info",
            )
            
            grp.save()
        
    
#
#
#
def load_initial_data(request):
    
    
    # Use for update and insert 
    
    major_heads_initial_load(False)    
    major_heads_groups_initial_load(request)        
    
        
    #
    # Standard Acc Gropus 
    
    # Use for truncate 
    # accounts_model.AccGroups.objects..truncate()
    
    
    return HttpResponse('')
    
#
#
#

class SettingsView(View):

    # Template 
    template_name = 'app/system/index.html'

    # Initialize 
    data = defaultdict()

    # Custom CSS/JS Files For Inclusion into template
    data["css_files"] = []
    data["js_files"] = []
    data["active_link"] = 'Settings - DB Operations'

    data["included_template"] = 'app/system/view_settings.html'
 

    def get(self, request):
    
        
    
        return render(request, self.template_name, self.data)
    
    def post(self, request):
        pass

class DatabaseOperations(View):
    pass