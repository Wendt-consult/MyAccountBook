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

from django.conf import settings

#=====================================================================================
#   INVOICE VIEW
#=====================================================================================
# 

class viewQuotation(View):

    # Template 
    template_name = 'app/app_files/quotation/base.html'
    
    # Initialize 
    data = defaultdict()
    data["view"] = ""
    data["contacts"] = {}
    data["active_link"] = 'Quotation'
    data["breadcrumb_title"] = 'QUOTATION'
    data['type'] = 'view'
    # Custom CSS/JS Files For Inclusion into template
    data["css_files"] = []
    data["js_files"] = ['custom_files/js/customize_view.js']

    data["included_template"] = 'app/app_files/quotation/view_quotation.html'
    
    #
    #
    def get(self, request):        
        
        # invoice = invoice_model.InvoiceModel.objects.filter(user = request.user,invoice_delete_status=0)
        # self.data["invoice"] = invoice
        
        # logic for view journal entry view and query
        # default_list = []
        # invoice = invoice.exclude(save_type = 3)
        # invoice_count = len(invoice)
        # for i in range(0,invoice_count):
        #     invoice_item = Invoice_Line_Items.objects.filter(invoice_item_list = invoice[i],is_header = False)
        #     item_count = len(invoice_item)
        #     # revser_track = 0
        #     check_list = []
        #     for j in range(0,item_count):
        #         if invoice_item[j].account.group_name not in check_list :
        #             check_list.append(invoice_item[j].account.group_name)
        #             acc = invoice_item.filter(account = invoice_item[j].account)
        #             acc_count = len(acc)
        #             default_dic = {}
        #             default_dic['ids'] = invoice[i].id
        #             default_dic['account_name'] = invoice_item[j].account.group_name
        #             calculate = 0.00
        #             for k in range(0,acc_count):
        #                 calculate += float(acc[k].amount)
        #             default_dic['value'] = '%.2f' % calculate
        #             default_list.append(default_dic)
        #             # default_dic.clear()

        # self.data['default_list'] = default_list
                        
        # CUSTOMIZE VIEW CODE
        # customize_invoice = CustomizeModuleName.objects.filter(Q(user = request.user) & Q(customize_name = 5))
        # if(len(customize_invoice) != 0):
        #     view_invoice = CustomizeInvoiceView.objects.get(customize_view_name = customize_invoice[0].id)
        #     if(view_invoice is not None):
        #         self.data['customize'] = view_invoice
        #     else:
        #         self.data['customize'] = 'NA'
        # else:
        #         self.data['customize'] = 'NA'
                
        return render(request, self.template_name, self.data)

#=====================================================================================
#   ADD QUOTATION
#=====================================================================================
#
def add_quotation(request, ins, slug):

    # Initialize 
    data = defaultdict()

    # Template 
    template_name = 'app/app_files/quotation/add_quotation.html'
    
    # Custom CSS/JS Files For Inclusion into template
    data["css_files"] = []
    data["js_files"] = ['custom_files/js/quotation.js','custom_files/js/product.js','custom_files/js/contacts.js',]

    # Set link as active in menubar
    data["active_link"] = 'Quotation'
    data["breadcrumb_title"] = 'QUOTATION'
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
        major_heads = accounts_model.MajorHeads.objects.get(major_head_name = 'Income')
        acc_ledger_income = accounts_model.AccGroups.objects.filter(Q(user = request.user) & Q(major_head = major_heads))
        acc_group_name = []
        acc_ids =[]
        acc_count = len(acc_ledger_income)
        for i in range(0,acc_count):
            acc_group_name.append(acc_ledger_income[i].group_name)
            acc_ids.append(acc_ledger_income[i].id)
        
        # for tax option
        tax = []
        org_gst = len(gst)
        for i in range(0,org_gst):
            tax.append(gst[i].taxname_percent)

        # common dictionary
        data = {'products': name, 'ids': ids , 'acc_group_name':acc_group_name, 'acc_ids':acc_ids, 'gst':tax} 
        return JsonResponse(data)
    elif(int(ins) == 0):
        # for product details
        products = ProductsModel.objects.filter(Q(user = request.user) & Q(is_active = True) & Q(product_delete_status = 0) & Q(product_type__in = [0,1] ))
        data["products"] = products

        # 
        # for account_ledger details
        major_heads = accounts_model.MajorHeads.objects.get(major_head_name = 'Income')
        acc_ledger_income = accounts_model.AccGroups.objects.filter(Q(user = request.user) & Q(major_head = major_heads))
        data['acc_ledger_income'] = acc_ledger_income

        # for purchase account_ledger details
        major_heads = accounts_model.MajorHeads.objects.get(major_head_name = 'Expense')
        acc_ledger_expense = accounts_model.AccGroups.objects.filter(Q(user = request.user) & Q(major_head = major_heads))
        data['acc_ledger_expense'] = acc_ledger_expense

        # for coming to direct contact module
        data['direct_con'] = 'NA'
        if(slug != 'NA'):
            contacts = contacts.get(pk = int(slug))
            data['direct_con'] = contacts.id

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

        return render(request, template_name, data)

