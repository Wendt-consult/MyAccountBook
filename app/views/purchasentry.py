from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse
from django.views import View
from collections import OrderedDict, defaultdict
from django.contrib import messages

from app.models.contacts_model import Contacts
from app.models.users_model import *
from app.models.products_model import *
from app.models.accounts_model import *
from app.models.purchase_model import *
from app.models.customize_model import *
from app.models.purchasentry_model import *
from app.models.payment_made_model import *

from app.forms.products_form import * 
from app.forms.contact_forms import * 
from app.forms.tax_form import *
from app.forms.inc_fomsets import *
from app.forms.accounts_ledger_forms import *


from app.other_constants import creditnote_constant
from app.other_constants import user_constants,country_list
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.db.models import Q
import datetime

import json, os, csv

from app.helpers import email_helper

from datetime import datetime,date

from django.conf import settings

#=====================================================================================
#   PURCHAS ENTRY VIEW
#=====================================================================================
#

class PurchaseEntry(View):

    # Template 
    template_name = 'app/app_files/purchase_entry/base.html'
    
    # Initialize 
    data = defaultdict()
    data["view"] = ""
    data["contacts"] = {}
    data["active_link"] = 'Purchase Entry'
    data["breadcrumb_title"] = 'PURCHASE ENTRY'
    data['type'] = 'view'
    # Custom CSS/JS Files For Inclusion into template
    data["css_files"] = []
    data["js_files"] = ['custom_files/js/customize_view.js']

    data["included_template"] = 'app/app_files/purchase_entry/view_purchase_entry.html'
    
    #
    #
    def get(self, request):        
        
        entry = purchasentry_model.PurchaseEntry.objects.filter(user = request.user,purchase_delete_status = 0)

        self.data["entry"] = entry
    
        # CUSTOMIZE VIEW CODE
        customize_entry = CustomizeModuleName.objects.filter(Q(user = request.user) & Q(customize_name = 7))
        if(len(customize_entry) != 0):
            view_purchase_entry = CustomizePurchaseEntryView.objects.get(customize_view_name = customize_entry[0].id)
            if(view_purchase_entry is not None):
                self.data['customize'] = view_purchase_entry
            else:
                self.data['customize'] = 'NA'
        else:
                self.data['customize'] = 'NA'
                
        return render(request, self.template_name, self.data)
#=====================================================================================
#   DELETE PURCHASE ENTRY
#=====================================================================================
#

def delete_purchase_entry(request, ins):
    if ins is not None:
        try:
            purchasentry_model.PurchaseEntry.objects.filter(pk = int(ins)).update(purchase_delete_status = 1)
        
        except:
            return redirect('/unauthorized/', permanent=False)

        # Purchase_Items.objects.filter(Q(user= request.user) & Q(purchase_item_list = purchase_order)).delete()
        # PurchaseOrder.objects.get(pk = int(ins)).delete()

        return redirect('/view_purchase_entry/', permanent=False)
    return redirect('/unauthorized/', permanent=False)
#=====================================================================================
#   ADD PURCHASE ENTRY
#=====================================================================================
#
def add_purchase_entry(request,ins,slug):

    # Initialize 
    data = defaultdict()

    # Template 
    template_name = 'app/app_files/purchase_entry/add_purchase_entry.html'
    
    # Custom CSS/JS Files For Inclusion into template
    data["css_files"] = []
    data["js_files"] = ['custom_files/js/purchsentry.js','custom_files/js/product.js','custom_files/js/contacts.js',]

    # Set link as active in menubar
    data["active_link"] = 'Purchase Entry'
    data["breadcrumb_title"] = 'PURCHASE ENTRY'
    data['type'] = 'add'
    
    # Product form
    data["add_product_images_form"] = ProductPhotosForm()
    data["add_product_form"] = ProductForm(request.user) 

    # contact Forms
    data["contact_form"] = ContactsForm()
    data["tax_form"] = TaxForm()
    data["other_details_form"] = OtherDetailsForm()
    data["social_form"] = ContactsExtraForm()
    data["new_address_form"] = EditAddressForm()

    # gst form
    data["gst_form"] = OrganisationTaxForm()

    # FORMSETS    
    data["address_formset"] = AddressFormset
    data["accounts_formset"] = AccountsFormset

    # ACCOUNT_LEDGER FORMS
    data["groups_form"] = AccGroupsForm()

    # constant
    data['gst_code'] = country_list.GST_STATE_CODE
     # list contact name
    contacts = Contacts.objects.filter(Q(user = request.user) & Q(is_active = True) & Q(contact_delete_status = 0))
    gst = users_model.OrganisationGSTSettings.objects.filter(user = request.user)
    
    # default_term_condition = Organisations.objects.filter(user = request.user)
    # if(len(default_term_condition) > 0):
    #     msg = default_term_condition[0].invoice_terms_and_condition
    #     purchase_notes = default_term_condition[0].invoice_note
    #     data['term_msg'] = msg
    #     data['pur_notes'] = purchase_notes

    data["contacts"] = contacts
    data['gst'] = gst 
    # data['country_code'] = user_constants.PHONE_COUNTRY_CODE
    data['payment_terms'] = payment_constants.PAYMENT_DAYS
    data['invoice_frequency'] = payment_constants.INVOICE_FREQUENCY
    data["state"] = country_list.STATE_LIST_CHOICES
    data['gst_r_type'] = user_constants.org_GST_REG_TYPE

    # list product name

    if( int(ins) == 1):
        # for product details
        products = ProductsModel.objects.filter(Q(user = request.user) & Q(is_active = True) & Q(product_delete_status = 0) & Q(product_type__in = [0,1] ))
        name = []
        ids =[]
        count = len(products)
        for i in range(0,count):
            if(products[i].hsn_code is not None):
                a = str(products[i].product_name)+' - ('+str(products[i].hsn_code)+')'
                name.append(a)
            else:
                name.append(products[i].product_name)
            ids.append(products[i].id)
        # 
        # for account_ledger details
        major_heads = accounts_model.MajorHeads.objects.get(major_head_name = 'Expense')
        acc_ledger_income = accounts_model.AccGroups.objects.filter(Q(user = request.user) & Q(major_head = major_heads))
        acc_group_name = []
        acc_ids =[]
        acc_count = len(acc_ledger_income)
        for i in range(0,acc_count):
            acc_group_name.append(acc_ledger_income[i].group_name)
            acc_ids.append(acc_ledger_income[i].id)

        # common dictionary
        data = {'products': name, 'ids': ids , 'acc_group_name':acc_group_name, 'acc_ids':acc_ids} 
        return JsonResponse(data)
    elif(int(ins) == 0):
        # for product details
        products = ProductsModel.objects.filter(Q(user = request.user) & Q(is_active = True) & Q(product_delete_status = 0) & Q(product_type__in = [0,1] ))
        data["products"] = products

        # 
        # for account_ledger details
        major_heads = accounts_model.MajorHeads.objects.get(major_head_name = 'Expense')
        acc_ledger_income = accounts_model.AccGroups.objects.filter(Q(user = request.user) & Q(major_head = major_heads))
        
        # link to purchase order to purchase entry
        if(slug != 'NA'):
            purchase_order = PurchaseOrder.objects.get(pk = int(slug))
            purchase_item = Purchase_Items.objects.filter(Q(user= request.user) & Q(purchase_item_list = purchase_order))
            intproducts = ProductsModel.objects.filter(Q(user = request.user))
            # for purchase order gst check active or inactive
            if(purchase_order.purchase_org_gst_num != ''):
                org_tax = users_model.User_Tax_Details.objects.get(user = request.user, gstin = purchase_order.purchase_org_gst_num)
                if(org_tax.is_active == True):
                    data['order_gst'] = 'active'
                else:
                    data['order_gst'] = 'inactive'
            else:
                data['order_gst'] = 'inactive'

            data['purchase_order'] = purchase_order
            data['purchase_item'] = purchase_item
            data['intproducts'] = intproducts
            data['item_count'] = len(purchase_item)
            data['link_purchase_order'] = 'yes'
        else:
            data['order_gst'] = 'inactive'
            data['link_purchase_order'] = 'no'
        # org gst number
        data['is_gst'] = 'no'
        data['is_signle_gst']  = 'no'
        data['org_gst_type'] = None
        org = Organisations.objects.get(user = request.user)

        org_gst_num = User_Tax_Details.objects.filter(organisation = org.id,is_active = True)

        data['org_id'] = org.id
        if(len(org_gst_num) == 1):
            data['is_signle_gst'] = 'yes'
            data['is_gst'] = org_gst_num[0].gstin
            data['org_gst_type'] = org_gst_num[0].gst_reg_type
        elif(len(org_gst_num) > 0):
            default = org_gst_num.filter(default_gstin = True,is_active = True)
            if(len(default) != 0):
                data['is_gst'] = default[0].gstin
                data['org_gst_type'] = default[0].gst_reg_type
            else:
                data['is_gst'] = org_gst_num[0].gstin
                data['org_gst_type'] = org_gst_num[0].gst_reg_type

        data['acc_ledger_income'] = acc_ledger_income
        return render(request, template_name, data)

#=====================================================================================
#   CHECK PURCHASE_ENTRY UNIQUR AND SET DEFULT
#=====================================================================================
#

def unique_entry_number(request, ins, number):
    data = defaultdict()
    if(ins == 0):
        entry = purchasentry_model.PurchaseEntry.objects.filter(user = request.user)

        count = len(entry)

        if(count == 0):
            data['entry_number'] = 'PE-0001'
        else:
            inc = count+1
            for i in range(0,count):
                a = 'PE-000'+str(inc)
                result = entry.filter(Q(user = request.user) & Q(purchase_entry_number__iexact = a)).exists() 
                if(result == True):
                    inc += 1
                elif(result == False):
                    data['entry_number'] = 'PE-000'+str(inc)
                    break
        
        return JsonResponse(data)
    elif (ins == 1):
        # check purchase entry number is unique
        entry = PurchaseEntry.objects.filter(Q(user = request.user) & Q(purchase_entry_number = number))
        count = len(entry)
        if(count == 0):
            data['unique'] = 0
        else:
            data['unique'] = 1
        return JsonResponse(data)

#=====================================================================================
#   SAVE PURCHASE_ENTRY
#=====================================================================================
#

def save_purchase_entry(request):

    if request.POST:

        pe_number = request.POST.get("purchase_entry_number")
        check_pe_number = request.POST.get("auto_entry_number","off")
        pe_vendor = request.POST.get("entry_vendor")
        pay_terms = request.POST.get("entry_pay_terms")
        pe_date = request.POST.get("purchase_entry_date")
        # change purchase entry date formate
        if(pe_date != ''):
            pe_date = datetime.strptime(str(pe_date), '%d-%m-%Y').strftime('%Y-%m-%d')

        pe_reference = request.POST.get("purchase_entry_ref")
        pe_due_date = request.POST.get("purchase_entry_due_date")
        # change purchase entry due date formate
        if(pe_due_date != ''):
            pe_due_date = datetime.strptime(str(pe_due_date), '%d-%m-%Y').strftime('%Y-%m-%d')
       
        message = request.POST.get("entry_notes")
        attachement = request.FILES.get("Attachment")
        subtotal = request.POST.get("SubTotal")
        distotal = request.POST.get("purchase_Discountotal")
        cgst = request.POST.get("CGST")
        sgst = request.POST.get("SGST")
        igst = request.POST.get("IGST")
        total_amount = request.POST.get("Total")
        purchase_order_connect = request.POST.get("purchase_order_connect")
        
        # for invoice gst number and type
        org_gst_number = request.POST.get("org_gst_number")
        org_gst_reg_type = request.POST.get("org_gst_reg_type")
        single_gst_code = request.POST.get("single_gst_code")

        # is_tc = request.POST.get('invoice_t&c','off')
        # is_notes = request.POST.get('invoice_default_notes','off')

        # if(is_tc == 'on'):
        #     org = Organisations.objects.get(user = request.user)
        #     if(org.invoice_terms_and_condition is None):
        #         org.invoice_terms_and_condition = term_condition
        #         org.save()
        #     elif(org.invoice_terms_and_condition is not None):
        #         Organisations.objects.get(user = request.user).update(invoice_terms_and_condition = term_condition)

        # if(is_notes == 'on'):
        #     org = Organisations.objects.get(user = request.user)
        #     if(org.invoice_note is None):
        #         org.invoice_note = message
        #         org.save()
        #     elif(org.invoice_note is not None):
        #         Organisations.objects.get(user = request.user).update(invoice_note = message)

        if 'save_close' in request.POST:
            save_type = 1
        elif 'save_draft' in request.POST:
            save_type = 2

        contact = Contacts.objects.get(user = request.user, pk = int(pe_vendor))

        entry = purchasentry_model.PurchaseEntry(
            user = request.user, 
            vendor = contact, 
            purchase_entry_number = pe_number,
            purchase_number_check = check_pe_number,
            save_type=save_type,
            purchase_entry_date = pe_date,
            purchase_entry_refrence = pe_reference,
            purchase_entry_pay_terms = pay_terms,
            Note = message,
            attachements=attachement,
            sub_total = subtotal,
            total_discount = distotal,
            total_balance = total_amount,    
            cgst = cgst,
            sgst = sgst,
            igst = igst,
            purchase_org_gst_num = org_gst_number,
            purchase_org_gst_type = org_gst_reg_type,
            purchase_org_gst_state = single_gst_code,
            )
        if(cgst != '' or sgst != ''):
            entry.is_cs_gst = True
        elif(igst != ''):
            entry.is_cs_gst = False

        if(pe_due_date != ''):
            entry.purchase_entry_due_date = pe_due_date
            
        if(purchase_order_connect == 'yes'):
            entry.freight_charges = request.POST.get("Freight_Charges")
            entry.advance = request.POST.get("entry_advance")
            entry.connect_purchase_order = 'YES'
            purchase_order = PurchaseOrder.objects.get(pk = int(request.POST.get("purchase_order_id")))
            entry.purchase_order = purchase_order
            advance = request.POST.get("entry_advance")
            if(advance != '' and advance != None):
                a = float(total_amount) + float(advance)
                entry.total = round(a,2)
                entry.balance_due = total_amount
        else:
            entry.total = total_amount

        #  for payment status
        current_date = date.today()
        due = datetime.strptime(pe_due_date, '%Y-%m-%d').date()
        if(due < current_date):
            delta = (current_date - due).days
            entry.entry_status = 1
            entry.entry_date_count = delta
        else:
            entry.entry_status = 0

        entry.save()               

        product_name = request.POST.getlist('ItemName[]',None)
        product_desc = request.POST.getlist('desc[]',None)
        account_ids = request.POST.getlist('product_account[]',None)
        product_price = request.POST.getlist('Price[]',None)
        product_unit = request.POST.getlist('Unit[]',None)
        product_quantity = request.POST.getlist('Quantity[]',None)
        product_discount = request.POST.getlist('Discount[]',None)
        product_discount_type = request.POST.getlist('Dis[]',None)
        product_tax = request.POST.getlist('tax[]')
        product_cgst = request.POST.getlist('row_cgst[]',None)
        product_sgst = request.POST.getlist('row_sgst[]',None)
        product_igst = request.POST.getlist('row_igst[]',None)
        product_amount = request.POST.getlist('Amount[]',None)
        product_amount_inc = request.POST.getlist('Amount_inc[]',None)

        count = len(product_name)
        for i in range(0,count):

            if(product_quantity[i] != ''):
                products = ProductsModel.objects.get(pk = int(product_name[i]))
                account = accounts_model.AccGroups.objects.get(pk = int(account_ids[i]))
                entry_item = PurchaseEntryItems(
                    user= request.user,
                    purchase_entry_list = entry,
                    product = products,
                    description=product_desc[i],
                    account=account,
                    price=product_price[i],
                    unit=product_unit[i],
                    quantity=product_quantity[i],
                    discount_type = product_discount_type[i],
                    discount=product_discount[i],
                    tax=product_tax[i],
                    cgst_amount = product_cgst[i],
                    sgst_amount = product_sgst[i],
                    igst_amount = product_igst[i],
                    amount=product_amount[i],
                    amount_inc = product_amount_inc[i],
                )
                entry_item.save()  

                # for create make payment if some advance given
                if(entry.balance_due !='' and entry.balance_due is not None):
                    createPayment(request, entry)

        return redirect('/view_purchase_entry/', permanent = False)
#=====================================================================================
#   MAKE PAYMENT
#=====================================================================================
#

def createPayment(request, entry = None):
    payment_count = PurchasePayment.objects.filter(user = request.user).count()
    payment_number = None
    if(payment_count > 0 ):
        payment_number = 'PM-000'+str(payment_count + 1)
    else:
        payment_number = 'PM-0001'

    if entry is not None:
        payment = PurchasePayment(
            user = request.user,
            purchase_entry_reference = entry,
            vendor = entry.vendor,
            payment_number = payment_number,
            payment_reference = entry.purchase_entry_refrence,
            Note = entry.Note,
            attachements = entry.attachements,
            Amount = entry.advance,
        )

        if(entry.purchase_order.advance_payment_date != None):
            payment.payment_date = entry.purchase_order.advance_payment_date 
        if(entry.purchase_order.advacne_payment_method != ''):
            payment.payment_mode = int(entry.purchase_order.advacne_payment_method)

        payment.save()

#=====================================================================================
#   EDIT PURCHASE ENTRY
#=====================================================================================
#
class EditPurchaseEntry(View):

    # Initialize 
    data = defaultdict()

    # Template 
    template_name = 'app/app_files/purchase_entry/edit_purchase_entry.html'
    
    # Custom CSS/JS Files For Inclusion into template
    data["css_files"] = []
    data["js_files"] = ['custom_files/js/purchsentry.js','custom_files/js/product.js','custom_files/js/contacts.js',]

    # Set link as active in menubar
    data["active_link"] = 'Purchase Entry'
    data["breadcrumb_title"] = 'PURCHASE ENTRY'
    data['type'] = 'edit'

    # contact Forms
    data["contact_form"] = ContactsForm()
    data["tax_form"] = TaxForm()
    data["other_details_form"] = OtherDetailsForm()
    data["social_form"] = ContactsExtraForm()
    data["new_address_form"] = EditAddressForm()

    # FORMSETS    
    data["address_formset"] = AddressFormset
    data["accounts_formset"] = AccountsFormset

    # gst form
    data["gst_form"] = OrganisationTaxForm()

    # ACCOUNT_LEDGER FORMS
    data["groups_form"] = AccGroupsForm()

    data['country_code'] = user_constants.PHONE_COUNTRY_CODE

    # constant
    data['gst_code'] = country_list.GST_STATE_CODE

    def get(self, request, *args, **kwargs):

        try:
            entry = purchasentry_model.PurchaseEntry.objects.get(pk = int(kwargs["ins"]))
            contacts = Contacts.objects.filter(Q(user = request.user) & Q(is_active = True) & Q(contact_delete_status = 0))

            # inactive and delete product or contact
            intcontacts = Contacts.objects.filter(Q(user = request.user))
            intproducts = ProductsModel.objects.filter(Q(user = request.user))
                
            products = ProductsModel.objects.filter(Q(user = request.user) & Q(is_active = True) & Q(product_delete_status = 0))
            entry_item = purchasentry_model.PurchaseEntryItems.objects.filter(Q(user= request.user) & Q(purchase_entry_list = entry))

            major_heads = accounts_model.MajorHeads.objects.get(major_head_name = 'Expense')
            acc_ledger_income = accounts_model.AccGroups.objects.filter(Q(user = request.user) & Q(major_head = major_heads))
            gst = users_model.OrganisationGSTSettings.objects.filter(user = request.user)
    
        except:
            return redirect('/unauthorized/', permanent=False)

        self.data["contacts"] = contacts
        self.data['gst'] = gst

        # inactive and delete product or contact
        self.data["intproducts"] = intproducts
        self.data["intcontacts"] = intcontacts

        self.data["products"] = products
        self.data["entry"] = entry
        self.data["entry_item"] = entry_item
        self.data['acc_ledger_income'] = acc_ledger_income
        self.data["item_count"] = len(entry_item)

        self.data['payment_terms'] = payment_constants.PAYMENT_DAYS

        self.data["state"] = country_list.STATE_LIST_CHOICES

        # Product form
        self.data["add_product_images_form"] = ProductPhotosForm()
        self.data["add_product_form"] = ProductForm(request.user) 

        return render(request, self.template_name, self.data)

    #
    #
    #
    def post(self, request, *args, **kwargs):
        try:
            entry = purchasentry_model.PurchaseEntry.objects.get(pk = int(kwargs["ins"]))
            entry_item = purchasentry_model.PurchaseEntryItems.objects.filter(Q(user= request.user) & Q(purchase_entry_list = entry))
            
        except:
            # pass
            return redirect('/unauthorized/', permanent=False)

        if request.method == 'POST':
            pe_number = request.POST.get("purchase_entry_number")
            check_pe_number = request.POST.get("auto_entry_number","off")
            pe_vendor = request.POST.get("entry_vendor")
            pay_terms = request.POST.get("entry_pay_terms")
            pe_date = request.POST.get("purchase_entry_date")
            # change purchase entry date formate
            if(pe_date != ''):
                pe_date = datetime.strptime(str(pe_date), '%d-%m-%Y').strftime('%Y-%m-%d')

            pe_reference = request.POST.get("purchase_entry_ref")
            pe_due_date = request.POST.get("purchase_entry_due_date")
            # change purchase entry due date formate
            if(pe_due_date != ''):
                pe_due_date = datetime.strptime(str(pe_due_date), '%d-%m-%Y').strftime('%Y-%m-%d')
        
            message = request.POST.get("entry_notes")
            attachement = request.FILES.get("Attachment")
            subtotal = request.POST.get("SubTotal")
            distotal = request.POST.get("purchase_Discountotal")
            cgst = request.POST.get("CGST")
            sgst = request.POST.get("SGST")
            igst = request.POST.get("IGST")
            total_amount = request.POST.get("Total")
            # for invoice gst number and type
            org_gst_number = request.POST.get("org_gst_number")
            org_gst_reg_type = request.POST.get("org_gst_reg_type")
            single_gst_code = request.POST.get("single_gst_code")

            if 'save_close' in request.POST:
                save_type = 1
            elif 'save_draft' in request.POST:
                save_type = 2

            contact = Contacts.objects.get(user = request.user, pk = int(pe_vendor))

            purchasentry_model.PurchaseEntry.objects.filter(pk = int(kwargs["ins"])).update(
                user = request.user, 
                vendor = contact, 
                purchase_entry_number = pe_number,
                purchase_number_check = check_pe_number,
                save_type=save_type,
                purchase_entry_date = pe_date,
                purchase_entry_refrence = pe_reference,
                purchase_entry_pay_terms = pay_terms,
                Note = message,
                attachements=attachement,
                sub_total = subtotal,
                total_discount = distotal,
                total_balance = total_amount,    
                cgst = cgst,
                sgst = sgst,
                igst = igst,
                purchase_org_gst_num = org_gst_number,
                purchase_org_gst_type = org_gst_reg_type,
                purchase_org_gst_state = single_gst_code
                )
            if(cgst != '' or sgst != ''):
                purchasentry_model.PurchaseEntry.objects.filter(pk = int(kwargs["ins"])).update(is_cs_gst = True)
            elif(igst != ''):
                purchasentry_model.PurchaseEntry.objects.filter(pk = int(kwargs["ins"])).update(is_cs_gst = False)

            if(pe_due_date != ''):
                purchasentry_model.PurchaseEntry.objects.filter(pk = int(kwargs["ins"])).update(purchase_entry_due_date = pe_due_date)

            advance = request.POST.get("entry_advance")

            if(advance != '' and advance != None):
                a = float(total_amount) + float(advance)
                purchasentry_model.PurchaseEntry.objects.filter(pk = int(kwargs["ins"])).update(total = round(a,2), balance_due = total_amount)
            else:
                purchasentry_model.PurchaseEntry.objects.filter(pk = int(kwargs["ins"])).update(total = total_amount)

            #  for payment status
            current_date = date.today()

            due = datetime.strptime(pe_due_date, '%Y-%m-%d').date()
            if(due < current_date):
                delta = (current_date - due).days
                purchasentry_model.PurchaseEntry.objects.filter(pk = int(kwargs["ins"])).update(entry_status = 1,entry_date_count = delta)
            else:
                 purchasentry_model.PurchaseEntry.objects.filter(pk = int(kwargs["ins"])).update(entry_status = 0)

            product_name = request.POST.getlist('ItemName[]',None)
            product_desc = request.POST.getlist('desc[]',None)
            account_ids = request.POST.getlist('product_account[]',None)
            product_price = request.POST.getlist('Price[]',None)
            product_unit = request.POST.getlist('Unit[]',None)
            product_quantity = request.POST.getlist('Quantity[]',None)
            product_discount = request.POST.getlist('Discount[]',None)
            product_discount_type = request.POST.getlist('Dis[]',None)
            product_tax = request.POST.getlist('tax[]',None)
            product_cgst = request.POST.getlist('row_cgst[]',None)
            product_sgst = request.POST.getlist('row_sgst[]',None)
            product_igst = request.POST.getlist('row_igst[]',None)
            product_amount = request.POST.getlist('Amount[]',None)
            product_amount_inc = request.POST.getlist('Amount_inc[]',None)

            purchasentry_model.PurchaseEntryItems.objects.filter(Q(user= request.user) & Q(purchase_entry_list = entry)).delete()

            count = len(product_name)
            for i in range(0,count):

                if(product_quantity[i] != ''):
                    products = ProductsModel.objects.get(pk = int(product_name[i]))
                    account = accounts_model.AccGroups.objects.get(pk = int(account_ids[i]))
                    entry_item = purchasentry_model.PurchaseEntryItems(
                        user= request.user,
                        purchase_entry_list = entry,
                        product = products,
                        description=product_desc[i],
                        account=account,
                        price=product_price[i],
                        unit=product_unit[i],
                        quantity=product_quantity[i],
                        discount_type = product_discount_type[i],
                        discount=product_discount[i],
                        tax=product_tax[i],
                        cgst_amount = product_cgst[i],
                        sgst_amount = product_sgst[i],
                        igst_amount = product_igst[i],
                        amount=product_amount[i],
                        amount_inc = product_amount_inc[i],
                    )
                    entry_item.save()

        return redirect('/view_purchase_entry/', permanent = False)
