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
# from app.models.creditnote_model import *

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
        
        # purchase_order = purchase_model.PurchaseOrder.objects.filter(user = request.user)
        # purchase_paginator = Paginator(purchase_order, 10)
        # purchase_page = request.GET.get('page')     
        # try:
        #     purchase_posts = purchase_paginator.page(purchase_page)
        # except PageNotAnInteger:
        #     purchase_posts = purchase_paginator.page(1)
        # except EmptyPage:
        #     purchase_posts = purchase_paginator.page(purchase_paginator.num_pages)
        # self.data["purchase_order"] = purchase_posts
        # self.data["purchase_page"] = purchase_page
        # self.data['purchase_order'] = purchase_order

        # CUSTOMIZE VIEW CODE
        # customize_purchase = CustomizeModuleName.objects.filter(Q(user = request.user) & Q(customize_name = 4))
        # if(len(customize_purchase) != 0):
        #     view_purchase = CustomizePurchaseView.objects.get(customize_view_name = customize_purchase[0].id)
        #     if(view_purchase is not None):
        #         self.data['customize'] = view_purchase
        #     else:
        #         self.data['customize'] = 'NA'
        # else:
        #         self.data['customize'] = 'NA'
                
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