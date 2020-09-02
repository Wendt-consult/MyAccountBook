from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse
from django.views import View
from collections import OrderedDict, defaultdict
from django.contrib import messages

from app.models.contacts_model import Contacts
from app.models.users_model import *
from app.models.products_model import *
from app.models.accounts_model import *
# from app.models.purchase_model import *
from app.models.customize_model import *
from app.models.invoice_model import *

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
from datetime import datetime
import json, os, csv

from app.helpers import email_helper

from apscheduler.schedulers.background import BackgroundScheduler
from app.views.scheduler import test_fun
from django.conf import settings

#=====================================================================================
#   BACKGROUND RUNNING
#=====================================================================================
# 
sched = BackgroundScheduler()

# sched.add_job(test_fun, 'cron', hour=0)
sched.add_job(test_fun, 'interval', minutes=1)

sched.start()
#=====================================================================================
#   INVOICE VIEW
#=====================================================================================
# 


class Invoice(View):

    # Template 
    template_name = 'app/app_files/invoice/base.html'
    
    # Initialize 
    data = defaultdict()
    data["view"] = ""
    data["contacts"] = {}
    data["active_link"] = 'Invoice'
    data["breadcrumb_title"] = 'INVOICE'
    data['type'] = 'view'
    # Custom CSS/JS Files For Inclusion into template
    data["css_files"] = []
    data["js_files"] = ['custom_files/js/customize_view.js']

    data["included_template"] = 'app/app_files/invoice/view_invoice.html'
    
    #
    #
    def get(self, request):        
        
        invoice = invoice_model.InvoiceModel.objects.filter(user = request.user,invoice_delete_status=0)
        # invoice_paginator = Paginator(invoice, 10)
        # invoice_page = request.GET.get('page')     
        # try:
        #     invoice_posts = invoice_paginator.page(invoice_page)
        # except PageNotAnInteger:
        #     invoice_posts = invoice_paginator.page(1)
        # except EmptyPage:
        #     invoice_posts = invoice_paginator.page(invoice_paginator.num_pages)
        self.data["invoice"] = invoice
        # self.data["invoice_page"] = invoice_page
    
        # CUSTOMIZE VIEW CODE
        customize_invoice = CustomizeModuleName.objects.filter(Q(user = request.user) & Q(customize_name = 5))
        if(len(customize_invoice) != 0):
            view_invoice = CustomizeInvoiceView.objects.get(customize_view_name = customize_invoice[0].id)
            if(view_invoice is not None):
                self.data['customize'] = view_invoice
            else:
                self.data['customize'] = 'NA'
        else:
                self.data['customize'] = 'NA'
                
        return render(request, self.template_name, self.data)

#=====================================================================================
#   ADD INVOCE
#=====================================================================================
#
def add_invoice(request, slug):

    # Initialize 
    data = defaultdict()

    # Template 
    template_name = 'app/app_files/invoice/add_invoice.html'
    
    # Custom CSS/JS Files For Inclusion into template
    data["css_files"] = []
    data["js_files"] = ['custom_files/js/invoice.js','custom_files/js/product.js','custom_files/js/contacts.js',]

    # Set link as active in menubar
    data["active_link"] = 'Invoice'
    data["breadcrumb_title"] = 'INVOICE'
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
    
    default_term_condition = Organisations.objects.filter(user = request.user)
    if(len(default_term_condition) > 0):
        msg = default_term_condition[0].invoice_terms_and_condition
        purchase_notes = default_term_condition[0].invoice_note
        data['term_msg'] = msg
        data['pur_notes'] = purchase_notes

    data["contacts"] = contacts
    data['gst'] = gst 
    # data['country_code'] = user_constants.PHONE_COUNTRY_CODE
    data['payment_terms'] = payment_constants.PAYMENT_DAYS
    data['invoice_frequency'] = payment_constants.INVOICE_FREQUENCY
    data["state"] = country_list.STATE_LIST_CHOICES
    data['gst_r_type'] = user_constants.org_GST_REG_TYPE

    # list product name

    if( int(slug) == 1):
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
        major_heads = accounts_model.MajorHeads.objects.get(major_head_name = 'Income')
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
    elif(int(slug) == 0):
        # for product details
        products = ProductsModel.objects.filter(Q(user = request.user) & Q(is_active = True) & Q(product_delete_status = 0) & Q(product_type__in = [0,1] ))
        data["products"] = products

        # 
        # for account_ledger details
        major_heads = accounts_model.MajorHeads.objects.get(major_head_name = 'Income')
        acc_ledger_income = accounts_model.AccGroups.objects.filter(Q(user = request.user) & Q(major_head = major_heads))
        
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
#   CHECK PURCHASE_ORDER UNIQUR AND SET DEFULT
#=====================================================================================
#

def unique_invoice_number(request, ins, number):
    data = defaultdict()
    if(ins == 0):
        purchase_order = purchase_model.PurchaseOrder.objects.filter(user = request.user)

        count = len(purchase_order)

        if(count == 0):
            data['purchase_number'] = 'PO-0001'
        else:
            inc = count+1
            for i in range(0,count):
                a = 'PO-000'+str(inc)
                result = purchase_order.filter(Q(user = request.user) & Q(purchase_order_number__iexact = a)).exists() 
                if(result == True):
                    inc += 1
                elif(result == False):
                    data['purchase_number'] = 'PO-000'+str(inc)
                    break
        
        return JsonResponse(data)
    elif (ins == 1):
        # check credit note number is unquie
        purchase_order = purchase_model.PurchaseOrder.objects.filter(Q(user = request.user) & Q(purchase_order_number = number))
        count = len(purchase_order)
        if(count == 0):
            data['unique'] = 0
        else:
            data['unique'] = 1
        return JsonResponse(data)

def org_address_state(request):
    # Initialize 
    data = defaultdict()
    data['state'] = None
    org = users_model.Organisations.objects.get(user = request.user)
    org_address = users_model.User_Address_Details.objects.filter(Q(is_user = True) & Q(is_organisation = True) & Q(organisation = org) & Q(default_address = True))
    if(len(org_address) != 0):
        data['state'] = org_address[0].get_state_display()
    else:
        first_address = users_model.User_Address_Details.objects.filter(Q(is_user = True) & Q(is_organisation = True) & Q(organisation = org))
        
        if(len(first_address) != 0):
            data['state'] = first_address[0].get_state_display()
    return JsonResponse(data)

#=====================================================================================
#   SAVE INVOICE
#=====================================================================================
#

def save_invoice(request):

    if request.POST:
        invoice_customer = request.POST.get("invoice_customer")
        email = request.POST.get("Email_Address")
        cc_email = request.POST.get("CC_Email_Address")
        invoice_number = request.POST.get("invoice_number")
        check_invocie_number = request.POST.get("auto_invoice_number","off")
        invoice_date = request.POST.get("Invoice_date")
        # change due date formate
        in_date = datetime.strptime(str(invoice_date), '%d-%m-%Y').strftime('%Y-%m-%d')

        invoice_purchae_number = request.POST.get("invoice_purchase_number")
        invoice_new = request.POST.get("one_radio","off")
        invoice_recurring = request.POST.get("recurring_radio","off")
        if(invoice_new == 'on'):
            pay_terms = request.POST.get("invoice_pay_terms")
            due_date = request.POST.get("Invoice_one_due_date")
            # change due date formate
            new_date = datetime.strptime(str(due_date), '%d-%m-%Y').strftime('%Y-%m-%d')
        elif(invoice_recurring == 'on'):
            invoice_start_date = request.POST.get("Invoice_recurring_start")
            # change recurring start date format
            recurring_start_date = datetime.strptime(str(invoice_start_date), '%d-%m-%Y').strftime('%Y-%m-%d')

            invoice_recurring_end = request.POST.get("Invoice_recurring_end")
            # change recurring end date format
            recurring_end_date = datetime.strptime(str(invoice_recurring_end), '%d-%m-%Y').strftime('%Y-%m-%d')

            invoice_Frequency = request.POST.get("invoice_recurring_Frequency")   
            invoice_repeat = request.POST.get("Invoice_recurring_repeat")       
            invoice_advance = request.POST.get("Invoice_recurring_advance")        

        invoice_employee = request.POST.get("invoice_seales_person")
        invoice_state_supply = request.POST.get("invoice_state_supply")
        term_condition = request.POST.get("invoice_MessageOnStatement")
        message = request.POST.get("invoice_notes")
        attachement = request.FILES.get("Attachment")
        subtotal = request.POST.get("SubTotal")
        distotal = request.POST.get("purchase_Discountotal")
        # subtotal = request.POST.get("SubTotal")
        cgst = request.POST.get("CGST")
        sgst = request.POST.get("SGST")
        igst = request.POST.get("IGST")

        # for invoice gst number and type
        org_gst_number = request.POST.get("org_gst_number")
        org_gst_reg_type = request.POST.get("org_gst_reg_type")
        single_gst_code = request.POST.get("single_gst_code")

        shipping_charges = request.POST.get("shipping_charges")
        total_amount = request.POST.get("Total")

        is_tc = request.POST.get('invoice_t&c','off')
        is_notes = request.POST.get('invoice_default_notes','off')

        if(is_tc == 'on'):
            org = Organisations.objects.get(user = request.user)
            if(org.invoice_terms_and_condition is None):
                org.invoice_terms_and_condition = term_condition
                org.save()
            elif(org.invoice_terms_and_condition is not None):
                Organisations.objects.get(user = request.user).update(invoice_terms_and_condition = term_condition)

        if(is_notes == 'on'):
            org = Organisations.objects.get(user = request.user)
            if(org.invoice_note is None):
                org.invoice_note = message
                org.save()
            elif(org.invoice_note is not None):
                Organisations.objects.get(user = request.user).update(invoice_note = message)

        if 'save_send' in request.POST:
            save_type = 1
        elif 'save_close' in request.POST:
            save_type = 2
        elif 'save_draft' in request.POST:
            save_type = 3
        elif 'save_print' in request.POST:
            save_type = 4
        elif 'save_new' in request.POST:
            save_type = 5

        contact = Contacts.objects.get(user = request.user, pk = int(invoice_customer))

        invoice = InvoiceModel(
            user = request.user, 
            invoice_customer = contact, 
            email = email,
            cc_email = cc_email, 
            purchase_order_number = invoice_purchae_number,
            invoice_number = invoice_number,
            invoice_check = check_invocie_number,
            save_type=save_type,
            invoice_date = in_date,
            invoice_type_new = invoice_new,
            invoice_type_recurring = invoice_recurring, 
            invoice_salesperson = invoice_employee,
            invoice_state_supply = invoice_state_supply,
            terms_and_condition = term_condition, 
            Note = message,
            attachements=attachement,
            sub_total = subtotal,
            total_discount = distotal,
            total_amount = total_amount,
            shipping_charges = shipping_charges,     
            cgst = cgst,
            sgst = sgst,
            igst = igst,
            invoice_org_gst_num = org_gst_number,
            invoice_org_gst_type = org_gst_reg_type,
            invoice_org_gst_state = single_gst_code,
       )
        if(cgst != '' or sgst != ''):
            invoice.is_cs_gst = True
        else:
            invoice.is_cs_gst = False
        if(invoice_new == 'on'):
            invoice.invoice_new_pay_terms = pay_terms
            invoice.invoice_new_due_date = new_date
        if(invoice_recurring == 'on'):
            invoice.invoice_recurring_start_date = recurring_start_date
            invoice.invoice_recurring_end_date = recurring_end_date
            invoice.invoice_recurring_repeat = invoice_repeat
            invoice.invoice_recurring_frequency = invoice_Frequency
            invoice.invoice_recurring_advance = invoice_advance
        invoice.save()               


        # igst = list(filter(None, [igst_5, igst_12, igst_18, igst_28, igst_other]))
        # cgst = list(filter(None, [cgst_5, cgst_12, cgst_18, cgst_28,cgst_other]))
        # sgst = list(filter(None, [sgst_5, sgst_12, sgst_18, sgst_28, sgst_other]))
        #print(igst, cgst, sgst)

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
        header_count = 1
        row_count = 1
        header = 0
        for i in range(0,count):

            if(product_quantity[i] != 'header'):
                if(header == 0):
                    products = ProductsModel.objects.get(pk = int(product_name[i]))
                    account = accounts_model.AccGroups.objects.get(pk = int(account_ids[i]))

                    invoice_item = Invoice_Line_Items(
                        user= request.user,
                        invoice_item_list = invoice,
                        is_header = False,
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
                        header_number_count = row_count,
                        # tax_amount = (float(product_tax[i])/100)*float(product_amount[i]), 
                        # igst_amount = float(igst[i]) if len(igst) > 0 else 0,
                        # cgst_amount = float(cgst[i]) if len(cgst) > 0 else 0,
                        # sgst_amount = float(sgst[i]) if len(sgst) > 0 else 0,
                    )
                else:
                    products = ProductsModel.objects.get(pk = int(product_name[i]))
                    account = accounts_model.AccGroups.objects.get(pk = int(account_ids[i-header]))

                    invoice_item = Invoice_Line_Items(
                        user= request.user,
                        invoice_item_list = invoice,
                        is_header = False,
                        product = products,
                        description=product_desc[i-header],
                        account=account,
                        price=product_price[i-header],
                        unit=product_unit[i-header],
                        quantity=product_quantity[i],
                        discount_type = product_discount_type[i-header],
                        discount=product_discount[i-header],
                        tax=product_tax[i-header],
                        cgst_amount = product_cgst[i-header],
                        sgst_amount = product_sgst[i-header],
                        igst_amount = product_igst[i-header],
                        amount=product_amount[i],
                        amount_inc = product_amount_inc[i-header],
                        header_number_count = row_count,
                        # header_number_count = row_count,
                        # tax_amount = (float(product_tax[i-header])/100)*float(product_amount[i]), 
                        # igst_amount = float(igst[i]) if len(igst) > 0 else 0,
                        # cgst_amount = float(cgst[i]) if len(cgst) > 0 else 0,
                        # sgst_amount = float(sgst[i]) if len(sgst) > 0 else 0,
                    )
                row_count += 1
            elif(product_quantity[i] == 'header'):
                invoice_item = Invoice_Line_Items(
                    user= request.user,
                    invoice_item_list = invoice,
                    is_header = True,
                    header_name = product_name[i],
                    header_subtotal=product_amount[i],
                    header_number_count = header_count
                )
                header_count += 1
                header += 1

            invoice_item.save()  


        if(save_type == 4):  
            invoice = InvoiceModel.objects.latest('pk')
            ins = '/invoice/print/'+str(invoice.id)+'/'
            return redirect(ins, permanent = False)
            

        if(save_type == 1):  
            invoice_mailer(request, invoice, contact)
        
        if(save_type == 5):
            ins = '/invoice/add/0/'
            return redirect(ins, permanent = False)

        return redirect('/invoice/', permanent = False)

#=====================================================================================
#   CHECK PURCHASE_ORDER UNIQUR AND SET DEFULT
#=====================================================================================
#

def unique_invoice_number(request, ins, number):
    data = defaultdict()
    if(ins == 0):
        invoice = InvoiceModel.objects.filter(user = request.user)

        count = len(invoice)

        if(count == 0):
            data['invoice_number'] = 'IN-0001'
        else:
            inc = count+1
            for i in range(0,count):
                a = 'IN-000'+str(inc)
                result = invoice.filter(Q(user = request.user) & Q(invoice_number__iexact = a)).exists() 
                if(result == True):
                    inc += 1
                elif(result == False):
                    data['invoice_number'] = 'IN-000'+str(inc)
                    break
        
        return JsonResponse(data)
    elif (ins == 1):
        invoice = InvoiceModel.objects.filter(Q(user = request.user) & Q(invoice_number = number))
        count = len(invoice)
        if(count == 0):
            data['unique'] = 0
        else:
            data['unique'] = 1
        return JsonResponse(data)


#=====================================================================================
#   EDIT CREDITNOTE 
#=====================================================================================
#
class EditInvoice(View):

    # Initialize 
    data = defaultdict()

    # Template 
    template_name = 'app/app_files/invoice/edit_invoice.html'
    
    # Custom CSS/JS Files For Inclusion into template
    data["css_files"] = []
    data["js_files"] = ['custom_files/js/invoice.js','custom_files/js/product.js','custom_files/js/contacts.js',]

    # Set link as active in menubar
    data["active_link"] = 'Invoice'
    data["breadcrumb_title"] = 'INVOICE'
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
            invoice = InvoiceModel.objects.get(pk = int(kwargs["ins"]))
            contacts = Contacts.objects.filter(Q(user = request.user) & Q(is_active = True) & Q(contact_delete_status = 0))

            # inactive and delete product or contact
            intcontacts = Contacts.objects.filter(Q(user = request.user))
            intproducts = ProductsModel.objects.filter(Q(user = request.user))
            
            products = ProductsModel.objects.filter(Q(user = request.user) & Q(is_active = True) & Q(product_delete_status = 0))
            invoice_item = Invoice_Line_Items.objects.filter(Q(user= request.user) & Q(invoice_item_list = invoice))

            major_heads = accounts_model.MajorHeads.objects.get(major_head_name = 'Income')
            acc_ledger_income = accounts_model.AccGroups.objects.filter(Q(user = request.user) & Q(major_head = major_heads))
            default_term_condition = Organisations.objects.filter(user = request.user)
            gst = users_model.OrganisationGSTSettings.objects.filter(user = request.user)
    
        except:
            return redirect('/unauthorized/', permanent=False)

        # invoice item without header
        invoice_row = invoice_item.filter(is_header = False)

        # invoice item with header
        invoice_row_header = invoice_item.filter(is_header = True)

        if(len(default_term_condition) > 0):
            msg = default_term_condition[0].invoice_terms_and_condition
            invoice_notes = default_term_condition[0].invoice_note
            self.data['term_msg'] = msg
            self.data['invoice_notes'] = invoice_notes

        self.data["contacts"] = contacts
        self.data['gst'] = gst

        # inactive and delete product or contact
        self.data["intproducts"] = intproducts
        self.data["intcontacts"] = intcontacts

        self.data["products"] = products
        self.data["invoice"] = invoice
        self.data["invoice_item"] = invoice_item
        self.data['acc_ledger_income'] = acc_ledger_income
        self.data["item_count"] = len(invoice_row)-1
        self.data['item_header_count'] = len(invoice_row_header)

        self.data['payment_terms'] = payment_constants.PAYMENT_DAYS
        self.data['invoice_frequency'] = payment_constants.INVOICE_FREQUENCY
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
            invoice = InvoiceModel.objects.get(pk = int(kwargs["ins"]))
            invoice_item = Invoice_Line_Items.objects.filter(Q(user= request.user) & Q(invoice_item_list = invoice))
            
        except:
            # pass
            return redirect('/unauthorized/', permanent=False)

        if request.method == 'POST':
            invoice_customer = request.POST.get("invoice_customer")
            email = request.POST.get("Email_Address")
            cc_email = request.POST.get("CC_Email_Address")
            invoice_number = request.POST.get("invoice_number")
            check_invocie_number = request.POST.get("auto_invoice_number","off")
            invoice_date = request.POST.get("Invoice_date")
            # change due date formate
            in_date = datetime.strptime(str(invoice_date), '%d-%m-%Y').strftime('%Y-%m-%d')

            invoice_purchae_number = request.POST.get("invoice_purchase_number")
            invoice_new = request.POST.get("one_radio","off")
            invoice_recurring = request.POST.get("recurring_radio","off")
            if(invoice_new == 'on'):
                pay_terms = request.POST.get("invoice_pay_terms")
                due_date = request.POST.get("Invoice_one_due_date")
                # change due date formate
                new_date = datetime.strptime(str(due_date), '%d-%m-%Y').strftime('%Y-%m-%d')
            elif(invoice_recurring == 'on'):
                invoice_start_date = request.POST.get("Invoice_recurring_start")
                # change recurring start date format
                recurring_start_date = datetime.strptime(str(invoice_start_date), '%d-%m-%Y').strftime('%Y-%m-%d')

                invoice_recurring_end = request.POST.get("Invoice_recurring_end")
                # change recurring end date format
                recurring_end_date = datetime.strptime(str(invoice_recurring_end), '%d-%m-%Y').strftime('%Y-%m-%d')

                invoice_Frequency = request.POST.get("invoice_recurring_Frequency")   
                invoice_repeat = request.POST.get("Invoice_recurring_repeat")       
                invoice_advance = request.POST.get("Invoice_recurring_advance")        

            invoice_employee = request.POST.get("invoice_seales_person")
            invoice_state_supply = request.POST.get("invoice_state_supply")
            term_condition = request.POST.get("invoice_MessageOnStatement")
            message = request.POST.get("invoice_notes")
            attachement = request.FILES.get("Attachment")
            subtotal = request.POST.get("SubTotal")
            distotal = request.POST.get("purchase_Discountotal")
            # subtotal = request.POST.get("SubTotal")
            cgst = request.POST.get("CGST")
            sgst = request.POST.get("SGST")
            igst = request.POST.get("IGST")
            # for invoice gst number and type
            org_gst_number = request.POST.get("org_gst_number")
            org_gst_reg_type = request.POST.get("org_gst_reg_type")
            single_gst_code = request.POST.get("single_gst_code")
            shipping_charges = request.POST.get("shipping_charges")
            total_amount = request.POST.get("Total")
            is_tc = request.POST.get('invoice_t&c','off')
            is_notes = request.POST.get('invoice_default_notes','off')

            if(is_tc == 'on'):
                org = Organisations.objects.get(user = request.user)
                if(org.invoice_terms_and_condition is None):
                    org.invoice_terms_and_condition = term_condition
                    org.save()
                elif(org.invoice_terms_and_condition is not None):
                    Organisations.objects.get(user = request.user).update(invoice_terms_and_condition = term_condition)

            if(is_notes == 'on'):
                org = Organisations.objects.get(user = request.user)
                if(org.invoice_note is None):
                    org.invoice_note = message
                    org.save()
                elif(org.invoice_note is not None):
                    Organisations.objects.get(user = request.user).update(invoice_note = message)

            if 'save_send' in request.POST:
                save_type = 1
            elif 'save_close' in request.POST:
                save_type = 2
            elif 'save_draft' in request.POST:
                save_type = 3
            elif 'save_print' in request.POST:
                save_type = 4
            elif 'save_new' in request.POST:
                save_type = 5
            
            contact = Contacts.objects.get(Q(user = request.user) & Q(pk = int(invoice_customer)))
            InvoiceModel.objects.filter(pk = int(kwargs["ins"])).update(user= request.user, invoice_customer = contact, email=email,cc_email=cc_email, purchase_order_number = invoice_purchae_number,
                        invoice_number = invoice_number,invoice_check = check_invocie_number,save_type=save_type,invoice_date = in_date,invoice_type_new = invoice_new,
                        invoice_type_recurring = invoice_recurring, invoice_salesperson = invoice_employee,invoice_state_supply = invoice_state_supply,
                        terms_and_condition = term_condition, Note=message,attachements=attachement,sub_total=subtotal,total_discount=distotal,
                        cgst = cgst,sgst = sgst,igst = igst,total_amount = total_amount,shipping_charges=shipping_charges,
                        invoice_org_gst_num = org_gst_number,invoice_org_gst_type = org_gst_reg_type,invoice_org_gst_state = single_gst_code,)
            
            if(cgst != '' or sgst != ''):
                InvoiceModel.objects.filter(pk = int(kwargs["ins"])).update(is_cs_gst = True)
            else:
                InvoiceModel.objects.filter(pk = int(kwargs["ins"])).update(is_cs_gst = False)
                
            if(invoice_new == 'on'):
                InvoiceModel.objects.filter(pk = int(kwargs["ins"])).update(invoice_new_pay_terms = pay_terms,invoice_new_due_date = new_date)
            else:
                InvoiceModel.objects.filter(pk = int(kwargs["ins"])).update(invoice_new_pay_terms = None,invoice_new_due_date = None)
            if(invoice_recurring == 'on'):
                InvoiceModel.objects.filter(pk = int(kwargs["ins"])).update(invoice_recurring_start_date = recurring_start_date,invoice_recurring_end_date = recurring_end_date,
                                            invoice_recurring_repeat = invoice_repeat,invoice_recurring_frequency = invoice_Frequency,invoice_recurring_advance = invoice_advance)
            else:
                InvoiceModel.objects.filter(pk = int(kwargs["ins"])).update(invoice_recurring_start_date = None,invoice_recurring_end_date = None,
                                            invoice_recurring_repeat = None,invoice_recurring_frequency = None,invoice_recurring_advance = None)


            #******************************************************************************
            #  Added By Lawrence : Execute On Invoice Edit
            #******************************************************************************
            #
            invoice = InvoiceModel.objects.get(pk = int(kwargs["ins"]))

            igst_amount = float(invoice.igst) if invoice.igst !="" else 0
            cgst_amount = float(invoice.cgst) if invoice.cgst !="" else 0
            sgst_amount = float(invoice.sgst) if invoice.sgst !="" else 0
            
            gst_ledger = gst_ledger_model.GST_Ledger.objects.get(invoice=invoice)

            gst_ledger.gst_number = invoice.invoice_org_gst_num
            gst_ledger.cgst_amount = cgst_amount
            gst_ledger.sgst_amount = sgst_amount
            gst_ledger.igst_amount = igst_amount
            gst_ledger.is_invoice = True
            gst_ledger.total_tax = gst_ledger.cgst_amount + gst_ledger.sgst_amount + gst_ledger.igst_amount

            gst_ledger.user = invoice.user

            gst_ledger.save()

            #******************************************************************************
            # Code End
            #******************************************************************************
            #

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

            Invoice_Line_Items.objects.filter(Q(user= request.user) & Q(invoice_item_list = invoice)).delete()

            count = len(product_name)
            header_count = 1
            row_count = 1
            header = 0
        for i in range(0,count):

            if(product_quantity[i] != 'header'):
                if(header == 0):
                    products = ProductsModel.objects.get(pk = int(product_name[i]))
                    account = accounts_model.AccGroups.objects.get(pk = int(account_ids[i]))
                    invoice_item = Invoice_Line_Items(
                        user= request.user,
                        invoice_item_list = invoice,
                        is_header = False,
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
                        header_number_count = row_count,
                        # tax_amount = (float(product_tax[i])/100)*float(product_amount[i]), 
                        # igst_amount = float(igst[i]) if len(igst) > 0 else 0,
                        # cgst_amount = float(cgst[i]) if len(cgst) > 0 else 0,
                        # sgst_amount = float(sgst[i]) if len(sgst) > 0 else 0,
                        )
                else:
                    products = ProductsModel.objects.get(pk = int(product_name[i]))
                    account = accounts_model.AccGroups.objects.get(pk = int(account_ids[i-header]))
                    invoice_item = Invoice_Line_Items(
                        user= request.user,
                        invoice_item_list = invoice,
                        is_header = False,
                        product = products,
                        description=product_desc[i-header],
                        account=account,
                        price=product_price[i-header],
                        unit=product_unit[i-header],
                        quantity=product_quantity[i],
                        discount_type = product_discount_type[i-header],
                        discount=product_discount[i-header],
                        tax=product_tax[i-header],
                        cgst_amount = product_cgst[i-header],
                        sgst_amount = product_sgst[i-header],
                        igst_amount = product_igst[i-header],
                        amount=product_amount[i],
                        amount_inc = product_amount_inc[i-header],
                        header_number_count = row_count,
                        # tax_amount = (float(product_tax[i-header])/100)*float(product_amount[i]), 
                        # igst_amount = float(igst[i]) if len(igst) > 0 else 0,
                        # cgst_amount = float(cgst[i]) if len(cgst) > 0 else 0,
                        # sgst_amount = float(sgst[i]) if len(sgst) > 0 else 0,
                        )
                row_count += 1
            elif(product_quantity[i] == 'header'):
                invoice_item = Invoice_Line_Items(user= request.user,invoice_item_list = invoice,is_header = True,header_name = product_name[i],header_subtotal=product_amount[i],
                                                    header_number_count = header_count)
                header_count += 1
                header += 1

            invoice_item.save()  

            
            if(save_type == 4):  

                ins = '/invoice/print/'+str(kwargs["ins"])+'/'
                return redirect(ins, permanent = False)

            if(save_type == 1):  
                invoice_mailer(request, invoice, contact)

            if(save_type == 5):
                ins = '/invoice/add/0/'
                return redirect(ins, permanent = False)
            
        return redirect('/invoice/', permanent = False)

#=====================================================================================
#   CLONE PURCHASE_ORDER
#=====================================================================================
#
class CloneInvoice(View):

    # Initialize 
    data = defaultdict()

    # Template 
    template_name = 'app/app_files/invoice/clone_invoice.html'
    
    # Custom CSS/JS Files For Inclusion into template
    data["css_files"] = []
    data["js_files"] = ['custom_files/js/invoice.js','custom_files/js/product.js','custom_files/js/contacts.js',]

    # Set link as active in menubar
    data["active_link"] = 'Invoice'
    data["breadcrumb_title"] = 'INVOICE'
    data['type'] = 'clone'

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
            invoice = InvoiceModel.objects.get(pk = int(kwargs["ins"]))
            contacts = Contacts.objects.filter(Q(user = request.user) & Q(is_active = True) & Q(contact_delete_status = 0))
            products = ProductsModel.objects.filter(Q(user = request.user) & Q(is_active = True) & Q(product_delete_status = 0))
            
            # inactive and delete product or contact
            intcontacts = Contacts.objects.filter(Q(user = request.user))
            intproducts = ProductsModel.objects.filter(Q(user = request.user))

            invoice_item = Invoice_Line_Items.objects.filter(Q(user= request.user) & Q(invoice_item_list = invoice))
            major_heads = accounts_model.MajorHeads.objects.get(major_head_name = 'Income')
            acc_ledger_income = accounts_model.AccGroups.objects.filter(Q(user = request.user) & Q(major_head = major_heads))
            default_term_condition = Organisations.objects.filter(user = request.user)
            # default = Organisations.objects.filter(user = request.user)
            gst = users_model.OrganisationGSTSettings.objects.filter(user = request.user)
        except:
            return redirect('/unauthorized/', permanent=False)

        # invoice item without header
        invoice_row = invoice_item.filter(is_header = False)

        # invoice item with header
        invoice_row_header = invoice_item.filter(is_header = True)

        if(len(default_term_condition) > 0):
                msg = default_term_condition[0].invoice_terms_and_condition
                invoice_notes = default_term_condition[0].invoice_note
                self.data['term_msg'] = msg
                self.data['invoice_notes'] = invoice_notes

        # check we make a copy or note 
            
        strg1 = str(invoice.invoice_customer)
        strg2 = strg1.split(' -')
        contact_result = contacts.filter(contact_name__iexact = strg2[0]).exists()
        if(contact_result != True):
            self.data['invoice_contact_status2'] = 'NO'
        elif(contact_result == True):
            self.data['invoice_contact_status2'] = 'YES'

        if(invoice.invoice_salesperson != ''):
            check = Contacts.objects.get(pk = int(invoice.invoice_salesperson))
            if(check.contact_delete_status == 1 or check.is_active == False):
                self.data['check'] = 'on'
            else:
                self.data['check'] = 'yes'
        else:
            self.data['check'] = 'off'

        a = []
        for i in range(0,len(invoice_item)):
            if(invoice_item[i].is_header == False):
                strg3 = str(invoice_item[i].product)
                strg4 = strg3.split(' -')
                result = products.filter(product_name__iexact = strg4[0]).exists()
                if(result == True):
                    a.append(invoice_item[i])

        if(len(invoice_item) != len(a)):
            self.data['invoice_product_status2'] = 'NO'
        else:
            self.data['invoice_product_status2'] = 'YES'
        
        self.data["contacts"] = contacts
        self.data['gst'] = gst
        # inactive and delete product or contact
        self.data["intproducts"] = intproducts
        self.data["intcontacts"] = intcontacts
        self.data["products"] = products
        self.data["invoice"] = invoice

        self.data["invoice_item"] = invoice_item
        self.data['acc_ledger_income'] = acc_ledger_income
        # if(len(a) == 0):
        #     self.data["item_count"] = 0
        # else:
        self.data["item_count"] = len(invoice_row)-1
        self.data['item_header_count'] = len(invoice_row_header)

        self.data['payment_terms'] = payment_constants.PAYMENT_DAYS
        self.data['invoice_frequency'] = payment_constants.INVOICE_FREQUENCY
        self.data["state"] = country_list.STATE_LIST_CHOICES


        # Product form
        self.data["add_product_images_form"] = ProductPhotosForm()
        self.data["add_product_form"] = ProductForm(request.user)


        # org gst number
        self.data['is_gst'] = 'no'
        self.data['is_signle_gst'] = 'no'
        self.data['org_gst_type'] = None
        org = Organisations.objects.get(user = request.user)

        org_gst_num = User_Tax_Details.objects.filter(organisation = org.id,is_active = True)

        self.data['org_id'] = org.id
        if(len(org_gst_num) == 1):
            self.data['is_signle_gst'] = 'yes'
            self.data['is_gst'] = org_gst_num[0].gstin
            self.data['org_gst_type'] = org_gst_num[0].gst_reg_type
        elif(len(org_gst_num) > 0):
            default = org_gst_num.filter(default_gstin = True,is_active = True)
            if(len(default) != 0):
                self.data['is_gst'] = default[0].gstin
                self.data['org_gst_type'] = default[0].gst_reg_type
            else:
                self.data['is_gst'] = org_gst_num[0].gstin
                self.data['org_gst_type'] = org_gst_num[0].gst_reg_type


        return render(request, self.template_name, self.data)

#   
#****************************************************************************************
# Code By : roshan maurya
# Common mailer function for sending invoice mail_send
# pass request, invoice and contact instances as arguments
#****************************************************************************************

def invoice_mailer(request, invoice = None, contact = None):

    if invoice is not None and contact is not None: 

        if invoice.email !="":
            InvoiceModel.objects.filter(pk = int(invoice.id)).update(invoice_status = 3)
            organisation = None

            try:
                organisation = Organisations.objects.get(user = request.user)
                subject = "invoice - {} from {} to {}".format(invoice.invoice_number, organisation.organisation_name, contact.contact_name)
            except:
                subject = "invoice - {} to {}".format(invoice.invoice_number,contact.contact_name)
        
            msg_body = ["Dear {},".format(contact.contact_name)]
            msg_body.append("Please find attached the invoice {} for your reference.".format(invoice.invoice_number))
            msg_body.append("<div style='padding:10px; border:1px solid #000000'>")
            msg_body.append("Invoice - {}".format(invoice.invoice_number))

            if invoice.invoice_new_due_date:
                msg_body.append("Due Date - {}".format(invoice.invoice_new_due_date))
            msg_body.append("Amount - {}".format(invoice.total_amount)) 
            msg_body.append("Invoice To - {}".format(contact.contact_name)) 
            if invoice.terms_and_condition:
                msg_body.append("Terms - {}".format(invoice.terms_and_condition)) 
            msg_body.append("</div>")
            msg_body.append("Please feel free to contact us if you have any questions.")
            msg_body.append("Regards,")
            if organisation.organisation_name:
                msg_body.append("Company Name{}".format(organisation.organisation_name))

            if organisation is not None:
                msg_body.append(organisation.organisation_name)

            msg_body = '<br>'.join(msg_body)

            msg_html = "<html><body>"+msg_body+"</body></html>"

            to_list = [email_id for email_id in invoice.email.split(",")]
            cc_list = [cc_email_id for cc_email_id in invoice.cc_email.split(",")]
        
            # attachements = []
            # if str(creditnote.attachements) !="" and send_attachments:
            #     attachements = [os.path.join(settings.MEDIA_ROOT,str(creditnote.attachements))]   
        
            msg = email_helper.Email_Helper(to=to_list, cc=cc_list, subject=subject, message=msg_html)
            msg.mail_send()
            
            #
            
            return True
        return False
    return False
    
#
#
#

def send_invoice(request, ins=None):
    if request.is_ajax():
            
        try:
            invoice = InvoiceModel.objects.get(pk = int(ins))
        except:
            return HttpResponse(0)
            
        try:
            contact = Contacts.objects.get(pk = invoice.invoice_customer_id, user = request.user)
        except:
            return HttpResponse(0)   
            
            
         
        if invoice_mailer(request, invoice, contact):
            return HttpResponse(1) 
        return HttpResponse(0) 
    return HttpResponse(0) 


#=====================================================================================
#   PRINT PURCHASE ORDER
#=====================================================================================
#
def print_invoice(request, ins):

    template_name = 'app/app_files/invoice/print_invoice.html'
    # Initialize 
    data = defaultdict()
    try:
        invoice = InvoiceModel.objects.get(pk = int(ins))
        organisation = Organisations.objects.get(user = request.user)
        organisation_contact = Organisation_Contact.objects.filter(organisation = organisation)
        
        invoice_item = Invoice_Line_Items.objects.filter(Q(user= request.user) & Q(invoice_item_list = invoice))
        contact = Contacts.objects.get(pk = int(invoice.invoice_customer_id))
        address = users_model.User_Address_Details.objects.filter(Q(organisation = organisation) & Q(is_organisation = True) & Q(is_user = True) & Q(default_address = True))
        org_bank_details = users_model.User_Account_Details.objects.filter(Q(organisation = organisation) & Q(is_organisation = True) & Q(is_user = True) & Q(default_bank = True)) 

        customer_gst = User_Tax_Details.objects.get(contact = invoice.invoice_customer_id)
        customer_address = users_model.User_Address_Details.objects.filter(Q(contact = invoice.invoice_customer_id) & Q(default_address = True))

            
    except:
        return redirect('/unauthorized/', permanent=False)

    

    data["contact_name"] = invoice.invoice_customer
        
    data["invoice"] = invoice
    
    data["invoice_item"] = invoice_item
    data['organisation'] = organisation

    # for org bank details 
    if(len(org_bank_details) == 1):
        data['org_bank'] = org_bank_details[0]
    elif(len(org_bank_details) == 0):
        org_bank = users_model.User_Account_Details.objects.filter(Q(organisation = organisation))
        if(len(org_bank) != 0):
            data['org_bank'] = org_bank[0]

    # for org address
    if(len(address) == 1):
        data['org_address'] = address[0]
        data['state'] = address[0].get_state_display()
        data['country'] = address[0].get_country_display()
    elif(len(address) == 0):
        org_address = users_model.User_Address_Details.objects.filter(Q(organisation = organisation))
        if(len(org_address) != 0):
            data['org_address'] = org_address[0]
            data['state'] = org_address[0].get_state_display()
            data['country'] = org_address[0].get_country_display()

    data['organisation_contact'] = organisation_contact
    data['contact'] = contact
    

    data['gst'] = customer_gst.gstin
    if(len(customer_address) == 1):
        data['customer_address'] = customer_address[0]
    elif(len(customer_address) == 0):
        address_first = users_model.User_Address_Details.objects.filter(Q(contact = invoice.invoice_customer_id))
        if(len(address_first) != 0):
            data['customer_address'] = address_first[0]
    
    return render(request,template_name,data)


#=====================================================================================
#   DELETE INVOICE
#=====================================================================================
#

def delete_invoice(request, ins):
    if ins is not None:
        try:
            invoice = InvoiceModel.objects.get(pk = int(ins))
        
        except:
            return redirect('/unauthorized/', permanent=False)

        Invoice_Line_Items.objects.filter(Q(user= request.user) & Q(invoice_item_list = invoice)).delete()
        InvoiceModel.objects.get(pk = int(ins)).delete()

        return redirect('/invoice/', permanent=False)
    return redirect('/unauthorized/', permanent=False)

#=====================================================================================
#   SEARCH ENIGN
#=====================================================================================
#

def search_engin_product(request):

    data = defaultdict()

    if request.method == 'POST':
        search_text = request.POST['search_text']
        if(search_text == ''):
            data['products'] = []
        else:
            product = ProductsModel.objects.filter(Q(product_name__contains = search_text) & Q(is_active = True) & Q(product_delete_status = 0))
            data['products'] = product
        data['search'] = search_text
        return render(request,'app/app_files/invoice/ajax_search.html', data)

#=====================================================================================
#   CHECK CUSTOMER INVOICE TERMS
#=====================================================================================
#
def check_invoice_terms(request, ins):
    data = defaultdict()
    customer = Contacts.objects.get(pk = int(ins))
    invoice = User_Tax_Details.objects.get(Q(is_user = False) & Q(contact = customer))
    if(invoice.invoice_terms is not None):
        data['invoice_terms'] = invoice.get_invoice_terms_display()
    else:
        data['invoice_terms'] = '0'

    return JsonResponse(data)

#=====================================================================================
#   INVOICE STATUS CHANGE
#=====================================================================================
#

def paid_invoice(request, ins):
    try:
        InvoiceModel.objects.filter(pk = int(ins)).update(invoice_status = 2)
    except:
        return HttpResponse(0) 
    return HttpResponse(1) 

#=====================================================================================
#   vendor state address
#=====================================================================================
#
def customer_gst(request, ins):
    # Initialize 
    data = defaultdict()
    contact = Contacts.objects.get(pk = int(ins))
    gst = User_Tax_Details.objects.get(contact = contact)
    data['contact_bill'] = ''
    print(gst.bills_terms)
    if(gst.bills_terms is not None):
        data['contact_bill'] =  gst.bills_terms
    data['gst_type'] = gst.gst_reg_type
    return JsonResponse(data)

#=====================================================================================
#   DELETE INVOICE
#=====================================================================================
#

def delete_invoice(request, ins):
    if ins is not None:
        try:
            InvoiceModel.objects.filter(pk = int(ins)).update(invoice_delete_status = 1)
        
        except:
            return redirect('/unauthorized/', permanent=False)

        # Purchase_Items.objects.filter(Q(user= request.user) & Q(purchase_item_list = purchase_order)).delete()
        # PurchaseOrder.objects.get(pk = int(ins)).delete()

        return redirect('/invoice/', permanent=False)
    return redirect('/unauthorized/', permanent=False)