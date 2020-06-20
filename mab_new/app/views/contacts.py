from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse
from django.views import View
from collections import OrderedDict, defaultdict
from django.contrib import messages

from app.models.contacts_model import *
from app.models.users_model import *
from app.models.customize_model import *

from app.forms.contact_forms import *
from app.forms.tax_form import *
from app.forms.inc_fomsets import *
from app.helpers import *

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


from django.conf import *

from django.db import *
from django.db.models import Q


import json, os, csv, re




#=====================================================================================
#   CONTACTS VIEW
#=====================================================================================
#
class ContactsView(View):

    # Template 
    template_name = 'app/app_files/contacts/base.html'
    
    # Initialize 
    data = defaultdict()
    data["view"] = ""
    data["contacts"] = {}
    data["active_link"] = 'Contacts'
    data["breadcrumb_title"] = 'CONTACTS'

    # Custom CSS/JS Files For Inclusion into template
    data["css_files"] = []
    data["js_files"] = ['custom_files/js/customize_view.js','custom_files/js/contacts.js']

    data["included_template"] = 'app/app_files/contacts/view_contacts.html'
    
    #
    #
    def get(self, request, *args, **kwargs):   
    
        search = request.GET.get('search',False)
        
        customer_type = request.GET.getlist('customer_type[]')
        org_type = request.GET.getlist('org_type[]')
        is_active = request.GET.getlist('is_active[]')

        contacts = contacts_model.Contacts.objects.filter(Q(user = request.user) & Q(contact_delete_status = 0))

        if search:
            contacts = contacts.filter(
                Q(contact_name__contains = search) | 
                Q(display_name__contains = search) |
                Q(organization_name__contains = search)
            )

        if customer_type:
            contacts = contacts.filter(customer_type__in = customer_type)
        
        if org_type:
            contacts = contacts.filter(organization_type__in = org_type)
        
        if is_active:
            contacts = contacts.filter(is_active__in = is_active)
        else:
            contacts = contacts.filter(is_active = True)

        # self.data["contacts"] = contacts
        contact_paginator = Paginator(contacts, 10)
        contact_page = request.GET.get('page')     
        try:
            contact_posts = contact_paginator.page(contact_page)
        except PageNotAnInteger:
            contact_posts = contact_paginator.page(1)
        except EmptyPage:
            contact_posts = contact_paginator.page(contact_paginator.num_pages)
        self.data["contacts"] = contact_posts
        self.data["contact_page"] = contact_page

        # CUSTOMIZE VIEW CODE
        customize_contact = CustomizeModuleName.objects.filter(Q(user = request.user) & Q(customize_name = 1))
        if(len(customize_contact) != 0):
            view_contact = CustomizeContactView.objects.get(customize_view_name = customize_contact[0].id)
            if(view_contact is not None):
                self.data['customize'] = view_contact
            else:
                self.data['customize'] = 'NA'
        else:
                self.data['customize'] = 'NA'
                
        
        
        return render(request, self.template_name, self.data)


#=====================================================================================
#   ADD CONTACTS
#=====================================================================================
#
def add_contacts(request, slug = None, ins = None):

    # Initialize 
    data = defaultdict()

    # Template 
    template_name = 'app/app_files/contacts/add_contacts.html'
    data["included_template"] = 'app/app_files/contacts/add_contacts.html'
    
    # Custom CSS/JS Files For Inclusion into template
    data["css_files"] = []
    data["js_files"] = ['custom_files/js/contacts.js']

    # Set link as active in menubar
    data["active_link"] = 'Contacts'
    data["breadcrumb_title"] = 'CONTACTS'

    # Initialize Forms
    data["contact_form"] = ContactsForm()
    data["tax_form"] = TaxForm()
    data["other_details_form"] = OtherDetailsForm()
    data["social_form"] = ContactsExtraForm()

    #
    # FORMSETS    
    data["address_formset"] = AddressFormset
    data["accounts_formset"] = AccountsFormset

    #
    # POST REQUEST - FORM SUBMISSION
    #
    if request.POST:
        contact_form = ContactsForm(request.POST)
        tax_form = TaxForm(request.POST)   

        ins = None

        if contact_form.is_valid():
            ins = contact_form_ins = contact_form.save(commit = False)
            contact_form_ins.user = request.user

            if contact_form_ins.is_imported_user:
                try:
                    profile = Profile.objects.get(app_id__iexact = contact_form_ins.app_id)
                    imp_user = User.objects.get(pk = profile.user_id)
                except:
                    return redirect('/unauthorized/', permanent = False)
                
                contact_form_ins.imported_user = imp_user
            
            #
            # Social form -- save
            #

            social_form = ContactsExtraForm(request.POST, request.FILES, instance = contact_form_ins)
            if social_form.is_valid():
                social_form.save()

            contact_form_ins.save() 
        else:
            print(contact_form.errors.as_data())

        #
        #
        if ins is not None:

            #
            # tax form/ other details form -- save
            #
            if tax_form.is_valid(): 
                obj_tax = tax_form.save(commit = False)
                obj_tax.contact = ins

                other_details_form = OtherDetailsForm(request.POST, instance = obj_tax)
                if other_details_form.is_valid():
                    other_details_form.save()
                obj_tax.save()    
            else:
                pass

            #
            # Address Formset -- save
            #
            address_formset = AddressFormset(request.POST)
            
            if address_formset.is_valid():               

                rownum = 0

                flat_no = []
                is_shipping_address_diff = []

                found_default = False

                for form in address_formset:
                                                   
                    for i in form.data.keys():
                    
                        if "default_address" in i:
                            if found_default is False and (form.data[i] == '1' or form.data[i] == 'True'): 
                                found_default = True
                                                
                        if "flat_no" in i and i not in flat_no:
                            flat_no.append(i)
                        if "is_shipping_address_diff" in i and i not in is_shipping_address_diff:
                            is_shipping_address_diff.append(i)
                
                if found_default:
                    user_helper.change_contact_default_address_status(ins)

                for form in address_formset:
                    if form.is_valid():    
                      
                        if form.data[flat_no[rownum]]:
                            
                            obj = form.save(commit = False)
                            obj.is_user = False
                            obj.contact = ins
                            # obj.address_belong = 1
                            
                            if form.data[is_shipping_address_diff[rownum]] == "1":    
                                obj.is_shipping_address = 0
                            
                            obj.save()  
                    rownum +=1    
            #
            # Accounts Formset -- save
            #
            accounts_formset = AccountsFormset(request.POST)
            if accounts_formset.is_valid():

                rownum = 0

                account_holder_name = []
                for form in accounts_formset:
                    for i in form.data.keys():
                        if "account_holder_name" in i and i not in account_holder_name:
                            account_holder_name.append(i)

                for form in accounts_formset:
                    if form.is_valid():
                        if form.data[account_holder_name[rownum]]:
                            obj = form.save(commit = False)
                            obj.is_user = False
                            obj.contact = ins
                            obj.save()
                        rownum +=1
                        
        if request.POST.get('json_response'):
            success = True if ins.customer_type == 2 else False
            data = {'success':success, 'contact_name':ins.contact_name.upper(), 'contact_id':ins.id}
            return JsonResponse(data)
                
        return redirect('/contacts/', data)
    return render(request, template_name, data)


#=====================================================================================
#   EDIT CONTACTS
#=====================================================================================
#
def edit_contact(request, ins = None):
        
        # Initialize 
        data = defaultdict()

        # Template 
        template_name = 'app/app_files/contacts/edit_contact.html'
        data["included_template"] = 'app/app_files/contacts/edit_contact.html'
        
        # Custom CSS/JS Files For Inclusion into template
        data["css_files"] = []
        data["js_files"] = ['custom_files/js/contacts.js']

        # Set link as active in menubar
        data["active_link"] = 'Contacts'
        data["breadcrumb_title"] = 'CONTACTS'

        if ins is not None:

            contact = None
            tax_form = None
            accounts = None

            #
            # Contact Details
            try:
                contact = Contacts.objects.get(pk = int(ins))
            except:
                return redirect('/unauthorized/', permanent=False)

            data["contact_details"] = contact

            data["contact_form"] = ContactsForm(instance = contact)
            data["social_form"] = ContactsExtraForm(instance = contact)
            data['contact_attachment'] = contact.attachements

            #

            data["contact_ins"] = contact.id
            data["tax_ins"] = ""
            
            #
            # Tax Details
            try:
                tax_form = User_Tax_Details.objects.get(is_user = False, contact = contact)
                data["tax_ins"] = tax_form.id  
            except:
                pass

            data["tax_form_details"] = tax_form
            data["tax_form"] = TaxForm(instance = tax_form)
            data["other_details_form"] = OtherDetailsForm(instance = tax_form)

            #
            # Addresses
            contact_address_form = User_Address_Details.objects.filter(contact = contact, is_user = False)
            c_count = len(contact_address_form)

            data["contact_addresses"] = contact_address_form

            data["c_count"] = [i for i in range(c_count)]
            
            data["contact_address_form"] = []
            for i in range(c_count):
                data["contact_address_form"].append(EditAddressForm(instance = contact_address_form[i], prefix = 'form_{}'.format(contact_address_form[i].id)))


            data["new_address_form"] = EditAddressForm()
            data["new_accounts_form"] = AccountDetailsForm()

            #
            # Accounts
            contact_accounts_form = User_Account_Details.objects.filter(contact = contact, is_user = False)
            a_c_count = len(contact_accounts_form)
            data["contact_accounts"] = contact_accounts_form

            data["a_c_count"] = [i for i in range(a_c_count)]

            data["contact_accounts_form"] = []
            for i in range(a_c_count):
                data["contact_accounts_form"].append(AccountDetailsForm(instance = contact_accounts_form[i], prefix = 'form_{}'.format(contact_accounts_form[i].id)))

        else:    
            return redirect('/unauthorized/', permanent = False)
        return render(request, template_name, data)

#=======================================================================================
#   ADD ADDRESS DETAILS FORM
#=======================================================================================
#
def add_address_details_form(request):

    if request.POST:
        try:
            contact_ins = Contacts.objects.get(pk = int(request.POST["ids_con"]))
        except:
            return redirect('/unauthorized/', permanent = False)

        address_form = EditAddressForm(request.POST)
        
        if address_form.is_valid():
        
            if address_form.data["default_address"] == "True" :
                user_helper.change_contact_default_address_status(contact_ins)
        
            ins = address_form.save(commit = False)
            ins.contact = contact_ins
            ins.is_user = False
            ins.save()
        else:
            print(address_form.errors)

    return redirect('/contacts/edit/{}/'.format(request.POST["ids_con"]), permanent = False)


#=======================================================================================
#   ADD ACCOUNTS DETAILS
#=======================================================================================
#
def add_accounts_details_form(request):

    if request.POST:
        try:
            contact_ins = Contacts.objects.get(pk = int(request.POST["ids"]))
        except:
            return redirect('/unauthorized/', permanent = False)

        accounts_form = AccountDetailsForm(request.POST)

        if accounts_form.is_valid():
            ins = accounts_form.save(commit = False)
            ins.contact = contact_ins
            ins.is_user = False
            ins.save()

    return redirect('/contacts/edit/{}/'.format(request.POST["ids"]), permanent = False)




#=======================================================================================
#   EDIT CONTACT DETAILS
#=======================================================================================
#
def edit_contact_details_form(request):

    if request.POST:

        try:
            contact_ins = Contacts.objects.get(pk = int(request.POST["ids"]))
        except:
            return redirect('/unauthorized/', permanent = False)

        contact_form = ContactsForm(request.POST, instance=contact_ins)
        if contact_form.is_valid():    
            contact_form.save() 
    return redirect('/contacts/edit/{}/'.format(request.POST["ids"]), permanent = False)

#=======================================================================================
#   EDIT TAX & OTHER DETAILS
#=======================================================================================
#
def edit_tax_details_form(request):
    if request.POST:
        try:
            obj_ins = users_model.User_Tax_Details.objects.get(pk = int(request.POST["obj_ins"]))   
            tax_form = TaxForm(request.POST, instance = obj_ins)

            if tax_form.is_valid():
                tax_form.save()  
        except:
            contact_ins = contacts_model.Contacts.objects.get(pk = int(request.POST["ids"]))
            tax_form = TaxForm(request.POST)

            if tax_form.is_valid():
                tax_form.save(commit  = False)
                tax_form.contact = contact_ins
                tax_form.save()  

    return redirect('/contacts/edit/{}/'.format(request.POST["ids"]), permanent = False)


def edit_other_details_form(request):
    if request.POST:
        try:
            obj_ins = users_model.User_Tax_Details.objects.get(pk = int(request.POST["obj_ins"]))   
            tax_form = OtherDetailsForm(request.POST, instance = obj_ins)

            if tax_form.is_valid():
                tax_form.save()  
        except:
            try:
                contact_ins = contacts_model.Contacts.objects.get(pk = int(request.POST["ids"]))
            except:
                return redirect('/unauthorized/', permanent=False)

            tax_form = OtherDetailsForm(request.POST)

            if tax_form.is_valid():
                tax_form.save(commit  = False)
                tax_form.contact = contact_ins
                tax_form.save()         
    return redirect('/contacts/edit/{}/'.format(request.POST["ids"]), permanent = False)
#=======================================================================================
#   EDIT ADDRESS DETAILS
#=======================================================================================
#
def edit_address_details_form(request):
    if request.POST:

        keys = [i for i in request.POST.keys() if "flat_no" in i]

        prefix = keys[0].replace("-flat_no", "").replace("form_", "")
        
        
        try:
            obj = users_model.User_Address_Details.objects.get(pk = int(prefix))
            address_form = EditAddressForm(request.POST, prefix='form_'+prefix, instance = obj)
                        
            if address_form.is_valid():
                if address_form.data['form_'+prefix+"-default_address"] == "True":
                    user_helper.change_contact_default_address_status(obj.contact)
                
                address_form.save()
                
        except:
            try:
                contact = Contacts.objects.get(pk = int(request.POST["ids"]))
            except:
                return redirect('/unauthorized/', permanent=False)

            address_form = EditAddressForm(request.POST, prefix='form_'+prefix)
            
            if address_form.is_valid():      
                if address_form.data['form_'+prefix+"-default_address"] == "True":
                    user_helper.change_contact_default_address_status(obj.contact)
                    
                obj_add = address_form.save()
                obj_add.contact = contact
                obj_add.save() 
        
        return redirect('/contacts/edit/{}/'.format(request.POST["ids"]), permanent = False)

#=======================================================================================
#   EDIT ACCOUNTS DETAILS
#=======================================================================================
#
def edit_accounts_details_form(request):
    if request.POST:

        keys = [i for i in request.POST.keys() if "account_number" in i]

        prefix = keys[0].replace("-account_number", "").replace("form_", "")

        try:
            account = users_model.User_Account_Details.objects.get(pk = int(prefix))
        except:
            return redirect('/unauthorized/', permanent=False)

        account_form = AccountDetailsForm(request.POST, prefix='form_'+prefix, instance = account)
        if account_form.is_valid():
            account_form.save()

    return redirect('/contacts/edit/{}/'.format(request.POST["ids"]), permanent = False)

#=======================================================================================
#   EDIT SOCIAL DETAILS
#=======================================================================================
#
def edit_social_details_form(request):
    if request.POST:
        try:
            contact = Contacts.objects.get(pk = int(request.POST["ids"]))
        except:
            return redirect('/unauthorized/', permanent=False)
        
        social_form = ContactsExtraForm(request.POST, request.FILES, instance = contact)

        if social_form.is_valid():
            social_form.save()

    return redirect('/contacts/edit/{}/'.format(request.POST["ids"]), permanent = False)   

#================================================================================
# CHECK APPLICATION ID
# GET USER ID BASED ON THE CHECK
#================================================================================

def get_app_user_id(app_id):
    data = {'ret':0, 'id':None}
    try:
        pro = Profile.objects.get(app_id__iexact = app_id)
        data["ret"] = 1
        data["id"] = pro.user_id
    except:
        pass
    return data

#================================================================================
# CHECK APPLICATION ID
#================================================================================

def count_user_in_contact_list(user_id, imp_user_id):
    return Contacts.objects.filter(user = user_id, imported_user_id = int(imp_user_id)).count()

#================================================================================
# USER - CONTACT ALREADY PRESENT IN THE CONTACT LIST
#================================================================================

def check_app_id(request):
    data = {}
    if request.is_ajax():
        if request.POST: 
            data = get_app_user_id(request.POST["id"])
    return HttpResponse(json.dumps(data))


#================================================================================
# CHECK APPLICATION ID EXISTS IN THE CONTACT LIST
#================================================================================

def user_exists_in_list(request):
    if request.is_ajax():
        if request.POST:
            total = count_user_in_contact_list(request.user, request.POST["id"])
            return HttpResponse(total)    
        return HttpResponse(-1)
    return HttpResponse(-1)

#================================================================================
# CONTACTS FILE UPLOAD VIEW
#================================================================================

class ContactsFileUploadView(View):
    
    # Template 
    template_name = 'app/app_files/contacts/upload_contacts.html'
    
    # Initialize 
    data = defaultdict()
    data["view"] = ""
    data["contacts"] = {}
    data["active_link"] = 'Contacts'
    data["breadcrumb_title"] = 'CONTACTS'

    # Custom CSS/JS Files For Inclusion into template
    data["css_files"] = []
    data["js_files"] = ['custom_files/js/contacts.js']

    data["included_template"] = 'app/app_files/contacts/upload_contacts.html'
    
    data["error_now"] = []
    data["row_count"] = 0
    data["saved_msg"] = '0'

    # Documentation Import
    data["documentation_dict"] = documentation_dict.CSV_IMPORT_DICT

    #
    #
    def get(self, request, a):        
        self.data["error"] = ""
        self.data["saved_msg"] = '0'
        self.data["error_key_dict"] = {}
        self.data["upload_form"] = UploadContactsForm()
        return render(request, self.template_name, self.data)

    def post(self, request, a):
        self.data["error"] = ""
        self.data["saved_msg"] = '0'
        self.data["error_key_dict"] = {}
        
        self.data["upload_form"] = UploadContactsForm(request.POST, request.FILES)

        if self.data["upload_form"].is_valid():

            if str(request.FILES['csv_file']).lower().endswith('.csv'):

                self.data["upload_form"].save(commit = False)
                self.data["upload_form"].user = request.user
                obj = self.data["upload_form"].save()

                #***************************************************************
                #   Validate and Write data to database
                #***************************************************************

                file_path = settings.MEDIA_ROOT+"/"+str(obj.csv_file)

                if check_record_count(file_path) <= 100:

                    err, self.data["row_count"], self.data["error_key_dict"] = check_csv_validation(request.user, file_path)
                
                    if err > 0:
                        self.data["saved_msg"] = '3'
                        obj.delete()
                    else:
                        if obj:
                            self.data["saved_msg"] = '1'
                            csv_2_contacts(request.user,file_path)
                        else:
                            self.data["saved_msg"] = '2'
                    
                    self.data["error"] = err
                else:
                    self.data["saved_msg"] = '5'                
            else:
               self.data["saved_msg"] = '4'
        else:
            self.data["error"] = "Only CSV file is supported"

        return render(request, self.template_name, self.data)

#==============================================================================
# Function to insert contact import csv data into database
#==============================================================================
#

def check_record_count(file_path):
    row_count = 0

    with open(file_path, newline='', encoding='utf-8') as csvfile:
        records = csv.DictReader(csvfile)

        fields = records.fieldnames

        for row in records:
            if row["is_parent_record"] == 'TRUE':
                row_count += 1

    return row_count

#
#
#
def check_csv_validation(user, file_path):
    row_count = 1
    error_key_dict = dict()
    error_row = 0

    with open(file_path, newline='', encoding='utf-8') as csvfile:
        records = csv.DictReader(csvfile)

        fields = records.fieldnames

        for row in records:

            #*************************************************************** 
            # Get and Set Missing/Existence of fields
            #***************************************************************
            salutation = row["salutation"] if "salutation" in fields else None
            customer_type = row["customer_type"] if "customer_type" in fields else None
            is_sub_customer = row["is_sub_customer"] if "is_sub_customer" in fields else 1
            contact_name = row["contact_name"] if "contact_name" in fields else None
            display_name = row["display_name"] if "display_name" in fields else None
            
            organization_name = row["organisation_name"] if "organisation_name" in fields else None
            
            if "is_msme_reg" in fields:
                is_msme_reg = True if row["is_msme_reg"] == 'TRUE' else False
            else:
                is_msme_reg = False

            email = row["email"] if "email" in fields else None
            phone = row["phone"] if "phone" in fields else None
            website = row["website"] if "website" in fields else None
            facebook = row["facebook"] if "facebook" in fields else None
            twitter = row["twitter"] if "twitter" in fields else None
            notes = row["notes"] if "notes" in fields else None

            contact_person = row["contact_person"] if "contact_person" in fields else None
            flat_no = row["flat_door_no"] if "flat_door_no" in fields else None
            street = row["street"] if "street" in fields else None
            city = row["city"] if "city" in fields else None
            pincode = row["pincode"] if "pincode" in fields else None
            state = row["state"] if "state" in fields else None
            country = row["country"] if "country" in fields else None

            account_number = row["account_number"] if "account_number" in fields else None 
            account_holder_name = row["account_holder_name"] if "account_holder_name" in fields else None 
            ifsc_code = row["ifsc_code"] if "ifsc_code" in fields else None 
            bank_name = row["bank_name"] if "bank_name" in fields else None 
            bank_branch_name = row["branch_name"] if "branch_name" in fields else None
            
            pan = row["pan"] if "pan" in fields else None
            gstin = row["gstin"] if "gstin" in fields else None            
            business_reg_no = row["business_reg_no"] if "business_reg_no" in fields else None
            tax_reg_no = row["tax_reg_no"] if "tax_reg_no" in fields else None
            cst_reg_no = row["cst_reg_no"] if "cst_reg_no" in fields else None
            tds = row["tds"] if "tds" in fields else None
            preferred_currency = row["preferred_currency"] if "preferred_currency" in fields else None
            opening_balance = row["opening_balance"] if "opening_balance" in fields else None
            as_of = row["as_of"] if "as_of" in fields else None
            preferred_payment_method = row["preferred_payment_method"] if "preferred_payment_method" in fields else None
            preferred_delivery = row["preferred_delivery"] if "preferred_delivery" in fields else None
            invoice_terms = row["invoice_terms"] if "invoice_terms" in fields else None
            bills_terms = row["billing_terms"] if "billing_terms" in fields else None

            #***************************************************************
            # Validations
            #***************************************************************

            email_pattern = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'

            url_pattern = '^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$'

            ifsc_pattern = '^[A-Za-z]{4}[a-zA-Z0-9]{7}$'

            gst_pattern = '^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$'

            pan_pattern = re.compile(r'[A-Z]{5}[0-9]{4}[A-Z]{1}')

            phone_pattern = re.compile(r'\d{10}')

            number_pattern = re.compile(r'\d*')

            currency_pattern = re.compile(r'^-?0*(?:\d+(?!,)(?:\.\d{1,2})?|(?:\d{1,3}(?:,\d{3})*(?:\.\d{1,2})?))$')

            # ERROR DICT
            error_key_dict[str(row_count)] = {
                "error" : 0,
                "email" : {'ret':0, 'value':''},
                "website" : {'ret':0, 'value':''},
                "pan" : {'ret':0, 'value':''},
                "ifsc_code" : {'ret':0, 'value':''},
                "gstin" : {'ret':0, 'value':''},
                "phone" : {'ret':0, 'value':''},
                "account_number" : {'ret':0, 'value':''},
                "pincode" : {'ret':0, 'value':''},
                "opening_balance" : {'ret':0, 'value':''},
            }


            # check email
            error_key_dict[str(row_count)]["email"]["value"] = email
            if not re.search(email_pattern, email) and email is not None and email != '':
                error_key_dict[str(row_count)]["error"] = 1                
                error_key_dict[str(row_count)]["email"]["ret"] = 1
                error_row = 1   

            # check url            
            error_key_dict[str(row_count)]["website"]["value"] = website
            if not re.search(url_pattern, website) and website is not None and website !='':
                error_key_dict[str(row_count)]["error"] = 1
                error_key_dict[str(row_count)]["website"]["ret"] = 1
                error_row = 1     
            

            # check PAN
            error_key_dict[str(row_count)]["pan"]["value"] = pan
            if not pan_pattern.fullmatch(pan) and pan is not None and pan !='':
                error_key_dict[str(row_count)]["error"] = 1                
                error_key_dict[str(row_count)]["pan"]["ret"] = 1
                error_row = 1    

            # check IFSC
            error_key_dict[str(row_count)]["ifsc_code"]["value"] = ifsc_code
            if not re.search(ifsc_pattern, ifsc_code) and ifsc_code is not None and ifsc_code!='':
                error_key_dict[str(row_count)]["error"] = 1
                error_key_dict[str(row_count)]["ifsc_code"]["ret"] = 1
                error_row = 1    

            # check GST
            error_key_dict[str(row_count)]["gstin"]["value"] = gstin
            if not re.search(gst_pattern, gstin) and gstin is not None and gstin!='':
                error_key_dict[str(row_count)]["error"] = 1
                error_key_dict[str(row_count)]["gstin"]["ret"] = 1
                error_row = 1    

            # check Phone
            error_key_dict[str(row_count)]["phone"]["value"] = phone
            if not phone_pattern.fullmatch(phone) and phone is not None and phone!='':
                error_key_dict[str(row_count)]["error"] = 1
                error_key_dict[str(row_count)]["phone"]["ret"] = 1
                error_row = 1      

            # check Account Number
            error_key_dict[str(row_count)]["account_number"]["value"] = account_number
            if not number_pattern.fullmatch(account_number) and account_number is not None and account_number!='':
                error_key_dict[str(row_count)]["error"] = 1
                error_key_dict[str(row_count)]["account_number"]["ret"] = 1
                error_row = 1    

            # check Account Number
            error_key_dict[str(row_count)]["pincode"]["value"] = pincode
            if not number_pattern.fullmatch(pincode) and pincode is not None and pincode!='':
                error_key_dict[str(row_count)]["error"] = 1
                error_key_dict[str(row_count)]["pincode"]["ret"] = 1
                error_row = 1   

            # check Opening Balance
            error_key_dict[str(row_count)]["opening_balance"]["value"] = opening_balance
            if not currency_pattern.fullmatch(opening_balance) and opening_balance is not None and opening_balance!='':
                error_key_dict[str(row_count)]["error"] = 1
                error_key_dict[str(row_count)]["opening_balance"]["ret"] = 1
                error_row = 1     

            # GST_REG_TYPE validation
            if "gst_reg_type" in fields: 
                if row["gst_reg_type"] !='':                
                    gst_reg_type = int(row["gst_reg_type"]) 
                    if not(gst_reg_type >=0 and gst_reg_type <=7):
                        error_row = 1     
                else:
                    gst_reg_type = 1
           
            # ORGANISATION_TYPE validation
            if "organisation_type" in fields:
                if row["organisation_type"] !='':  
                    organization_type = int(row["organisation_type"])
                    if not(organization_type >= 1 and organization_type <=6):
                        error_row = 1     
                else:
                    organization_type = 1

            row_count += 1
    return error_row, row_count, error_key_dict
        


#***************************************************************
# Phase 1
#***************************************************************
def csv_2_contacts(user, file_path):
    
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        records = csv.DictReader(csvfile)

        fields = records.fieldnames

        contact_ins = None

        for row in records:

            #*************************************************************** 
            # Get and Set Missing/Existence of fields
            #***************************************************************
            salutation = row["salutation"] if "salutation" in fields else None
            customer_type = row["customer_type"] if "customer_type" in fields else None
            is_sub_customer = row["is_sub_customer"] if "is_sub_customer" in fields else 1
            contact_name = row["contact_name"] if "contact_name" in fields else None
            display_name = row["display_name"] if "display_name" in fields else None
            organization_type = row["organisation_type"] if "organisation_type" in fields else 1
            organization_name = row["organisation_name"] if "organisation_name" in fields else None
            
            if "is_msme_reg" in fields:
                is_msme_reg = True if row["is_msme_reg"] == 'TRUE' else False
            else:
                is_msme_reg = False

            email = row["email"] if "email" in fields else None
            phone = row["phone"] if "phone" in fields else None
            website = row["website"] if "website" in fields else None
            facebook = row["facebook"] if "facebook" in fields else None
            twitter = row["twitter"] if "twitter" in fields else None
            notes = row["notes"] if "notes" in fields else None

            contact_person = row["contact_person"] if "contact_person" in fields else None
            flat_no = row["flat_door_no"] if "flat_door_no" in fields else None
            street = row["street"] if "street" in fields else None
            city = row["city"] if "city" in fields else None
            pincode = row["pincode"] if "pincode" in fields else None
            state = row["state"] if "state" in fields else None
            country = row["country"] if "country" in fields else None

            account_number = row["account_number"] if "account_number" in fields else None 
            account_holder_name = row["account_holder_name"] if "account_holder_name" in fields else None 
            ifsc_code = row["ifsc_code"] if "ifsc_code" in fields else None 
            bank_name = row["bank_name"] if "bank_name" in fields else None 
            bank_branch_name = row["branch_name"] if "branch_name" in fields else None
            
            pan = row["pan"] if "pan" in fields else None
            gstin = row["gstin"] if "gstin" in fields else None
            gst_reg_type = row["gst_reg_type"] if "gst_reg_type" in fields else None
            business_reg_no = row["business_reg_no"] if "business_reg_no" in fields else None
            tax_reg_no = row["tax_reg_no"] if "tax_reg_no" in fields else None
            cst_reg_no = row["cst_reg_no"] if "cst_reg_no" in fields else None
            tds = row["tds"] if "tds" in fields else None
            preferred_currency = row["preferred_currency"] if "preferred_currency" in fields else None
            opening_balance = row["opening_balance"] if "opening_balance" in fields else None
            as_of = row["as_of"] if "as_of" in fields else None
            preferred_payment_method = row["preferred_payment_method"] if "preferred_payment_method" in fields else None
            preferred_delivery = row["preferred_delivery"] if "preferred_delivery" in fields else None
            invoice_terms = row["invoice_terms"] if "invoice_terms" in fields else None
            bills_terms = row["billing_terms"] if "billing_terms" in fields else None

            
            if row["is_parent_record"] == 'TRUE':
                
                #***************************************************************
                # Initiate Create
                #***************************************************************

                contact = Contacts(
                    salutation = salutation,
                    customer_type = customer_type,
                    is_sub_customer = is_sub_customer,
                    contact_name = contact_name,
                    display_name = display_name,
                    organization_type = organization_type,
                    organization_name = organization_name,
                    is_msme_reg = is_msme_reg,
                    email = email,
                    phone = phone,
                    website = website,
                    facebook = facebook,
                    twitter = twitter,
                    user = user,
                    notes = notes,
                )
                
                #***************************************************************
                #   If @ret is TRUE and user is not present in the  
                #   contact list then add user to contact list.
                #   If user is present then overwrite the data with the 
                #   csv record data.
                #***************************************************************  
                 
                if "app_id" in fields and row["app_id"].strip() !="":
                    ret = get_app_user_id(row["app_id"])

                    if ret["ret"] == 1:                        
                        if count_user_in_contact_list(user, ret["id"]) == 0:
                            contact.save()

                            contact.imported_user_id = ret["id"]
                            contact.app_id = row["app_id"]

                            if row["use_app_user_details"] == 'TRUE': 
                                contact.is_imported_user = True
                                
                            contact.save()
                            contact_ins = contact
                        else:
                            #***************************************************************
                            # Initiate Update
                            #***************************************************************

                            contact_ins = contact = Contacts.objects.get(app_id__iexact = row["app_id"], user = user)
                            contact.salutation = salutation
                            contact.customer_type = customer_type
                            contact.is_sub_customer = is_sub_customer
                            contact.contact_name = contact_name
                            contact.display_name = display_name
                            contact.organization_type = organization_type
                            contact.organization_name = organization_name
                            contact.is_msme_reg = is_msme_reg
                            contact.email = email
                            contact.phone = phone
                            contact.website = website
                            contact.facebook = facebook
                            contact.twitter = twitter
                            contact.notes = notes
                            contact.save()
                    else:
                        contact_ins = None
                else:
                    contact.save()
                    contact_ins = contact

            #***************************************************************
            # Phase 2
            #***************************************************************

            if contact_ins is not None:
                
                #***************************************************************
                # Address Details
                #***************************************************************

                if "is_contact_address" in fields and row["is_contact_address"] == "TRUE":
                
                    is_billing_address = False
                    is_shipping_address = False

                    if "is_billing_address" in fields and row["is_billing_address"] == "TRUE":
                        is_billing_address = True

                    if "is_shipping_address" in fields and row["is_shipping_address"] == "TRUE":
                        is_shipping_address = True

                    contact_address = users_model.User_Address_Details(
                        is_user = False,
                        contact_person = contact_person, 
                        flat_no = flat_no,
                        street = street,
                        city = city,
                        pincode = pincode,
                        state = state,
                        country = country,
                        is_billing_address = is_billing_address,
                        is_shipping_address = is_shipping_address,
                        contact = contact_ins,
                    )
                    contact_address.save()

                #***************************************************************
                # Account Details
                #***************************************************************

                if "is_contact_account_details" in fields and row["is_contact_account_details"] == "TRUE":
                    
                    contact_account_details = users_model.User_Account_Details(
                        is_user = False,
                        contact = contact_ins,
                        account_number = account_number,
                        account_holder_name = account_holder_name,
                        ifsc_code = ifsc_code,
                        bank_name = bank_name,
                        bank_branch_name = bank_branch_name,
                    )
                    contact_account_details.save()

                #***************************************************************
                # Tax Details
                #***************************************************************
                if "is_contact_tax_details" in fields and row["is_contact_tax_details"] == "TRUE":
                    try:
                        tax_details = User_Tax_Details.objects.get(contact = contact_ins)

                        tax_details.pan = pan
                        tax_details.gstin = gstin
                        tax_details.gst_reg_type = gst_reg_type
                        tax_details.business_reg_no = business_reg_no
                        tax_details.tax_reg_no = tax_reg_no
                        tax_details.cst_reg_no = cst_reg_no
                        tax_details.preferred_currency = preferred_currency
                        tax_details.opening_balance = opening_balance
                        tax_details.as_of = as_of
                        tax_details.preferred_payment_method = preferred_payment_method
                        tax_details.preferred_delivery = preferred_delivery
                        tax_details.invoice_terms = invoice_terms
                        tax_details.bills_terms = bills_terms

                    except:
                        tax_details = User_Tax_Details(
                            is_user = False,
                            contact = contact_ins,
                            pan = pan,
                            gstin = gstin,
                            gst_reg_type = gst_reg_type,
                            business_reg_no = business_reg_no,
                            tax_reg_no = tax_reg_no,
                            cst_reg_no = cst_reg_no,
                            preferred_currency = preferred_currency,
                            opening_balance = opening_balance,
                            as_of = as_of,
                            preferred_payment_method = preferred_payment_method,
                            preferred_delivery = preferred_delivery,
                            invoice_terms = invoice_terms,
                            bills_terms = bills_terms,
                        )
                    
                    tax_details.save()

#===================================================================================================
# STATUS CHANGE
#===================================================================================================
#
def status_change(request, slug = None, ins = None):
    
    if slug is not None and ins is not None:
        try:
            contact = Contacts.objects.get(pk = int(ins))        
        except:
           return redirect('/unauthorized/', permanent=False)

        if slug == 'deactivate':
            contact.is_active = False
        elif slug == 'activate':
            contact.is_active = True
        else:
            return redirect('/unauthorized/', permanent=False)

        contact.save()
        return redirect('/contacts/', permanent=False)

    return redirect('/unauthorized/', permanent=False)


#===================================================================================================
# DELETE CHANGE
#===================================================================================================
#

def delete_contact(request, ins = None):
    if ins is not None:
        try:
            contact = Contacts.objects.get(pk = int(ins))
            contact.contact_delete_status = 1
            contact.save()
        except:
            return redirect('/unauthorized/', permanent=False)

        return redirect('/contacts/', permanent=False)
    return redirect('/unauthorized/', permanent=False)

        
#===================================================================================================
# DELETE ADDRESS
#===================================================================================================
#

def delete_contact_address(request, ins = None):
    if ins is not None:
        try:
            users_model.User_Address_Details.objects.get(pk = int(ins)).delete()
        except:
            return HttpResponse(0)
        
        return HttpResponse(1)
    return HttpResponse(1)
        
#===================================================================================================
# DELETE ADDRESS
#===================================================================================================
#

def delete_accounts_details(request, ins = None):     
    if ins is not None:
        try:
            users_model.User_Account_Details.objects.get(pk = int(ins)).delete()
        except:
            return HttpResponse(0)
        
        return HttpResponse(1)
    return HttpResponse(1)

#===================================================================================================
# SEARCH CONTACTS
#===================================================================================================
#