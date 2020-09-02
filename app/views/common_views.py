from django.http import HttpResponse, Http404, JsonResponse
from django.views import View
from collections import OrderedDict, defaultdict
from django.contrib import messages

from django.shortcuts import redirect, render

from django.conf import settings

from django.db.models import *

from app.models.invoice_model import *
from app.models.collects_model import *
from app.models.products_model import *
from app.models.users_model import *
from app.models.contacts_model import *
from app.models.customize_model import *

from app.forms.invoice_forms import *
from app.forms.products_form import *
from app.forms.contact_forms import *
from app.forms.tax_form import *

from app.other_constants import country_list

import json


#**********************************************************************************************
# FETCH CONTACT BILLING/SHIPPING ADDRESSES 
#**********************************************************************************************
#

def fetch_contact_addresses(request, ins=None):

    data = {'ret':0, 'organization_name':'', 'addresses':{}}

    if ins is not None:

        try:
            contact = Contacts.objects.get(pk = int(ins))
        except:
            return HttpResponse(json.dumps(data))

        contact_addresses = Contact_Addresses.objects.filter(contact = contact).values('id','contact_person', 
            'flat_no', 'street', 'city', 'state', 'country', 'pincode', 'is_billing_address', 
            'is_shipping_address')
        
        data['ret'] = 1
        data['organization_name'] = contact.organization_name
        data['addresses'] = list(contact_addresses)        
        return HttpResponse(json.dumps(data))
    return HttpResponse(json.dumps(data))


#**********************************************************************************************
# FETCH PRODUCTS  
#**********************************************************************************************
#

def fetch_products(request):
    products = ProductsModel.objects.filter(user = request.user).values()
    return HttpResponse(json.dumps(products))

def fetch_products_dropdown(request):
    products = ProductsModel.objects.filter(user = request.user).values('id', 'product_name')
    
    html = ['<option></option>']

    for row in products:
        html.append('<option value="{}">{}</option>'.format(row["id"], row["product_name"]))

    return HttpResponse(''.join(html))


#**********************************************************************************************
# FETCH PRODUCT DETAILS
#**********************************************************************************************
#

def fetch_product_details(request, ins=None):
    data = {'ret':0, 'details':{}, 'quantity_in_stock':0}

    if ins is not None:
        
        product = ProductsModel.objects.filter(pk = int(ins)).values()
        data['details'] = list(product)
        
        p_count = InventoryProduct.objects.filter(product = product[0]["id"]).aggregate(total = Sum('quantity'))
        data['quantity_in_stock'] = p_count["total"]     
        data['product_type'] = items_constant.PRODUCT_TYPE_DICT[product[0]["product_type"]]   

        return HttpResponse(json.dumps(data))
    return HttpResponse(json.dumps(data))


#**********************************************************************************************
# ADD CONTACT 
#**********************************************************************************************
#

def add_contact_or_employee(request):

    if request.POST:
        contact_form = ContactsForm(request.POST)
        tax_form = TaxForm(request.POST)        
        contact_address_form_1 = ContactsAddressForm(request.POST, prefix = 'form1')
        contact_address_form_2 = ContactsAddressForm(request.POST, prefix = 'form2')
        contact_account_details_form = ContactAccountDetailsForm(request.POST)

        ins = None

        if contact_form.is_valid():

            ins = contact_form_ins = contact_form.save(commit = False)
            contact_form_ins.user = request.user

            if contact_form_ins.is_imported_user:
                try:
                    profile = Profile.objects.get(app_id__iexact = contact_form_ins.app_id)
                    imp_user = User.objects.get(pk = profile.user_id)
                except:
                    return HttpResponse(0)
                
                contact_form_ins.imported_user = imp_user
            
            social_form = ContactsExtraForm(request.POST, request.FILES, instance = contact_form_ins)
            if social_form.is_valid():
                social_form.save()

            contact_form_ins.save() 

        if ins is not None:
            #
            # tax form save
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
            # contact_account_details_form save
            if contact_account_details_form.is_valid():
                obj_acc = contact_account_details_form.save(commit = False)
                obj_acc.contact = ins
                obj_acc.save() 
            else:
                pass
            
            #
            # address form save
            if contact_address_form_1.is_valid():
                obj_add1 = contact_address_form_1.save(commit = False)
                obj_add1.contact = ins
                obj_add1.save() 
            else:
                pass

            #
            # address 2 form save
            if contact_address_form_2.is_valid():
                x = request.POST.get("more_address_table_enabled", None)
                if x == '1' and x is not None:
                    obj_add2 = contact_address_form_2.save(commit = False)
                    obj_add2.contact = ins
                    obj_add2.save() 
            else:
                pass

            return HttpResponse(1)
        return HttpResponse(0)
    return HttpResponse(0)
    
#**********************************************************************************************
# FETCH CONTACTS IN A DROPDOWN 
#**********************************************************************************************
#

def get_contacts_dropdown(request):

    contacts = Contacts.objects.filter(user = request.user).values()

    html = ['<option></option>']

    for row in contacts:
        html.append('<option value="{}">{}</option>'.format(row["id"], row["contact_name"]))

    return HttpResponse(''.join(html))


#**********************************************************************************************
# ADD/EDIT ADDRESS FOR A CONTACT 
#**********************************************************************************************
#

def add_edit_address(request, ins = None, obj = None):

    if ins is not None:
        try:
            contact = Contacts.objects.get(pk = int(ins))
        except:
            return HttpResponse(0)

        if obj is not None:
            try:
                address = Contact_Addresses.objects.get(pk = int(obj))
            except:
                return HttpResponse(0)            

            address_form = ContactsAddressForm( request.POST, instance = address, prefix = 'form3')

            if address_form.is_valid():
                address_form.save()
                return HttpResponse(1)        
        else:
            address_form = ContactsAddressForm(request.POST, prefix = 'form3')

            if address_form.is_valid():
                add_f = address_form.save(commit = False)
                add_f.contact = contact
                add_f.save()
                return HttpResponse(1)

            return HttpResponse(2)    
        return HttpResponse(4)
    
    return HttpResponse(0)
 
 
#**********************************************************************************************
# CUSTOMIZE VIEW LIST
#**********************************************************************************************
#
def customize_view_list(request, ins):
    
    data = json.loads(request.POST.get('data'))
    customize_name = CustomizeModuleName.objects.filter(Q(user = request.user) & Q(customize_name = int(ins)))
    if(len(customize_name) != 0):
        if(ins == 1):
            CustomizeContactView.objects.filter(customize_view_name = customize_name[0].id).update(contact_name = data['name'],contact_org_name = data['org'],contact_email = data['mail'],
                                                contact_phone = data['phone'])
        elif(ins == 2):
            CustomizeProductView.objects.filter(customize_view_name = customize_name[0].id).update(product_sku = data['sku'],product_type = data['type'],product_name = data['name'],
                                                product_hsn = data['hsn'],product_description = data['desc'],product_selling_price = data['selling'],product_Purchase_price = data['purchase'])
        elif(ins == 3):
            CustomizeCreditView.objects.filter(customize_view_name = customize_name[0].id).update(credit_note = data['note'],credit_name = data['name'],credit_reference = data['reference'],
                                                credit_date = data['date'],credit_amount = data['amount'])
        elif(ins == 4):
            CustomizePurchaseView.objects.filter(customize_view_name = customize_name[0].id).update(purchase_number = data['number'],purchase_reference = data['reference'],purchase_vendor = data['vendor'],
                                                purchase_status = data['status'],purchase_total = data['total'],purchase_date = data['date'])
        elif(ins == 5):
            CustomizeInvoiceView.objects.filter(customize_view_name = customize_name[0].id).update(invoice_number = data['number'],invoice_customer = data['customer'],invoice_date = data['date'],
                                                invoice_due_date = data['due_date'],invoice_status = data['status'],invoice_amount = data['amount'])
        elif(ins == 6):
            CustomizeExpenseView.objects.filter(customize_view_name = customize_name[0].id).update(expense_vocher = data['vocher'],expense_date = data['date'],expense_vendor = data['vendor'],expense_payment = data['payment'],
                                                expense_method = data['method'],expense_amount = data['amount'])
        elif(ins == 7):
            CustomizePurchaseEntryView.objects.filter(customize_view_name = customize_name[0].id).update(entry_number = data['number'],entry_reference = data['reference'],entry_vendor = data['vendor'],
                                                entry_date = data['date'], entry_due_date = data['due_date'], entry_advance = data['advance'], entry_total = data['amount'])
    elif(len(customize_name) == 0):
        customize_module_name = CustomizeModuleName(user = request.user, customize_name = int(ins))
        customize_module_name.save()
        if(ins == 1):
            view_contact = CustomizeContactView(customize_view_name = customize_module_name,contact_name = data['name'],contact_org_name = data['org'],contact_email = data['mail'],
                                                contact_phone = data['phone'])
            view_contact.save()
        elif(ins == 2):
            view_product = CustomizeProductView(customize_view_name = customize_module_name,product_sku = data['sku'],product_type = data['type'],product_name = data['name'],
                                                product_hsn = data['hsn'],product_description = data['desc'],product_selling_price = data['selling'],product_Purchase_price = data['purchase'])
            view_product.save()
        elif(ins == 3):
            view_credit = CustomizeCreditView(customize_view_name = customize_module_name,credit_note = data['note'],credit_name = data['name'],credit_reference = data['reference'],
                                            credit_date = data['date'],credit_amount = data['amount'])
            view_credit.save()
        elif(ins == 4):
            view_purchase = CustomizePurchaseView(customize_view_name = customize_module_name,purchase_number = data['number'],purchase_reference = data['reference'],purchase_vendor = data['vendor'],
                                                purchase_status = data['status'],purchase_total = data['total'],purchase_date = data['date'])
            view_purchase.save()
        elif(ins == 5):
            view_invoice = CustomizeInvoiceView(customize_view_name = customize_module_name,invoice_number = data['number'],invoice_customer = data['customer'],invoice_date = data['date'],
                                                invoice_due_date = data['due_date'],invoice_status = data['status'],invoice_amount = data['amount'])
            view_invoice.save()
        elif(ins == 6):
            view_expense = CustomizeExpenseView(customize_view_name = customize_module_name,expense_vocher = data['vocher'],expense_date = data['date'],expense_vendor = data['vendor'],expense_payment = data['payment'],
                                                expense_method = data['method'],expense_amount = data['amount'])
            view_expense.save()
        elif(ins == 7):
            view_purchase_entry = CustomizePurchaseEntryView(customize_view_name = customize_module_name,entry_number = data['number'],entry_reference = data['reference'],entry_vendor = data['vendor'],
                                                entry_date = data['date'], entry_due_date = data['due_date'], entry_advance = data['advance'], entry_total = data['amount'])
            view_purchase_entry.save()
    return JsonResponse(data)

#**********************************************************************************************
#  GET GST NUMBER OF CGST SGST AND IGST
#**********************************************************************************************
#

def get_gst_number(request):
    # Initialize 
    data = defaultdict()
    data['gst_number'] = []
    data['gst_type'] = []
    org = Organisations.objects.get(user = request.user)
    org_gst_num = User_Tax_Details.objects.filter(organisation = org.id,is_active=True)
    for i in range(0,len(org_gst_num)):
        data['gst_number'].append(org_gst_num[i].gstin)
        data['gst_type'].append(org_gst_num[i].gst_reg_type)
    return JsonResponse(data)