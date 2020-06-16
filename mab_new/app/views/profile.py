from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse
from django.views import View
from collections import OrderedDict, defaultdict
from django.db.models import *
from app.models import *
from app.forms import *
from app.helpers import *

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

class Profile(View):

    # Template 
    template_name = 'app/app_files/profile_manager/index.html'

    # Initialize 
    data = defaultdict()
    data["view"] = ""
    data["contacts"] = {}
    data["active_link"] = 'Profile'
    data["breadcrumb_title"] = 'PROFILE'

    # Custom CSS/JS Files For Inclusion into template
    data["css_files"] = []
    #data["js_files"] = ['all_page/js/echarts/dist/echarts.js', 'custom_files/js/profile_graphs.js']
    data["js_files"] = ['custom_files/js/profile.js', 'custom_files/js/common.js', 'custom_files/js/contacts.js']

    data["included_template"] = 'app/app_files/profile_manager/profile_details.html'

    #
    #
    def get(self, request): 

        #
        # Organisation Form

        organisation_form = None
        self.data["address_details"] = {}

        try:
            organisation_form = users_model.Organisations.objects.get(user = request.user)
            self.data["organisation_form"] = profile_forms.OrganisationForm(instance = organisation_form)
        except:
            self.data["organisation_form"] = profile_forms.OrganisationForm()

        #
        # Organisation Contact Form

        self.data["org_contact_form"] = profile_forms.OrganisationContactForm()
        self.data['ids'] = organisation_form.id

        self.data["description"] = organisation_form.organisation_description
        self.data["organisation_name"] = organisation_form.organisation_name
 
        self.data["logo"] = ""
        if organisation_form.logo:
            self.data["logo"] = organisation_form.logo
        
        #
        # Accounts
        user_accounts = users_model.User_Account_Details.objects.filter(user = request.user, is_user = True)
        self.data["user_accounts"] = user_accounts

        #
        # Address Details

        self.data["org_address_form"] = contact_forms.EditAddressForm()
        self.data["gst_form"] = tax_form.OrganisationTaxForm()

        if organisation_form is not None:
            org_contacts = users_model.Organisation_Contact.objects.filter(organisation = organisation_form)
            cont_paginator = Paginator(org_contacts, 5)
            cont_page = request.GET.get('page')     
            try:
                cont_posts = cont_paginator.page(cont_page)
            except PageNotAnInteger:
                cont_posts = cont_paginator.page(1)
 
            except EmptyPage:
                cont_posts = cont_paginator.page(cont_paginator.num_pages)
            self.data["address_details"] = cont_posts
            self.data["cont_page"] = cont_page

            # org_address
            org_address = users_model.User_Address_Details.objects.filter(organisation = organisation_form, is_user = True, is_organisation = True)
            paginator = Paginator(org_address, 5)
            page = request.GET.get('page')     
            try:
                posts = paginator.page(page)
            except PageNotAnInteger:
                posts = paginator.page(1)
 
            except EmptyPage:
                posts = paginator.page(paginator.num_pages)
            
            self.data["org_address_details"] = posts
            self.data["page"] = page 
        # edit org address
        contact_address_form = users_model.User_Address_Details.objects.filter(organisation = organisation_form, is_user = True, is_organisation = True)
        c_count = len(contact_address_form)

        # self.data["contact_addresses"] = contact_address_form

        self.data["c_count"] = [i for i in range(c_count)]
            
        self.data["contact_address_form"] = []
        self.data["edit_gst_form"] = []
        
        for i in range(c_count):
            self.data["contact_address_form"].append(contact_forms.EditAddressForm(instance = contact_address_form[i], prefix = 'form_{}'.format(contact_address_form[i].id)))

        #   edit org account
        org_account = users_model.Organisation_Contact.objects.filter(organisation = organisation_form)
        org_account_count = len(org_account)
        self.data["org_account_count"] = [i for i in range(org_account_count)]
            
        self.data["org_account_form"] = []

        for i in range(org_account_count):
            self.data["org_account_form"].append(profile_forms.OrganisationContactForm(instance = org_account[i], prefix = 'form_{}'.format(org_account[i].id)))

        return render(request, self.template_name, self.data)

    #
    #
    def post(self, request):
        organisation = users_model.Organisations.objects.get(user = request.user)
        organisation_form = profile_forms.OrganisationForm(request.POST, request.FILES, instance = organisation)

        if organisation_form.is_valid():
            organisation_form.save()            

        return redirect('/profile/', self.data)


#================================================================================
# ADD ORGANISATION CONTACT
#================================================================================
def add_organisation_contact(request):
    if request.POST:
        
        organisation_form = users_model.Organisations.objects.get(user = request.user)
        form = profile_forms.OrganisationContactForm(request.POST)

        if form.is_valid():
            ret = form.save(commit=False)
            ret.organisation = organisation_form
            ret.save()
        else:
            print(form.errors)
        return redirect("/profile/",permanent = False)
    return redirect("/unauthorized/",permanent = False)

#=======================================================================================
#   ADD ADDRESS DETAILS FORM
#=======================================================================================
#
def add_organisation_addres(request):

    if request.POST:

        try:
            org_ins = users_model.Organisations.objects.get(pk = int(request.POST["ids"]))
        except:
            # pass
            return redirect('/unauthorized/', permanent = False)

        address_form = contact_forms.EditAddressForm(request.POST)
        gst_form = tax_form.OrganisationTaxForm(request.POST)

        gst = None

        if gst_form.is_valid():
            
            if gst_form.data["gstin"] !="" and gst_form.data["gst_reg_type"] !="":        
                gst = gst_form.save(commit = False)
                gst.is_user = True
                gst.organisation = org_ins
                gst.is_organisation = True            
                gst.save()

        if address_form.is_valid():            
            if address_form.data["default_address"] == "True":
                user_helper.change_org_default_address_status(org_ins)
        
            ins = address_form.save(commit = False)
            ins.is_user = True
            ins.organisation = org_ins
            ins.is_organisation = True
            ins.organisation_tax = gst
            ins.save()

    return redirect("/profile/",permanent = False)

#=======================================================================================
#   EDIT ADDRESS DETAILS
#=======================================================================================
#
def edit_org_address_details_form(request, ins):
    if request.POST:

        keys = [i for i in request.POST.keys() if "flat_no" in i]

        prefix = keys[0].replace("-flat_no", "").replace("form_", "")

        try:
            obj = users_model.User_Address_Details.objects.get(pk = int(prefix))    
        except:
            return redirect("/unauthorized/",permanent=False)
        
        #
        # check for GST
        #
                
        if obj.organisation_tax is not None:
            gst_form = tax_form.OrganisationTaxForm(request.POST, instance = obj.organisation_tax)
        else:
            gst_form = tax_form.OrganisationTaxForm(request.POST)
        
        gst = None
        
        if gst_form.is_valid():            
            if gst_form.data["gstin"] !="" and gst_form.data["gst_reg_type"] !="":        
                gst = gst_form.save(commit = False)
                gst.is_user = True
                gst.organisation = obj.organisation
                gst.is_organisation = True            
                gst.save()

        address_form = contact_forms.EditAddressForm(request.POST, prefix='form_'+prefix, instance = obj)
        if address_form.is_valid():        
        
            if address_form.data['form_'+prefix+"-default_address"] == "True":
                user_helper.change_org_default_address_status(obj.organisation)
        
            ins = address_form.save(commit = False)
            ins.is_user = True
            ins.organisation = obj.organisation
            ins.is_organisation = True
            ins.organisation_tax = gst
            ins.save()
         
        set_state_gst(obj.organisation, ins.state, gst)    
        
        return redirect("/profile/",permanent = False)

#=======================================================================================
#   EDIT ADDRESS DETAILS
#=======================================================================================
#
def edit_org_account_details_form(request, ins):
    if request.POST:

        # keys = [i for i in request.POST.keys() if "flat_no" in i]

        # prefix = keys[0].replace("-flat_no", "").replace("form_", "")

        # try:
        #     obj = users_model.User_Address_Details.objects.get(pk = int(prefix))
        #     address_form = contact_forms.EditAddressForm(request.POST, prefix='form_'+prefix, instance = obj)
        #     if address_form.is_valid():
        #         address_form.save()
            
        # except:
        #     try:
        #         org_ins = users_model.Organisations.objects.get(pk = int(ins))
        #     except:
        #         return redirect('/unauthorized/', permanent=False)

        #     address_form = contact_forms.EditAddressForm(request.POST, prefix='form_'+prefix)
        #     if address_form.is_valid():
        #         obj_add = address_form.save()
        #         obj_add.contact_org = org_ins
        #         obj_add.is_user = True
        #         obj_add.save() 

        try:
            org_ins = users_model.Organisation_Contact.objects.get(pk = int(ins))
        except:
            return redirect('/unauthorized/', permanent=False)

        address_form = profile_forms.OrganisationContactForm(request.POST, instance = org_ins)
        if address_form.is_valid():
            obj_add = address_form.save()
            # obj_add.contact_org = org_ins
            # obj_add.is_user = True
            obj_add.save() 
        
        return redirect("/profile/",permanent = False)

#===================================================================================================
# DELETE ORGANIZATION ACCOUNT
#===================================================================================================
#

def delete_org_account(request, ins = None):

    if ins is not None:
        try:
            users_model.Organisation_Contact.objects.get(pk = int(ins)).delete()
        except:
            return HttpResponse(0)
        
        return HttpResponse(1)
    return HttpResponse(1)
    
#===================================================================================================
# CHECK EXISTING GST
#===================================================================================================
#

def check_gst_existing(request):
    if request.POST:
        if request.is_ajax():    
            address_count = users_model.User_Address_Details.objects.filter(state = request.POST["state_id"], organisation_id = int(request.POST["organisation_id"]), is_user = True, is_organisation = True).count()
            return HttpResponse(address_count)
        return redirect("/unauthorized/", permnent = False)
    return redirect("/unauthorized/", permnent = False)
    
#===================================================================================================
# GET GST - BASED ON ADDRESS
#===================================================================================================
#    

def get_gst(request):
    if request.POST:
        if request.is_ajax():
        
            data = {'tax_id':None, 'gstin': None, 'gst_reg_type':None}
            
            try:
                ins = users_model.User_Address_Details.objects.get(pk = request.POST["address_id"])
            except:
                return redirect("/unauthorized/", permnent = False)
            
            try:            
                tax_details = users_model.User_Tax_Details.objects.get(pk = ins.organisation_tax_id)
                        
                data['tax_id'] = tax_details.id
                data['gstin'] = tax_details.gstin
                data['gst_reg_type'] = tax_details.gst_reg_type
            
            except:
                pass
            
            return JsonResponse(data)
        return redirect("/unauthorized/", permnent = False)
    return redirect("/unauthorized/", permnent = False)    
    
#===================================================================================================
# GET GST - FROM STATES
#===================================================================================================
#    
def get_state_gst(request):
    if request.POST:
        if request.is_ajax():
        
            data = {'gstin': None, 'gst_reg_type':None}
            
            addresses = users_model.User_Address_Details.objects.filter(
                            is_user = True, 
                            is_organisation = True, 
                            organisation = request.POST["organisation_id"], 
                            state = request.POST["state_id"],
                            organisation_tax__isnull = False,
                            )
                        
            for addr in addresses:
                if addr.organisation_tax.gstin is not None:
                
                    data['gstin'] = addr.organisation_tax.gstin
                    data['gst_reg_type'] = addr.organisation_tax.gst_reg_type
                    
                    return JsonResponse(data)
            return JsonResponse(data)
            
        return redirect("/unauthorized/", permnent = False)
    return redirect("/unauthorized/", permnent = False)      
            
#
#
#
def set_state_gst(organisation = None, state = None, gst = None):
    if gst is not None and organisation is not None and state is not None:
        addresses = users_model.User_Address_Details.objects.filter(
                            is_user = True, 
                            is_organisation = True, 
                            organisation = organisation, 
                            state = state)
            
        for addr in addresses:
            addr.organisation_tax = gst 
            addr.save()
 

#===================================================================================================
# GST SETTINGS
#===================================================================================================
# 

class GSTSettingsView(View):
    
    # Template 
    template_name = 'app/app_files/profile_manager/index.html'

    # Initialize 
    data = defaultdict()
    data["view"] = ""
    data["contacts"] = {}
    data["active_link"] = 'Profile'
    data["breadcrumb_title"] = 'GST Settings'

    # Custom CSS/JS Files For Inclusion into template
    data["css_files"] = []
    #data["js_files"] = []
    data["js_files"] = []

    data["included_template"] = 'app/app_files/profile_manager/gst_settings.html'

    #
    #
    def get(self, request): 
        self.data["org_add_form"] = tax_form.OrganisationGSTSettingsForm() 
        
        org = users_model.OrganisationGSTSettings.objects.filter(user=request.user)
        
        self.data["edit_form"] = []
        
        for i in range(org.count()):
            self.data["edit_form"].append(tax_form.OrganisationGSTSettingsForm(instance = org[i], prefix="form_{}".format(org[i].id))) 

        self.data["org_gst_details"] = org
    
        return render(request, self.template_name, self.data)
 
    #
    #
    def post(self, request):
        org_add_form = tax_form.OrganisationGSTSettingsForm(request.POST)
    
        if org_add_form.is_valid():
            org = org_add_form.save(commit=False)
            org.user = request.user
            org.save()
        else:
            print(org_add_form.errors)
        return redirect("/profile/gst_settings/", permanent=False)    
       
 
#===================================================================================================
# DELETE GST SETTINGS
#===================================================================================================
#  
 
def delete_gst_settings(request, ins=None):
    if ins is not None:
        org = users_model.OrganisationGSTSettings.objects.filter(user=request.user, pk=int(ins))
        org.delete()
        return redirect("/profile/gst_settings/", permanent=False)    
    return redirect("/unauthorized/", permnent = False)    
 
 
#===================================================================================================
# EDIT GST SETTINGS
#===================================================================================================
#  
 
def edit_gst_settings(request):

    if request.POST:
        keys = [i for i in request.POST.keys() if "-taxname" in i]
        
        prefix = keys[0].replace("-taxname", "").replace("form_", "")
        
        org = users_model.OrganisationGSTSettings.objects.get(pk=int(prefix))
        
        org.taxname = request.POST["form_{}-taxname".format(prefix)]
        org.taxname_percent = request.POST["form_{}-taxname_percent".format(prefix)]
        org.save()

        return redirect("/profile/gst_settings/", permanent=False)  
    return redirect("/unauthorized/", permnent = False) 
 
 
#===================================================================================================
# BLANK PROFILE
#===================================================================================================
#               
                    
def blank(req):
    return render(req,'app/app_files/profile_manager/blank.html')           