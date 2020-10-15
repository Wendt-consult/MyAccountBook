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
from app.models.quotation_model import *
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
from datetime import datetime,date
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
        
        quotation = quotation_model.QuotationModel.objects.filter(user = request.user,quotation_delete_status=0)
        self.data["quotation"] = quotation
        
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
        customize_quotation = CustomizeModuleName.objects.filter(Q(user = request.user) & Q(customize_name = 9))
        if(len(customize_quotation) != 0):
            view_quotation = CustomizeQuotationView.objects.get(customize_view_name = customize_quotation[0].id)
            if(view_quotation is not None):
                self.data['customize'] = view_quotation
            else:
                self.data['customize'] = 'NA'
        else:
                self.data['customize'] = 'NA'
                
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
    
    default_term_condition = Organisations.objects.filter(user = request.user)
    if(len(default_term_condition) > 0):
        msg = default_term_condition[0].quotation_terms_and_condition
        notes = default_term_condition[0].quotation_note
        data['term_msg'] = msg
        data['notes'] = notes

    data["contacts"] = contacts
    data['gst'] = gst 
    # data['country_code'] = user_constants.PHONE_COUNTRY_CODE
    data['payment_terms'] = payment_constants.PAYMENT_DAYS
    # data['invoice_frequency'] = payment_constants.INVOICE_FREQUENCY
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
        # data['direct_con'] = 'NA'
        # if(slug != 'NA'):
        #     contacts = contacts.get(pk = int(slug))
        #     data['direct_con'] = contacts.id

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

#=====================================================================================
#   CHECK QUOTATION UNIQUR AND SET DEFULT
#=====================================================================================
#

def unique_quotation_number(request, ins, number):
    data = defaultdict()
    if(ins == 0):
        quotation = QuotationModel.objects.filter(user = request.user)

        count = len(quotation)

        if(count == 0):
            data['quotation_number'] = 'QT-0001'
        else:
            inc = count+1
            for i in range(0,count):
                a = 'QT-000'+str(inc)
                result = quotation.filter(Q(user = request.user) & Q(quotation_number__iexact = a)).exists() 
                if(result == True):
                    inc += 1
                elif(result == False):
                    data['quotation_number'] = 'QT-000'+str(inc)
                    break
        
        return JsonResponse(data)
    elif (ins == 1):
        quotation = QuotationModel.objects.filter(Q(user = request.user) & Q(quotation_number = number))
        count = len(quotation)
        if(count == 0):
            data['unique'] = 0
        else:
            data['unique'] = 1
        return JsonResponse(data)

#=====================================================================================
#   SAVE QUOTATION
#=====================================================================================
#

def save_quotation(request):

    if request.POST:
        quotation_customer = request.POST.get("quotation_customer")
        email = request.POST.get("Email_Address")
        cc_email = request.POST.get("CC_Email_Address")
        quotation_number = request.POST.get("quotation_number")
        check_quotation_number = request.POST.get("auto_quotation_number","off")
        quotation_date = request.POST.get("Quotation_date")
        # change date formate
        quotation_date = datetime.strptime(str(quotation_date), '%d-%m-%Y').strftime('%Y-%m-%d')

        quotation_exprie_date = request.POST.get("Quotation_exprie_date")
        # change date formate
        quotation_exprie_date = datetime.strptime(str(quotation_exprie_date), '%d-%m-%Y').strftime('%Y-%m-%d')

        quotation_reference = request.POST.get("quotation_reference")
        quotation_employee = request.POST.get("quotation_sales_person")
        quotation_state_supply = request.POST.get("quotation_state_supply")
        quotation_pay_terms = request.POST.get("quotation_pay_terms")
        term_condition = request.POST.get("quotation_MessageOnStatement")
        message = request.POST.get("quotation_notes")
        attachement = request.FILES.get("Attachment")
        subtotal = request.POST.get("SubTotal")
        distotal = request.POST.get("quotation_Discountotal")
        # subtotal = request.POST.get("SubTotal")
        cgst = request.POST.get("CGST")
        sgst = request.POST.get("SGST")
        igst = request.POST.get("IGST")

        # for quotation gst number and type
        org_gst_number = request.POST.get("org_gst_number")
        org_gst_reg_type = request.POST.get("org_gst_reg_type")
        single_gst_code = request.POST.get("single_gst_code")

        shipping_charges = request.POST.get("shipping_charges")
        total_amount = request.POST.get("Total")

        is_tc = request.POST.get('quotation_t&c','off')
        is_notes = request.POST.get('quotation_default_notes','off')

        if(is_tc == 'on'):
            org = Organisations.objects.get(user = request.user)
            if(org.quotation_terms_and_condition is None):
                org.quotation_terms_and_condition = term_condition
                org.save()
            elif(org.quotation_terms_and_condition is not None):
                Organisations.objects.get(user = request.user).update(quotation_terms_and_condition = term_condition)

        if(is_notes == 'on'):
            org = Organisations.objects.get(user = request.user)
            if(org.quotation_note is None):
                org.quotation_note = message
                org.save()
            elif(org.quotation_note is not None):
                Organisations.objects.get(user = request.user).update(quotation_note = message)

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

        contact = Contacts.objects.get(user = request.user, pk = int(quotation_customer))

        quotation = QuotationModel(
            user = request.user, 
            quotation_customer = contact, 
            email = email,
            cc_email = cc_email, 
            quotation_referance = quotation_reference,
            quotation_number = quotation_number,
            quotation_check = check_quotation_number,
            save_type=save_type,
            quotation_date = quotation_date,
            quotation_expire_date = quotation_exprie_date,
            quotation_salesperson = quotation_employee,
            quotation_state_supply = quotation_state_supply,
            quotation_pay_terms = quotation_pay_terms,
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
            quotation_org_gst_num = org_gst_number,
            quotation_org_gst_type = org_gst_reg_type,
            quotation_org_gst_state = single_gst_code,
       )
        if(cgst != '' or sgst != ''):
            quotation.is_cs_gst = True
        else:
            quotation.is_cs_gst = False
        quotation.save()               


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

                    quotation_item = Quotation_Items(
                        user= request.user,
                        quotation_item_list = quotation,
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

                    quotation_item = Quotation_Items(
                        user= request.user,
                        quotation_item_list = quotation,
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
                quotation_item = Quotation_Items(
                    user= request.user,
                    quotation_item_list = quotation,
                    is_header = True,
                    header_name = product_name[i],
                    header_subtotal=product_amount[i],
                    header_number_count = header_count
                )
                header_count += 1
                header += 1

            quotation_item.save()  

        # a = generate_obj_pdf(request,invoice.id)
        # print(a)

        if(save_type == 4):  
            quotation = QuotationModel.objects.latest('pk')
            ins = '/quotation/print/'+str(quotation.id)+'/'
            return redirect(ins, permanent = False)
            

        if(save_type == 1):  
            quotation_mailer(request, quotation, contact)
        
        if(save_type == 5):
            ins = '/quotation/add/0/NA/'
            return redirect(ins, permanent = False)

        return redirect('/quotation/', permanent = False)

#=====================================================================================
#   EDIT INVOICE
#=====================================================================================
#
class EditQuotation(View):

    # Initialize 
    data = defaultdict()

    # Template 
    template_name = 'app/app_files/quotation/edit_quotation.html'
    
    # Custom CSS/JS Files For Inclusion into template
    data["css_files"] = []
    data["js_files"] = ['custom_files/js/quotation.js','custom_files/js/product.js','custom_files/js/contacts.js',]

    # Set link as active in menubar
    data["active_link"] = 'Quotation'
    data["breadcrumb_title"] = 'QUOTATION'
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
            quotation = QuotationModel.objects.get(pk = int(kwargs["ins"]))
            contacts = Contacts.objects.filter(Q(user = request.user) & Q(is_active = True) & Q(contact_delete_status = 0))

            # inactive and delete product or contact
            intcontacts = Contacts.objects.filter(Q(user = request.user))
            intproducts = ProductsModel.objects.filter(Q(user = request.user))
            
            products = ProductsModel.objects.filter(Q(user = request.user) & Q(is_active = True) & Q(product_delete_status = 0))
            quotation_item = Quotation_Items.objects.filter(Q(user= request.user) & Q(quotation_item_list = quotation))

            major_heads = accounts_model.MajorHeads.objects.get(major_head_name = 'Income')
            acc_ledger_income = accounts_model.AccGroups.objects.filter(Q(user = request.user) & Q(major_head = major_heads))
            # for purchase account_ledger details
            major_heads = accounts_model.MajorHeads.objects.get(major_head_name = 'Expense')
            acc_ledger_expense = accounts_model.AccGroups.objects.filter(Q(user = request.user) & Q(major_head = major_heads))
            
            default_term_condition = Organisations.objects.filter(user = request.user)
            gst = users_model.OrganisationGSTSettings.objects.filter(user = request.user)
    
        except:
            return redirect('/unauthorized/', permanent=False)

        # quotation item without header
        quotation_row = quotation_item.filter(is_header = False)

        # quotation item with header
        quotation_row_header = quotation_item.filter(is_header = True)

        if(len(default_term_condition) > 0):
            msg = default_term_condition[0].quotation_terms_and_condition
            quotation_notes = default_term_condition[0].quotation_note
            self.data['term_msg'] = msg
            self.data['quotation_notes'] = quotation_notes

        self.data["contacts"] = contacts
        self.data['gst'] = gst

        # inactive and delete product or contact
        self.data["intproducts"] = intproducts
        self.data["intcontacts"] = intcontacts

        self.data["products"] = products
        self.data["quotation"] = quotation
        self.data["quotation_item"] = quotation_item
        self.data['acc_ledger_income'] = acc_ledger_income
        self.data['acc_ledger_expense'] = acc_ledger_expense
        self.data["item_count"] = len(quotation_row)-1
        self.data['item_header_count'] = len(quotation_row_header)

        self.data['payment_terms'] = payment_constants.PAYMENT_DAYS
        # self.data['invoice_frequency'] = payment_constants.INVOICE_FREQUENCY
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
            quotation = QuotationModel.objects.get(pk = int(kwargs["ins"]))
            quotation_item = Quotation_Items.objects.filter(Q(user= request.user) & Q(quotation_item_list = quotation))
            
        except:
            # pass
            return redirect('/unauthorized/', permanent=False)

        if request.method == 'POST':
            quotation_customer = request.POST.get("quotation_customer")
            email = request.POST.get("Email_Address")
            cc_email = request.POST.get("CC_Email_Address")
            quotation_number = request.POST.get("quotation_number")
            check_quotation_number = request.POST.get("auto_quotation_number","off")
            quotation_date = request.POST.get("Quotation_date")
            # change date formate
            quotation_date = datetime.strptime(str(quotation_date), '%d-%m-%Y').strftime('%Y-%m-%d')

            quotation_exprie_date = request.POST.get("Quotation_exprie_date")
            # change date formate
            quotation_exprie_date = datetime.strptime(str(quotation_exprie_date), '%d-%m-%Y').strftime('%Y-%m-%d')

            quotation_reference = request.POST.get("quotation_reference")
            quotation_employee = request.POST.get("quotation_sales_person")
            quotation_state_supply = request.POST.get("quotation_state_supply")
            quotation_pay_terms = request.POST.get("quotation_pay_terms")
            term_condition = request.POST.get("quotation_MessageOnStatement")
            message = request.POST.get("quotation_notes")
            attachement = request.FILES.get("Attachment")
            subtotal = request.POST.get("SubTotal")
            distotal = request.POST.get("quotation_Discountotal")
            # subtotal = request.POST.get("SubTotal")
            cgst = request.POST.get("CGST")
            sgst = request.POST.get("SGST")
            igst = request.POST.get("IGST")

            # for quotation gst number and type
            org_gst_number = request.POST.get("org_gst_number")
            org_gst_reg_type = request.POST.get("org_gst_reg_type")
            single_gst_code = request.POST.get("single_gst_code")

            shipping_charges = request.POST.get("shipping_charges")
            total_amount = request.POST.get("Total")

            is_tc = request.POST.get('quotation_t&c','off')
            is_notes = request.POST.get('quotation_default_notes','off')

            if(is_tc == 'on'):
                org = Organisations.objects.get(user = request.user)
                if(org.quotation_terms_and_condition is None):
                    org.quotation_terms_and_condition = term_condition
                    org.save()
                elif(org.quotation_terms_and_condition is not None):
                    Organisations.objects.get(user = request.user).update(quotation_terms_and_condition = term_condition)

            if(is_notes == 'on'):
                org = Organisations.objects.get(user = request.user)
                if(org.quotation_note is None):
                    org.quotation_note = message
                    org.save()
                elif(org.quotation_note is not None):
                    Organisations.objects.get(user = request.user).update(quotation_note = message)

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
            
            contact = Contacts.objects.get(Q(user = request.user) & Q(pk = int(quotation_customer)))
            QuotationModel.objects.filter(pk = int(kwargs["ins"])).update(
                user = request.user, 
                quotation_customer = contact, 
                email = email,
                cc_email = cc_email, 
                quotation_referance = quotation_reference,
                quotation_number = quotation_number,
                quotation_check = check_quotation_number,
                save_type=save_type,
                quotation_date = quotation_date,
                quotation_expire_date = quotation_exprie_date,
                quotation_salesperson = quotation_employee,
                quotation_state_supply = quotation_state_supply,
                quotation_pay_terms = quotation_pay_terms,
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
                quotation_org_gst_num = org_gst_number,
                quotation_org_gst_type = org_gst_reg_type,
                quotation_org_gst_state = single_gst_code,
                )
            if(attachement != ''):
                QuotationModel.objects.filter(pk = int(kwargs["ins"])).update(attachements = attachement)

            if(cgst != '' or sgst != ''):
                QuotationModel.objects.filter(pk = int(kwargs["ins"])).update(is_cs_gst = True)
            else:
                QuotationModel.objects.filter(pk = int(kwargs["ins"])).update(is_cs_gst = False)
                

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

            Quotation_Items.objects.filter(Q(user= request.user) & Q(quotation_item_list = quotation)).delete()

            count = len(product_name)
            header_count = 1
            row_count = 1
            header = 0
        for i in range(0,count):

            if(product_quantity[i] != 'header'):
                if(header == 0):
                    products = ProductsModel.objects.get(pk = int(product_name[i]))
                    account = accounts_model.AccGroups.objects.get(pk = int(account_ids[i]))
                    quotation_item = Quotation_Items(
                        user= request.user,
                        quotation_item_list = quotation,
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
                    quotation_item = Quotation_Items(
                        user= request.user,
                        quotation_item_list = quotation,
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
                quotation_item = Quotation_Items(user= request.user,quotation_item_list = quotation,is_header = True,header_name = product_name[i],header_subtotal=product_amount[i],
                                                    header_number_count = header_count)
                header_count += 1
                header += 1

            quotation_item.save()  

            
            if(save_type == 4):  

                ins = '/quotation/print/'+str(kwargs["ins"])+'/'
                return redirect(ins, permanent = False)

            if(save_type == 1):  
                quotation_mailer(request, quotation, contact)

            if(save_type == 5):
                ins = '/quotation/add/0/NA/'
                return redirect(ins, permanent = False)
            
        return redirect('/quotation/', permanent = False)

#   
#****************************************************************************************
# Code By : roshan maurya
# Common mailer function for sending quotation mail_send
# pass request, quotation and contact instances as arguments
#****************************************************************************************

def quotation_mailer(request, quotation = None, contact = None):

    if quotation is not None and contact is not None: 

        if quotation.email !="":
            # InvoiceModel.objects.filter(pk = int(invoice.id)).update(invoice_status = 3)
            organisation = None

            try:
                organisation = Organisations.objects.get(user = request.user)
                subject = "Quotation - {} from {} to {}".format(quotation.quotation_number, organisation.organisation_name, contact.contact_name)
            except:
                subject = "Quotation - {} to {}".format(quotation.quotation_number,contact.contact_name)
        
            msg_body = ["Dear {},".format(contact.contact_name)]
            msg_body.append("Please find attached the quotation {} for your reference.".format(quotation.quotation_number))
            msg_body.append("<div style='padding:10px; border:1px solid #000000'>")
            msg_body.append("Quotation - {}".format(quotation.quotation_number))
            msg_body.append("Quotation Date - {}".format(quotation.quotation_date))
            msg.append("Quotation Expire Date - {}".format(quotation.quotation_expire_date))
            msg_body.append("Amount - {}".format(invoice.total_amount)) 
            msg_body.append("Quotation To - {}".format(contact.contact_name)) 
            if quotation.terms_and_condition:
                msg_body.append("Terms - {}".format(quotation.terms_and_condition)) 
            msg_body.append("</div>")
            msg_body.append("Please feel free to contact us if you have any questions.")
            msg_body.append("Regards,")
            if organisation.organisation_name:
                msg_body.append("Company Name:- {}".format(organisation.organisation_name))

            if organisation is not None:
                msg_body.append(organisation.organisation_name)

            msg_body = '<br>'.join(msg_body)

            msg_html = "<html><body>"+msg_body+"</body></html>"

            if(quotation.email.find(',') != -1):
                to_list = [quotation.email]
            else:
                to_list = [email_id for email_id in quotation.email.split(",")]
            
            if(quotation.cc_email.find(',') != -1):
                cc_list = [quotation.cc_email]
            else:
                cc_list = [cc_email_id for cc_email_id in quotation.cc_email.split(",")]
        
            # attachements = []
            # if str(quotation.attachements) !="":
            #     attachements = [os.path.join(settings.MEDIA_ROOT,str(invoice.attachements))] 
            #     msg = email_helper.Email_Helper(to=to_list, cc=cc_list, subject=subject, message=msg_html,attachment=attachements)  
            # else:
            #     msg = email_helper.Email_Helper(to=to_list, cc=cc_list, subject=subject, message=msg_html)
            msg.mail_send()
            
            #
            
            return True
        return False
    return False
    
#
#
#

def send_quotation(request, ins=None):
    if request.is_ajax():
            
        try:
            quotation = QuotationModel.objects.get(pk = int(ins))
        except:
            return HttpResponse(0)
            
        try:
            contact = Contacts.objects.get(pk = quotation.quotation_customer, user = request.user)
        except:
            return HttpResponse(0)   
            
            
         
        if quotation_mailer(request, quotation, contact):
            return HttpResponse(1) 
        return HttpResponse(0) 
    return HttpResponse(0) 

#=====================================================================================
#   PRINT QUOTATION
#=====================================================================================
#
def print_quotation(request, ins):

    template_name = 'app/app_files/quotation/print_quotation.html'
    # Initialize 
    data = defaultdict()
    try:
        quotation = QuotationModel.objects.get(pk = int(ins))
        organisation = Organisations.objects.get(user = request.user)
        organisation_contact = Organisation_Contact.objects.filter(organisation = organisation)
        
        quotation_item = Quotation_Items.objects.filter(Q(user= request.user) & Q(quotation_item_list = quotation))
        contact = Contacts.objects.get(pk = int(quotation.quotation_customer_id))
        address = users_model.User_Address_Details.objects.filter(Q(organisation = organisation) & Q(is_organisation = True) & Q(is_user = True) & Q(default_address = True))
        # org_bank_details = users_model.User_Account_Details.objects.filter(Q(organisation = organisation) & Q(is_organisation = True) & Q(is_user = True) & Q(default_bank = True)) 

        customer_gst = User_Tax_Details.objects.get(contact = quotation.quotation_customer_id)
        customer_address = users_model.User_Address_Details.objects.filter(Q(contact = quotation.quotation_customer_id) & Q(default_address = True))

            
    except:
        return redirect('/unauthorized/', permanent=False)

    

    data["contact_name"] = quotation.quotation_customer
        
    data["quotation"] = quotation
    
    data["quotation_item"] = quotation_item
    data['organisation'] = organisation

    # for org bank details 
    # if(len(org_bank_details) == 1):
    #     data['org_bank'] = org_bank_details[0]
    # elif(len(org_bank_details) == 0):
    #     org_bank = users_model.User_Account_Details.objects.filter(Q(organisation = organisation))
    #     if(len(org_bank) != 0):
    #         data['org_bank'] = org_bank[0]

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
        address_first = users_model.User_Address_Details.objects.filter(Q(contact = quotation.quotation_customer_id))
        if(len(address_first) != 0):
            data['customer_address'] = address_first[0]
    
    return render(request,template_name,data)

#=====================================================================================
#   DELETE QUOTATION
#=====================================================================================
#

def delete_quotation(request, ins):
    if ins is not None:
        try:
            quotation = QuotationModel.objects.get(pk = int(ins))
        
        except:
            return redirect('/unauthorized/', permanent=False)

        Quotation_Items.objects.filter(Q(user= request.user) & Q(quotation_item_list = quotation)).delete()
        QuotationModel.objects.get(pk = int(ins)).delete()

        return redirect('/quotation/', permanent=False)
    return redirect('/unauthorized/', permanent=False)

#=====================================================================================
#   QUOTATION TO MAKE INVOICE
#=====================================================================================
#

def quotation_to_invoice(request, ins):
    try:
        quotation = QuotationModel.objects.get(pk = int(ins))
        quotation_item = Quotation_Items.objects.filter(Q(user= request.user) & Q(quotation_item_list = quotation))
            
    except:
        return redirect('/unauthorized/', permanent=False)
    # get current date
    current_date = date.today()
    check_date = None
    if(quotation.quotation_pay_terms == 'Due Immediately'):
        check_date = current_date
    elif(quotation.quotation_pay_terms == '10 Days'):
        check_date = current_date + datetime.timedelta(days=10)
    elif(quotation.quotation_pay_terms == '20 Days'):
        check_date = current_date + datetime.timedelta(days=20)
    elif(quotation.quotation_pay_terms == '30 Days'):
        check_date = current_date + datetime.timedelta(days=30)
    elif(quotation.quotation_pay_terms == '60 Days'):
        check_date = current_date + datetime.timedelta(days=60)
    elif(quotation.quotation_pay_terms == '90 Days'):
        check_date = current_date + datetime.timedelta(days=90)
    # generate invoice unique number

    invoice_count = InvoiceModel.objects.filter(user = request.user)

    count = len(invoice_count)
    invoice_number = None
    if(count == 0):
        invoice_number = 'IN-0001'
    else:
        inc = count+1
        for i in range(0,count):
            a = 'IN-000'+str(inc)
            result = invoice_count.filter(Q(user = request.user) & Q(invoice_number__iexact = a)).exists() 
            if(result == True):
                inc += 1
            elif(result == False):
                invoice_number = 'IN-000'+str(inc)
                break

    # create invoice using quotation

    invoice = InvoiceModel(
            user = request.user, 
            invoice_customer = quotation.quotation_customer, 
            email = quotation.email,
            cc_email = quotation.cc_email, 
            purchase_order_number = quotation.quotation_number,
            invoice_number = invoice_number,
            invoice_check = 'on',
            save_type=2,
            invoice_date = current_date,
            invoice_type_new = 'on',
            invoice_new_pay_terms = quotation.quotation_pay_terms,
            invoice_new_due_date = check_date,
            # invoice_type_recurring = invoice_recurring, 
            invoice_salesperson = quotation.quotation_salesperson,
            invoice_state_supply = quotation.quotation_state_supply,
            terms_and_condition = quotation.terms_and_condition, 
            Note = quotation.Note,
            attachements=quotation.attachements,
            sub_total = quotation.sub_total,
            total_discount = quotation.total_discount,
            total_amount = quotation.total_amount,
            shipping_charges = quotation.shipping_charges,     
            cgst = quotation.cgst,
            sgst = quotation.sgst,
            igst = quotation.igst,
            is_cs_gst = quotation.is_cs_gst,
            invoice_org_gst_num = quotation.quotation_org_gst_num,
            invoice_org_gst_type = quotation.quotation_org_gst_type,
            invoice_org_gst_state = quotation.quotation_org_gst_state,
       )
    invoice.save()

    item_count = len(quotation_item)
    for i in range(0,item_count):
        # products = ProductsModel.objects.get(pk = int(product_name[i]))
        # account = accounts_model.AccGroups.objects.get(pk = int(account_ids[i]))

        invoice_item = Invoice_Line_Items(
            user= request.user,
            invoice_item_list = invoice,
            is_header = quotation_item[i].is_header,
            product = quotation_item[i].product,
            description=quotation_item[i].description,
            account=quotation_item[i].account,
            price=quotation_item[i].price,
            unit=quotation_item[i].unit,
            quantity=quotation_item[i].quantity,
            discount_type = quotation_item[i].discount_type,
            discount=quotation_item[i].discount,
            tax=quotation_item[i].tax,
            cgst_amount = quotation_item[i].cgst_amount,
            sgst_amount = quotation_item[i].sgst_amount,
            igst_amount = quotation_item[i].igst_amount,
            amount=quotation_item[i].amount,
            amount_inc = quotation_item[i].amount_inc,
            header_number_count = quotation_item[i].header_number_count,
            header_name = quotation_item[i].header_name,
            header_subtotal=quotation_item[i].header_subtotal,
        )
        invoice_item.save()

        quotation.is_invoice_creted = True
        quotation.save()
    return redirect('/quotation/', permanent = False)