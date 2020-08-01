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
#   PURCHASE_ORDER VIEW
#=====================================================================================
#

class PurchaseOrderView(View):

    # Template 
    template_name = 'app/app_files/purchase_order/base.html'
    
    # Initialize 
    data = defaultdict()
    data["view"] = ""
    data["contacts"] = {}
    data["active_link"] = 'Purchase Order'
    data["breadcrumb_title"] = 'PURCHASE ORDER'
    data['type'] = 'view'

    # Custom CSS/JS Files For Inclusion into template
    data["css_files"] = []
    data["js_files"] = ['custom_files/js/customize_view.js']

    data["included_template"] = 'app/app_files/purchase_order/view_purchase_order.html'
    
    #
    #
    def get(self, request):       
        purchase_order = purchase_model.PurchaseOrder.objects.filter(user = request.user)
        # purchase_paginator = Paginator(purchase_order, 1)
        # purchase_page = request.GET.get('page')     
        # try:
        #     purchase_posts = purchase_paginator.page(purchase_page)
        # except PageNotAnInteger:
        #     purchase_posts = purchase_paginator.page(1)
        # except EmptyPage:
        #     purchase_posts = purchase_paginator.page(purchase_paginator.num_pages)
        # self.data["purchase_order"] = purchase_posts
        # self.data["purchase_page"] = purchase_page
        self.data['purchase_order'] = purchase_order

        # CUSTOMIZE VIEW CODE
        customize_purchase = CustomizeModuleName.objects.filter(Q(user = request.user) & Q(customize_name = 4))
        if(len(customize_purchase) != 0):
            view_purchase = CustomizePurchaseView.objects.get(customize_view_name = customize_purchase[0].id)
            if(view_purchase is not None):
                self.data['customize'] = view_purchase
            else:
                self.data['customize'] = 'NA'
        else:
                self.data['customize'] = 'NA'
                
        return render(request, self.template_name, self.data)

#=====================================================================================
#   ADD purchase_order
#=====================================================================================
#
def add_purchase_order(request, slug):

    # Initialize 
    data = defaultdict()

    # Template 
    template_name = 'app/app_files/purchase_order/add_purchase_order.html'
    
    # Custom CSS/JS Files For Inclusion into template
    data["css_files"] = []
    data["js_files"] = ['custom_files/js/purchase_order.js','custom_files/js/product.js','custom_files/js/contacts.js', 'custom_files/js/common.js','custom_files/js/profile.js', ]

    # Set link as active in menubar
    data["active_link"] = 'Purchase Order'
    data["breadcrumb_title"] = 'PURCHASE ORDER'
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

     # list contact name
    contacts = Contacts.objects.filter(Q(user = request.user) & Q(is_active = True) & Q(contact_delete_status = 0))
    gst = users_model.OrganisationGSTSettings.objects.filter(user = request.user)
    
    default_term_condition = Organisations.objects.filter(user = request.user)
    if(len(default_term_condition) > 0):
        msg = default_term_condition[0].purchase_terms_and_condition
        purchase_notes = default_term_condition[0].purchase_note
        data['term_msg'] = msg
        data['pur_notes'] = purchase_notes

    data["contacts"] = contacts
    data['gst'] = gst 
    data['country_code'] = user_constants.PHONE_COUNTRY_CODE

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
        major_heads = accounts_model.MajorHeads.objects.get(major_head_name = 'Expense')
        acc_ledger_income = accounts_model.AccGroups.objects.filter(Q(user = request.user) & Q(major_head = major_heads))
        data['acc_ledger_income'] = acc_ledger_income
        return render(request, template_name, data)

#=====================================================================================
#   FETCH PRODUCT_type/Units/Price/Product Description/Currency
#=====================================================================================
#
def fetch_purchase_product(request, slug):
    
    # Initialize 
    data = defaultdict()
    products = ProductsModel.objects.get(pk = int(slug))
    data['is_check_purchase'] = 'no'
    data['is_check_selling'] = 'no'
    data['product'] = products.product_type
    data['unit'] = products.get_unit_display()
    data['price'] =  products.purchase_price
    data['selling'] = products.selling_price
    data['desc'] = products.product_description
    data['selling_tax'] = products.selling_tax
    data['purchase_tax'] = products.purchase_tax
    if(products.inclusive_tax is not None):
        data['is_check_selling'] = 'yes'
    if(products.inclusive_purchase_tax is not None):
        data['is_check_purchase'] = 'yes'
    return JsonResponse(data)

#=====================================================================================
#   FETCH ORGANIZATION AND CONTACT ADDRESS
#=====================================================================================
#

def org_contact_address(request, slug):

    # Initialize 
    data = defaultdict()

    data['address'] = []
    data['contact_person'] = []
    data['state'] = []
    data['branch'] = []
    data['gst'] = []

    if(slug == 'org'):
        organization = users_model.Organisations.objects.get(user = request.user)
        address = users_model.User_Address_Details.objects.filter(Q(is_user = True) & Q(organisation = organization) & Q(is_organisation = True) & Q(is_shipping_address = True)).values('address_tag','contact_person','flat_no', 'street', 'city', 'state', 'country', 'pincode','organisation_tax')
        data['ids'] = organization.id

        for i in range(0,len(address)):
            add=""
            count = 1
            for key, value in address[i].items():
                if( value is not None and count > 2):
                    if(key != 'organisation_tax'):
                        add+=str(value)+', '
                elif(count == 1):
                    data['branch'].append(value)
                    count +=1
                elif(count == 2):
                    data['contact_person'].append(value)
                    count +=1

                if(key == 'organisation_tax' ):

                    if(value is not None):
                        gst = users_model.User_Tax_Details.objects.get(pk = int(value))
                        data['gst'].append(gst.gstin)
                    else:
                        data['gst'].append(value)
                
            data['state'].append(address[i]['state'])
            # data['branch'].append(address[i]['address_tag'])
            data['address'].append(add[0:(len(add))-2])
        # contacts = Contacts.objects.filter(Q(user = request.user) & Q(is_user = True) & Q(contact_org = organization))
    elif(slug != 'org'):
        contacts = Contacts.objects.get(pk = int(slug))
        address = users_model.User_Address_Details.objects.filter(Q(is_user = False) & Q(contact = contacts) & Q(is_organisation = False) & Q(is_shipping_address = True)).values('address_tag','contact_person','flat_no', 'street', 'city', 'state', 'country', 'pincode' ,'organisation_tax')
        data['ids'] = contacts.id
        gst = users_model.User_Tax_Details.objects.get(contact = contacts)
        if(gst.gstin is not None):
            data['gst'].append(gst.gstin)
        else:
            data['gst'].append(None)
        for i in range(0,len(address)):
            add=""
            count = 1
            for j in address[i].values():
                
                if( j is not None and count > 2):
                    add+=str(j)+', '
                elif(count == 1):
                    data['branch'].append(j)
                    count +=1
                elif(count == 2):
                    data['contact_person'].append(j)
                    count +=1
            # print(address[i]['state'])
            data['state'].append(address[i]['state'])
        
            data['address'].append(add[0:(len(add))-2])
    
    return JsonResponse(data)

#=====================================================================================
#   LAST ORGAINZATION AND CONTACT ADDRESS FETCH
#=====================================================================================
#

def last_address_fetch(request):

    # Initialize 
    data = defaultdict()

    address = users_model.User_Address_Details.objects.latest('pk')

    data['contact_person'] = address.contact_person
    data['flat_no'] = address.flat_no
    data['street'] = address.street
    data['city'] = address.city
    data['state'] = address.state
    data['country'] = address.country
    data['pincode'] = address.pincode
    return JsonResponse(data)

#=====================================================================================
#   vendor state address
#=====================================================================================
#
def vendor_state(request, ins):
    # Initialize 
    data = defaultdict()
    contact = Contacts.objects.get(pk = int(ins))
    gst = User_Tax_Details.objects.get(contact = contact)
    address = users_model.User_Address_Details.objects.filter(Q(contact = contact) & Q(default_address = True))
    # if(contact.email is None):
    #     data['mail'] = 'null'
    # else:
    data['mail'] = contact.email
    data['gst_type'] = gst.gst_reg_type
    if(len(address) == 1):
        if(address[0].state is None):
            data['vendor_state'] = 'null'
        else:
            data['vendor_state'] = address[0].state
    elif(len(address) == 0):
        address_first = users_model.User_Address_Details.objects.filter(Q(contact = contact))
        if(len(address_first) == 0 or address_first[0].state == 'None'):
            data['vendor_state'] = 'null'
        else:
            data['vendor_state'] = address_first[0].state
        
    return JsonResponse(data)

#=====================================================================================
#   LAST expense account group fetch
#=====================================================================================
#
def vendor_details(request, ins):
     # Initialize 
    data = defaultdict()

    contact = Contacts.objects.get(pk = int(ins))
    data['name'] = contact.contact_name
    data['oganization_name'] = contact.organization_name
    data['mail'] = contact.email
    data['number'] = contact.phone
    data['address'] =[]
    address = users_model.User_Address_Details.objects.filter(Q(contact = contact) & Q(default_address = True)).values('contact_person','flat_no', 'street', 'city', 'state', 'country', 'pincode' ,)

    if(len(address) == 1):
        for i in range(0,len(address)):
            add=""
            for j in address[i].values():
                if( j is not None):
                    add+=str(j)+', '
            data['address'].append(add[0:(len(add))-2])
    elif(len(address) == 0):
        address_first = users_model.User_Address_Details.objects.filter(Q(contact = contact)).values('contact_person','flat_no', 'street', 'city', 'state', 'country', 'pincode' ,)
        if(len(address_first) != 0):
            for i in range(0,1):
                add=""
                for j in address_first[i].values():
                    if( j is not None):
                        add+=str(j)+', '
                data['address'].append(add[0:(len(add))-2])

    return JsonResponse(data)
#=====================================================================================
#   LAST expense account group fetch
#=====================================================================================
#

def last_acc_group_fetch(request):

    # Initialize 
    data = defaultdict()

    account_group = AccGroups.objects.latest('pk')
    data['group_name'] = account_group.group_name
    data['ids'] = account_group.id
    return JsonResponse(data)

#=====================================================================================
#   CHECK PURCHASE_ORDER UNIQUR AND SET DEFULT
#=====================================================================================
#

def unique_purchase_number(request, ins, number):
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

#=====================================================================================
#   SAVE PURCHASE_ORDER
#=====================================================================================
#

def save_purchase_order(request):

    if request.POST:
        vendor = request.POST.get("purchase_vendor")
        order_number = request.POST.get("purchse_order")
        check_order_number = request.POST.get("auto_purchase_number","off")
        order_date = request.POST.get("purchase_date")
        
        # change order date formate
        or_date = datetime.strptime(str(order_date), '%d-%m-%Y').strftime('%Y-%m-%d')
        
        delivery_date = request.POST.get("purchase_delivary_date")

        # change delivery date format
        deli_date = datetime.strptime(str(delivery_date), '%d-%m-%Y').strftime('%Y-%m-%d')

        reference = request.POST.get("purchase_reference")
        is_org =  request.POST.get("org_radio","off")
        is_cutomer =  request.POST.get("customer_radio" ,"off")
        customer = request.POST.get("choose_customer_address")
        attention = request.POST.get("purchase_attention")
        country_code = request.POST.get("country_code")
        contact_no = request.POST.get("purchase_contact")
        delivery_address = request.POST.get("purchase_address")
        term_condition = request.POST.get("purchase_MessageOnStatement")
        message = request.POST.get("purchase_notes")
        
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
        total_amount = request.POST.get("Total")
        freight_charges = request.POST.get("Freight_Charges")
        advance = request.POST.get("advance")
        total_balance = request.POST.get("total_balance")

        state = request.POST.get("order_state")
        is_tc = request.POST.get('purchase_t&c','off')
        is_notes = request.POST.get('purchase_default_notes','off')

        hidden_advance_date = request.POST.get("hidden_advance_date")
        hidden_advance_method = request.POST.get('hidden_advance_method',)
        hidden_advance_notes = request.POST.get('hidden_advance_notes')

        if(is_tc == 'on'):
            org = Organisations.objects.get(user = request.user)
            if(org.purchase_terms_and_condition is None):
                org.purchase_terms_and_condition = term_condition
                org.save()
            elif(org.purchase_terms_and_condition is not None):
                Organisations.objects.get(user = request.user).update(purchase_terms_and_condition = term_condition)

        if(is_notes == 'on'):
            org = Organisations.objects.get(user = request.user)
            if(org.purchase_note is None):
                org.purchase_note = message
                org.save()
            elif(org.purchase_note is not None):
                Organisations.objects.get(user = request.user).update(purchase_note = message)

        if 'save_send' in request.POST:
            save_type = 1
        elif 'save_close' in request.POST:
            save_type = 2
        elif 'save_draft' in request.POST:
            save_type = 3
        elif 'save_print' in request.POST:
            save_type = 4

        contact = Contacts.objects.get(user = request.user, pk = int(vendor))

        purchase_order = PurchaseOrder(user= request.user, vendor = contact, purchase_order_number = order_number, purchase_number_check = check_order_number,
                        save_type=save_type,purchase_order_date = or_date,purchase_delivery_date = deli_date,purchase_refrence = reference, delivery_address = delivery_address,
                        delivery_state = state,is_organisation_delivary = is_org,is_customer_delivary = is_cutomer,customer= customer,attention= attention,country_code = country_code,
                        contact_number=contact_no,terms_and_condition = term_condition, Note=message,sub_total=subtotal,total_discount=distotal,cgst_5 = cgst_5 ,igst_5 = igst_5,
                        sgst_5 = sgst_5,cgst_12 = cgst_12,igst_12 = igst_12,sgst_12 = sgst_12,cgst_18 = cgst_18,igst_18 = igst_18,sgst_18 = sgst_18,
                        cgst_28 = cgst_28,igst_28 = igst_28,sgst_28 = sgst_28,cgst_other=cgst_other,igst_other = igst_other,sgst_other = sgst_other,
                        total_amount = total_amount,freight_charges=freight_charges,advance=advance,total_balance=total_balance,
                        advacne_payment_method = hidden_advance_method,advacne_note= hidden_advance_notes,)
        if(hidden_advance_date != ''):
            purchase_order.advance_payment_date=hidden_advance_date

        if(save_type == 3):  
            purchase_order.purchase_status=1
            
        purchase_order.save()               

        igst = list(filter(None, [igst_5, igst_12, igst_18, igst_28, igst_other]))
        cgst = list(filter(None, [cgst_5, cgst_12, cgst_18, cgst_28,cgst_other]))
        sgst = list(filter(None, [sgst_5, sgst_12, sgst_18, sgst_28, sgst_other]))

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
            purchase_item = Purchase_Items(
                user= request.user,
                purchase_item_list = purchase_order,
                product = products,
                description=product_desc[i],
                account=account,
                price=product_price[i],
                unit=product_unit[i],
                quantity=product_quantity[i],
                discount_type = product_discount_type[i],
                discount=product_discount[i],
                tax=product_tax[i],
                amount=product_amount[i],
                igst_amount = float(igst[i]) if len(igst) > 0 else 0,
                cgst_amount = float(cgst[i]) if len(cgst) > 0 else 0,
                sgst_amount = float(sgst[i]) if len(sgst) > 0 else 0,
            )

            purchase_item.save()  


        # attach_check = request.POST.get("attach_check", False)

        if(save_type == 4):  
            order = PurchaseOrder.objects.latest('pk')
            ins = '/purchase_order/print/'+str(order.id)+'/'
            return redirect(ins, permanent = False)
            

        if(save_type == 1):  
            mail = request.POST.get('mail')    
            # if attach_check:
                # credit_note_mailer(request, creditnote, contact, send_attachments = True)
            # else:
            purchase_order_mailer(request, purchase_order, contact, mail)

        return redirect('/view_purchase_order/', permanent = False)


#=====================================================================================
#   EDIT CREDITNOTE 
#=====================================================================================
#
class EditPurchaseOrder(View):

# Initialize 
    data = defaultdict()

    # Template 
    template_name = 'app/app_files/purchase_order/edit_purchase_order.html'
    
    # Custom CSS/JS Files For Inclusion into template
    data["css_files"] = []
    data["js_files"] = ['custom_files/js/purchase_order.js','custom_files/js/product.js','custom_files/js/contacts.js', 'custom_files/js/common.js','custom_files/js/profile.js',  ]

    # Set link as active in menubar
    data["active_link"] = 'Purchase Order'
    data["breadcrumb_title"] = 'PURCHASE ORDER'
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

    def get(self, request, *args, **kwargs):

        try:
            purchase_order = PurchaseOrder.objects.get(pk = int(kwargs["ins"]))
            contacts = Contacts.objects.filter(Q(user = request.user) & Q(is_active = True) & Q(contact_delete_status = 0))

            # inactive and delete product or contact
            intcontacts = Contacts.objects.filter(Q(user = request.user))
            intproducts = ProductsModel.objects.filter(Q(user = request.user))
            
            products = ProductsModel.objects.filter(Q(user = request.user) & Q(is_active = True) & Q(product_delete_status = 0))
            purchase_item = Purchase_Items.objects.filter(Q(user= request.user) & Q(purchase_item_list = purchase_order))

            major_heads = accounts_model.MajorHeads.objects.get(major_head_name = 'Expense')
            acc_ledger_income = accounts_model.AccGroups.objects.filter(Q(user = request.user) & Q(major_head = major_heads))
            default_term_condition = Organisations.objects.filter(user = request.user)
            gst = users_model.OrganisationGSTSettings.objects.filter(user = request.user)
    
        except:
            return redirect('/unauthorized/', permanent=False)

        if(len(default_term_condition) > 0):
            msg = default_term_condition[0].purchase_terms_and_condition
            purchase_notes = default_term_condition[0].purchase_note
            self.data['term_msg'] = msg
            self.data['pur_notes'] = purchase_notes

        self.data["contacts"] = contacts
        self.data['gst'] = gst

        # inactive and delete product or contact
        self.data["intproducts"] = intproducts
        self.data["intcontacts"] = intcontacts

        self.data["products"] = products
        self.data["purchase_order"] = purchase_order
        self.data["purchase_item"] = purchase_item
        self.data['acc_ledger_income'] = acc_ledger_income
        self.data["item_count"] = len(purchase_item)-1

        # Product form
        self.data["add_product_images_form"] = ProductPhotosForm()
        self.data["add_product_form"] = ProductForm(request.user) 
        # msg = len(defult)
        # if( len(default) > 0):
        #     msg = default[0].terms_and_condition
        #     self.data['term_msg'] = msg

        return render(request, self.template_name, self.data)

    #
    #
    #
    def post(self, request, *args, **kwargs):
        try:
            purchase_order = PurchaseOrder.objects.get(pk = int(kwargs["ins"]))
            purchase_item = Purchase_Items.objects.filter(Q(user= request.user) & Q(purchase_item_list = purchase_order))
            
        except:
            # pass
            return redirect('/unauthorized/', permanent=False)

        if request.method == 'POST':
            vendor = request.POST.get("purchase_vendor")
            order_number = request.POST.get("purchse_order")
            check_order_number = request.POST.get("auto_purchase_number","off")
            order_date = request.POST.get("purchase_date")
            
            # change order date formate
            or_date = datetime.strptime(str(order_date), '%d-%m-%Y').strftime('%Y-%m-%d')
            
            delivery_date = request.POST.get("purchase_delivary_date")

            # change delivery date format
            deli_date = datetime.strptime(str(delivery_date), '%d-%m-%Y').strftime('%Y-%m-%d')

            reference = request.POST.get("purchase_reference")
            is_org =  request.POST.get("org_radio","off")
            is_cutomer =  request.POST.get("customer_radio" ,"off")
            customer = request.POST.get("choose_customer_address")
            attention = request.POST.get("purchase_attention")
            country_code = request.POST.get("country_code")
            contact_no = request.POST.get("purchase_contact")
            delivery_address = request.POST.get("purchase_address")
            term_condition = request.POST.get("purchase_MessageOnStatement")
            message = request.POST.get("purchase_notes")
            
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
            total_amount = request.POST.get("Total")
            freight_charges = request.POST.get("Freight_Charges")
            advance = request.POST.get("advance")
            total_balance = request.POST.get("total_balance")
            state = request.POST.get("order_state")

            is_tc = request.POST.get('purchase_t&c','off')
            is_notes = request.POST.get('purchase_default_notes','off')

            hidden_advance_date = request.POST.get("hidden_advance_date",None)
            # adv_date = datetime.strptime(str(hidden_advance_date), '%d-%m-%Y').strftime('%Y-%m-%d')
            hidden_advance_method = request.POST.get('hidden_advance_method',)
            hidden_advance_notes = request.POST.get('hidden_advance_notes')

            if(is_tc == 'on'):
                org = Organisations.objects.get(user = request.user)
                if(org.purchase_terms_and_condition is None):
                    org.purchase_terms_and_condition = term_condition
                    org.save()
                elif(org.purchase_terms_and_condition is not None):
                    Organisations.objects.get(user = request.user).update(purchase_terms_and_condition = term_condition)

            if(is_notes == 'on'):
                org = Organisations.objects.get(user = request.user)
                if(org.purchase_note is None):
                    org.purchase_note = message
                    org.save()
                elif(org.purchase_note is not None):
                    Organisations.objects.get(user = request.user).update(purchase_note = message)

            if 'save_send' in request.POST:
                save_type = 1
            elif 'save_close' in request.POST:
                save_type = 2
            elif 'save_draft' in request.POST:
                save_type = 3
            elif 'save_print' in request.POST:
                save_type = 4

            
            contact = Contacts.objects.get(Q(user = request.user) & Q(pk = int(vendor)))
            PurchaseOrder.objects.filter(pk = int(kwargs["ins"])).update(user= request.user, vendor = contact, purchase_order_number = order_number, purchase_number_check = check_order_number,
                        save_type=save_type,purchase_order_date = or_date,purchase_delivery_date = deli_date,purchase_refrence = reference, delivery_address = delivery_address,
                        delivery_state = state,is_organisation_delivary = is_org,is_customer_delivary = is_cutomer,customer= customer,attention= attention,country_code = country_code,
                        contact_number=contact_no,terms_and_condition = term_condition, Note=message,sub_total=subtotal,total_discount=distotal,cgst_5 = cgst_5 ,igst_5 = igst_5,
                        sgst_5 = sgst_5,cgst_12 = cgst_12,igst_12 = igst_12,sgst_12 = sgst_12,cgst_18 = cgst_18,igst_18 = igst_18,sgst_18 = sgst_18,
                        cgst_28 = cgst_28,igst_28 = igst_28,sgst_28 = sgst_28,cgst_other=cgst_other,igst_other = igst_other,sgst_other = sgst_other,
                        total_amount = total_amount,freight_charges=freight_charges,advance=advance,total_balance=total_balance,
                        advacne_payment_method=hidden_advance_method,advacne_note=hidden_advance_notes)
            if(hidden_advance_date != ''):
                PurchaseOrder.objects.filter(pk = int(kwargs["ins"])).update(advance_payment_date = hidden_advance_date)

            if(save_type == 3): 
                PurchaseOrder.objects.filter(pk = int(kwargs["ins"])).update(purchase_status=1) 

            product_name = request.POST.getlist('ItemName[]',None)
            product_desc = request.POST.getlist('desc[]',None)
            account_ids = request.POST.getlist('product_account[]',None)
            product_price = request.POST.getlist('Price[]',None)
            product_unit = request.POST.getlist('Unit[]',None)
            product_quantity = request.POST.getlist('Quantity[]',None)
            product_discount = request.POST.getlist('Discount[]',None)
            product_discount_type = request.POST.getlist('Dis[]',None)
            product_tax = request.POST.getlist('tax[]',None)
            product_amount = request.POST.getlist('Amount[]',None)

            Purchase_Items.objects.filter(Q(user= request.user) & Q(purchase_item_list = purchase_order)).delete()

            count = len(product_name)
            for i in range(0,count):

                products = ProductsModel.objects.get(pk = int(product_name[i]))
                account = accounts_model.AccGroups.objects.get(pk = int(account_ids[i]))
                purchase_item = Purchase_Items(user= request.user,purchase_item_list = purchase_order,product = products,description=product_desc[i],
                                account=account,price=product_price[i],unit=product_unit[i],quantity=product_quantity[i],discount_type = product_discount_type[i],
                                discount=product_discount[i],tax=product_tax[i],amount=product_amount[i])
                purchase_item.save()   
            
            if(save_type == 4):  
            # order = PurchaseOrder.objects.latest('pk')
            # print(order.id)
                ins = '/purchase_order/print/'+str(kwargs["ins"])+'/'
                return redirect(ins, permanent = False)

            if(save_type == 1):  
                mail = request.POST.get('mail')   

                # if attach_check:
                    # credit_note_mailer(request, creditnote, contact, send_attachments = True)
                # else:
                purchase_order_mailer(request, purchase_order, contact, mail)
            
        return redirect('/view_purchase_order/', permanent = False)

#=====================================================================================
#   CLONE PURCHASE_ORDER
#=====================================================================================
#
class ClonePurchaseOrder(View):

    # Initialize 
    data = defaultdict()

    # Template 
    template_name = 'app/app_files/purchase_order/clone_purchase_order.html'
    
    # Custom CSS/JS Files For Inclusion into template
    data["css_files"] = []
    data["js_files"] = ['custom_files/js/purchase_order.js','custom_files/js/product.js','custom_files/js/contacts.js', 'custom_files/js/common.js','custom_files/js/profile.js', ]

    # Set link as active in menubar
    data["active_link"] = 'Purchase Order'
    data["breadcrumb_title"] = 'PURCHASE ORDER'
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

    def get(self, request, *args, **kwargs):
            
        try:
            purchase_order = PurchaseOrder.objects.get(pk = int(kwargs["ins"]))
            contacts = Contacts.objects.filter(Q(user = request.user) & Q(is_active = True) & Q(contact_delete_status = 0))
            products = ProductsModel.objects.filter(Q(user = request.user) & Q(is_active = True) & Q(product_delete_status = 0))
            purchase_item = Purchase_Items.objects.filter(Q(user= request.user) & Q(purchase_item_list = purchase_order))

            major_heads = accounts_model.MajorHeads.objects.get(major_head_name = 'Expense')
            acc_ledger_income = accounts_model.AccGroups.objects.filter(Q(user = request.user) & Q(major_head = major_heads))
            default_term_condition = Organisations.objects.filter(user = request.user)
            # default = Organisations.objects.filter(user = request.user)
            gst = users_model.OrganisationGSTSettings.objects.filter(user = request.user)
        except:
            return redirect('/unauthorized/', permanent=False)

        if(len(default_term_condition) > 0):
            msg = default_term_condition[0].purchase_terms_and_condition
            purchase_notes = default_term_condition[0].purchase_note
            self.data['term_msg'] = msg
            self.data['pur_notes'] = purchase_notes

        # check we make a copy or note 
        if(purchase_order.is_customer_delivary == 'on'):
            check = Contacts.objects.get(pk = int(purchase_order.customer))
            if(check.contact_delete_status == 1 or check.is_active == False):
                self.data['check'] = 'on'
            else:
                self.data['check'] = 'yes'
        else:
            self.data['check'] = 'off'
            
        strg1 = str(purchase_order.vendor)
        strg2 = strg1.split(' -')
        contact_result = contacts.filter(contact_name__iexact = strg2[0]).exists()
        if(contact_result != True):
            self.data['purchaseorder_contact_status2'] = 'NO'
        elif(contact_result == True):
            self.data['purchaseorder_contact_status2'] = 'YES'

        a = []
        for i in range(0,len(purchase_item)):
            strg3 = str(purchase_item[i].product)
            strg4 = strg3.split(' -')
            result = products.filter(product_name__iexact = strg4[0]).exists()
            if(result == True):
                a.append(purchase_item[i])

        if(len(purchase_item) != len(a)):
            self.data['purchaseorder_product_status2'] = 'NO'
        else:
            self.data['purchaseorder_product_status2'] = 'YES'
        
        self.data["contacts"] = contacts
        # self.data["state"] = creditnote_constant.state
        self.data['gst'] = gst
        self.data["products"] = products
        self.data["purchase_order"] = purchase_order
        # if(len(a) > 0):
        self.data["purchase_item"] = a
        self.data['acc_ledger_income'] = acc_ledger_income
        self.data["item_count"] = len(purchase_item)-1

        # Product form
        self.data["add_product_images_form"] = ProductPhotosForm()
        self.data["add_product_form"] = ProductForm(request.user)
        # if( len(default) > 0):
        #     msg = default[0].terms_and_condition
        #     self.data['term_msg'] = msg

        return render(request, self.template_name, self.data)

#   
#****************************************************************************************
# Code By : Roshan
# Common mailer function for sending credit note mail_send
# pass request, creditnote and contact instances as arguments
#****************************************************************************************

def purchase_order_mailer(request, purchase_order = None, contact = None, mail = None):

    if purchase_order is not None and contact is not None: 
        PurchaseOrder.objects.filter(pk = int(purchase_order.id)).update(purchase_status = 3)
        if mail is not None:
    
            organisation = None

            try:
                organisation = Organisations.objects.get(user = request.user)
                subject = "Purchase Order - {} from {} to {}".format(purchase_order.purchase_order_number, organisation.organisation_name, contact.organization_name)
            except:
                subject = "Purchase Order - {} to {}".format(purchase_order.purchase_order_number,contact.organization_name)
        
            msg_body = ["Dear {},".format(contact.contact_name)]
            # msg_body.append("Please find attached the Credit Note {} for your reference.".format(creditnote.credit_number))
            msg_body.append("<div style='padding:10px; border:1px solid #000000'>")
            msg_body.append("Purchase Order - {}".format(purchase_order.purchase_order_number))
            msg_body.append("Purchase Order Date - {}".format(purchase_order.purchase_order_date))
            msg_body.append("Amount - {}".format(purchase_order.total_amount)) 
            msg_body.append("</div>")
            msg_body.append("Please feel free to contact us if you have any queries regarding the order.")
            msg_body.append("Regards,")

            if organisation is not None:
                msg_body.append(organisation.organisation_name)

            msg_body = '<br>'.join(msg_body)

            msg_html = "<html><body>"+msg_body+"</body></html>"

            to_list = [mail]
            # [email_id for email_id in creditnote.email.split(",")]
            # cc_list = [cc_email_id for cc_email_id in creditnote.cc_email.split(",")]
        
            # attachements = []
            # if str(creditnote.attachements) !="" and send_attachments:
            #     attachements = [os.path.join(settings.MEDIA_ROOT,str(creditnote.attachements))]   
        
            msg = email_helper.Email_Helper(to=to_list, subject=subject, message=msg_html)
            msg.mail_send()
            
            #
            
            return True
        return False
    return False
    
#
#
#

# def send_purchaseorder(request, ins=None):
#     if request.is_ajax():
            
#         try:
#             creditnote = CreditNode.objects.get(pk = int(ins))
#         except:
#             return HttpResponse(0)
            
#         try:
#             contact = Contacts.objects.get(pk = creditnote.contact_name_id, user = request.user)
#         except:
#             return HttpResponse(0)   
            
            
         
#         if credit_note_mailer(request, creditnote, contact, send_attachments = True):
#             return HttpResponse(1) 
#         return HttpResponse(0) 
#     return HttpResponse(0) 

#=====================================================================================
#   PRINT PURCHASE ORDER
#=====================================================================================
#
def print_purchase_order(request, ins):

    template_name = 'app/app_files/purchase_order/print_purchase_order.html'
    # Initialize 
    data = defaultdict()
    try:
        purchase_order = PurchaseOrder.objects.get(pk = int(ins))
        organisation = Organisations.objects.get(user = request.user)
        organisation_contact = Organisation_Contact.objects.filter(organisation = organisation)
        
        purchase_item = Purchase_Items.objects.filter(Q(user= request.user) & Q(purchase_item_list = purchase_order))
        contact = Contacts.objects.get(pk = int(purchase_order.vendor_id))
        address = users_model.User_Address_Details.objects.filter(Q(organisation = organisation) & Q(is_organisation = True) & Q(is_user = True) & Q(default_address = True))

        vendor_gst = User_Tax_Details.objects.get(contact = purchase_order.vendor_id)
        vendor_address = users_model.User_Address_Details.objects.filter(Q(contact = purchase_order.vendor_id) & Q(default_address = True))

            
    except:
        return redirect('/unauthorized/', permanent=False)

    

    data["contact_name"] = purchase_order.vendor
        
    data["purchase_order"] = purchase_order
    a = str(purchase_order.delivery_address)
    if (a.find('Gst Number:-') != -1): 
        a = a.split('Gst Number:-')
        data['gst_0'] = a[0]
        data['gst_1'] = a[1]
        data['check'] = '1'
    else:
        data['check'] = '2'
    data["purchase_item"] = purchase_item
    data['organisation'] = organisation

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
    

    data['gst'] = vendor_gst.gstin
    if(len(vendor_address) == 1):
        data['vendor_address'] = vendor_address[0]
    elif(len(vendor_address) == 0):
        address_first = users_model.User_Address_Details.objects.filter(Q(contact = purchase_order.vendor_id))
        if(len(address_first) != 0):
            data['vendor_address'] = address_first[0]
    
    return render(request,template_name,data)

#=====================================================================================
#   DELETE PURCHASE ORDER
#=====================================================================================
#

def delete_purchase_order(request, ins):
    if ins is not None:
        try:
            purchase_order = PurchaseOrder.objects.get(pk = int(ins))
        
        except:
            return redirect('/unauthorized/', permanent=False)

        Purchase_Items.objects.filter(Q(user= request.user) & Q(purchase_item_list = purchase_order)).delete()
        PurchaseOrder.objects.get(pk = int(ins)).delete()

        return redirect('/view_purchase_order/', permanent=False)
    return redirect('/unauthorized/', permanent=False)


#=====================================================================================
#   INVOICE STATUS CHANGE
#=====================================================================================
#

def void_purchase(request, ins):
    try:
        PurchaseOrder.objects.filter(pk = int(ins)).update(purchase_status = 2)
    except:
        return HttpResponse(0) 
    return HttpResponse(1) 