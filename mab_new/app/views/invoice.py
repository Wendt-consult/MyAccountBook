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
from app.other_constants import user_constants
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.db.models import Q
import datetime

import json, os, csv

from app.helpers import email_helper

from datetime import datetime

from django.conf import settings
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

    # Custom CSS/JS Files For Inclusion into template
    data["css_files"] = []
    data["js_files"] = ['custom_files/js/customize_view.js']

    data["included_template"] = 'app/app_files/invoice/view_invoice.html'
    
    #
    #
    def get(self, request):        
        
        invoice = invoice_model.InvoiceModel.objects.filter(user = request.user)
        invoice_paginator = Paginator(invoice, 10)
        invoice_page = request.GET.get('page')     
        try:
            invoice_posts = invoice_paginator.page(invoice_page)
        except PageNotAnInteger:
            invoice_posts = invoice_paginator.page(1)
        except EmptyPage:
            invoice_posts = invoice_paginator.page(invoice_paginator.num_pages)
        self.data["invoice"] = invoice_posts
        self.data["invoice_page"] = invoice_page
    
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
    data["js_files"] = ['custom_files/js/invoice.js','custom_files/js/product.js','custom_files/js/contacts.js', 'custom_files/js/common.js','custom_files/js/profile.js', ]

    # Set link as active in menubar
    data["active_link"] = 'Invoice'
    data["breadcrumb_title"] = 'INVOICE'
    
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
    data['country_code'] = user_constants.PHONE_COUNTRY_CODE
    data['payment_terms'] = payment_constants.PAYMENT_DAYS
    data['invoice_frequency'] = payment_constants.INVOICE_FREQUENCY
    data["state"] = creditnote_constant.state

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
        invoice_cust_mail = request.POST.get("mail")
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
        
        subtotal = request.POST.get("SubTotal")
        distotal = request.POST.get("purchase_Discountotal")
        # subtotal = request.POST.get("SubTotal")
        cgst_5 = request.POST.get("CGST_5")
        sgst_5 = request.POST.get("SGST_5")
        igst_5 = request.POST.get("IGST_5")
        cgst_12 = request.POST.get("CGST_12")
        sgst_12 = request.POST.get("SGST_12")
        igst_12 = request.POST.get("IGST_12")
        cgst_18 = request.POST.get("CGST_18")
        sgst_18 = request.POST.get("SGST_18")
        igst_18 = request.POST.get("IGST_18")
        cgst_28 = request.POST.get("CGST_28")
        sgst_28 = request.POST.get("SGST_28")
        igst_28 = request.POST.get("IGST_28")
        cgst_other = request.POST.get("CGST_other")
        sgst_other = request.POST.get("SGST_other")
        igst_other = request.POST.get("IGST_other")
        shipping_charges = request.POST.get("shipping_charges")
        total_amount = request.POST.get("Total")
        # freight_charges = request.POST.get("Freight_Charges")
        # advance = request.POST.get("advance")
        # total_balance = request.POST.get("total_balance")

        # state = request.POST.get("order_state")
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

        contact = Contacts.objects.get(user = request.user, pk = int(invoice_customer))

        invoice = InvoiceModel(user= request.user, invoice_customer = contact, invoice_customer_mail = invoice_cust_mail, purchase_order_number = invoice_purchae_number,
                        invoice_number = invoice_number,invoice_check = check_invocie_number,save_type=save_type,invoice_date = in_date,invoice_type_new = invoice_new,
                        invoice_type_recurring = invoice_recurring, invoice_salesperson = invoice_employee,invoice_state_supply = invoice_state_supply,
                        terms_and_condition = term_condition, Note=message,sub_total=subtotal,total_discount=distotal,cgst_5 = cgst_5 ,igst_5 = igst_5,
                        sgst_5 = sgst_5,cgst_12 = cgst_12,igst_12 = igst_12,sgst_12 = sgst_12,cgst_18 = cgst_18,igst_18 = igst_18,sgst_18 = sgst_18,
                        cgst_28 = cgst_28,igst_28 = igst_28,sgst_28 = sgst_28,cgst_other=cgst_other,igst_other = igst_other,sgst_other = sgst_other,
                        total_amount = total_amount,shipping_charges=shipping_charges)
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


        product_name = request.POST.getlist('ItemName[]',None)
        product_desc = request.POST.getlist('desc[]',None)
        account_ids = request.POST.getlist('product_account[]',None)
        product_price = request.POST.getlist('Price[]',None)
        product_unit = request.POST.getlist('Unit[]',None)
        product_quantity = request.POST.getlist('Quantity[]',None)
        product_discount = request.POST.getlist('Discount[]',None)
        product_discount_type = request.POST.getlist('Dis[]',None)
        product_tax = request.POST.getlist('tax[]')
        product_amount = request.POST.getlist('Amount[]',None)

        count = len(product_name)
        for i in range(0,count):

            products = ProductsModel.objects.get(pk = int(product_name[i]))
            account = accounts_model.AccGroups.objects.get(pk = int(account_ids[i]))
            invoice_item = Invoice_Line_Items(user= request.user,invoice_item_list = invoice,product = products,description=product_desc[i],
                                account=account,price=product_price[i],unit=product_unit[i],quantity=product_quantity[i],discount_type = product_discount_type[i],
                                discount=product_discount[i],tax=product_tax[i],amount=product_amount[i])

            invoice_item.save()  


        # if(save_type == 4):  
        #     order = PurchaseOrder.objects.latest('pk')
        #     ins = '/purchase_order/print/'+str(order.id)+'/'
        #     return redirect(ins, permanent = False)
            

        # if(save_type == 1):  
        #     mail = request.POST.get('mail')    
        #     purchase_order_mailer(request, purchase_order, contact, mail)

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
