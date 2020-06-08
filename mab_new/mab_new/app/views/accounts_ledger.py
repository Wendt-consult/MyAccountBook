from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse
from django.views import View
from collections import OrderedDict, defaultdict
from django.db.models import Q


from app.models import *
from app.forms import *
from app.other_constants import *

import json

#
#
#
def get_predefined_groups(request):
    
    htm = ['<option value="-----">-----</option>']

    if request.GET:
        # htm.append('<option style="background-color:#913f9e; color:#FFFFFF" value="-1">+ New Group</option>')
        
        acc_group = accounts_model.AccGroups.objects.filter(major_head = int(request.GET["ids"]), is_active = True)
       
        # GET STANDARD GROUPS
        acc_group_standard = acc_group.filter(is_standard = True)
        
        for acc in acc_group_standard:
            htm.append('<option value="{}">{}</option>'.format(acc.id, acc.group_name))
            
        # GET USER SPECIFIC GROUPS
        acc_group_user = acc_group.filter(is_standard = False, user = request.user)
        
        for acc in acc_group_user:
            htm.append('<option value="{}">{}</option>'.format(acc.id, acc.group_name))
    
    
    return HttpResponse(''.join(htm))



#
#
#
class AccLedger(View):
    
    # Template 
    template_name = 'app/app_files/acc_ledger/index.html'

    data = defaultdict()

    data["included_template"] = 'app/app_files/acc_ledger/add_accounts_ledger.html'

    data["css_files"] = []
    data["js_files"] = ['custom_files/js/ledger.js']

    data["active_link"] = 'Accounts'
    
    #
    #
    def get(self, request):

        self.data["ledger_form"] = accounts_ledger_forms.AccLedgerForm()
        self.data["groups_form"] = accounts_ledger_forms.AccGroupsForm()
        return render(request, self.template_name, self.data)

    #
    #
    def post(self, request):
        ledger_form = accounts_ledger_forms.AccLedgerForm(request.POST)

        if ledger_form.is_valid():
            obj = ledger_form.save(commit = False)
            obj.user = request.user
            obj.save()

        return redirect('/ledger/add/', permanent = False) 

#
#
#
def add_ledger_group(request):
    if request.POST:
        groups_form = accounts_ledger_forms.AccGroupsForm(request.POST)
    
        try:
            major_head = accounts_model.MajorHeads.objects.get(pk = int(request.POST["ids"]))
        except:
            return HttpResponse('0')

        if groups_form.is_valid():
            obj = groups_form.save(commit = False)
            obj.user = request.user
            obj.major_head = major_head
            obj.save()

            grp = str(obj.id)
            return HttpResponse(grp)
        return HttpResponse('0')
    return HttpResponse('0')
    
#
#
#
def acc_ledger_info(request,ins,strs):
    account = accounts_model.AccGroups.objects.filter(Q(user = request.user) & Q(major_head = int(ins)) & Q(group_name = strs)).values('group_info')
    data = {'account' : account[0]['group_info']} 
    return JsonResponse(data)

def unique(request,ins,strs):
    unique = accounts_model.AccGroups.objects.filter(Q(user = request.user) & Q(major_head = int(ins)) & Q(group_name = strs))
    if(len(unique) > 0):
        data = {'unique': 1}
        return JsonResponse(data)
    else:
        data = {'unique' : 0}
        return JsonResponse(data)

def unique2(request,ins,strs):
    unique2 = accounts_model.AccLedger.objects.filter(Q(user = request.user) & Q(major_heads = int(ins)) & Q(accounts_name = strs))
    print('aaaaaaaaaa')
    print(unique2)
    if(len(unique2) > 0):
        data = {'unique': 1}
        return JsonResponse(data)
    else:
        data = {'unique' : 0}
        return JsonResponse(data)
        