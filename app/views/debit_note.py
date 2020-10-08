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
from app.models.debit_note_model import *
# from app.models.payment_made_model import *
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
#   DEBIT_NOTE VIEW
#=====================================================================================
#

class DebitNoteView(View):

    # Template 
    template_name = 'app/app_files/debit_note/base.html'
    
    # Initialize 
    data = defaultdict()
    data["view"] = ""
    data["contacts"] = {}
    data["active_link"] = 'Debit Note'
    data["breadcrumb_title"] = 'DEBIT NOTE'
    data['type'] = 'view'

    # Custom CSS/JS Files For Inclusion into template
    data["css_files"] = []
    data["js_files"] = ['custom_files/js/customize_view.js']

    data["included_template"] = 'app/app_files/debit_note/view_debit_note.html'

    def get(self, request):

        debit_note = debit_note_model.DebitNote.objects.filter(user = request.user,debit_delete_status = 0)
        self.data['debit_note'] = debit_note

        # CUSTOMIZE VIEW CODE
        customize_debit = CustomizeModuleName.objects.filter(Q(user = request.user) & Q(customize_name = 8))
        if(len(customize_debit) != 0):
            view_debit = CustomizeDebitNoteView.objects.get(customize_view_name = customize_debit[0].id)
            if(view_debit is not None):
                self.data['customize'] = view_debit
            else:
                self.data['customize'] = 'NA'
        else:
                self.data['customize'] = 'NA'
        return render(request, self.template_name, self.data)

#=====================================================================================
#   ADD DEBIT_NOTE
#=====================================================================================
#
def add_debit_note(request, ins, slug):

    # Initialize 
    data = defaultdict()

    # Template 
    template_name = 'app/app_files/debit_note/add_debit_note.html'
    
    # Custom CSS/JS Files For Inclusion into template
    data["css_files"] = []
    data["js_files"] = ['custom_files/js/debit_note.js','custom_files/js/product.js','custom_files/js/contacts.js', 'custom_files/js/common.js','custom_files/js/profile.js', ]

    # Set link as active in menubar
    data["active_link"] = 'Debit Note'
    data["breadcrumb_title"] = 'DEBIT NOTE'
    data['type'] = 'add'
    
    # Product form
    data["add_product_images_form"] = ProductPhotosForm()
    data["add_product_form"] = ProductForm(request.user) 

    # contact Forms
    data["contact_form"] = ContactsForm()
    data["tax_form"] = TaxForm()
    data["other_details_form"] = OtherDetailsForm()
    data["social_form"] = ContactsExtraForm()
    data["new_address_form"] = EditOrgAddressForm()

    # gst form
    data["gst_form"] = OrganisationTaxForm()

    # FORMSETS    
    data["address_formset"] = AddressFormset
    data["accounts_formset"] = AccountsFormset

    # ACCOUNT_LEDGER FORMS
    data["groups_form"] = AccGroupsForm()

    # constant
    data['gst_code'] = country_list.GST_STATE_CODE
    data['gst_r_type'] = user_constants.org_GST_REG_TYPE

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
        acc_ledger_expense = accounts_model.AccGroups.objects.filter(Q(user = request.user) & Q(major_head = major_heads))
        acc_group_name = []
        acc_ids =[]
        acc_count = len(acc_ledger_expense)
        for i in range(0,acc_count):
            acc_group_name.append(acc_ledger_expense[i].group_name)
            acc_ids.append(acc_ledger_expense[i].id)
        # common dictionary
        data = {'products': name, 'ids': ids , 'acc_group_name':acc_group_name, 'acc_ids':acc_ids} 
        return JsonResponse(data)
    elif(int(ins) == 0):
        # for product details
        products = ProductsModel.objects.filter(Q(user = request.user) & Q(is_active = True) & Q(product_delete_status = 0) & Q(product_type__in = [0,1] ))
        data["products"] = products

        # 
        # for income account_ledger details
        major_heads = accounts_model.MajorHeads.objects.get(major_head_name = 'Income')
        acc_ledger_income = accounts_model.AccGroups.objects.filter(Q(user = request.user) & Q(major_head = major_heads))
        data['acc_ledger_income'] = acc_ledger_income

        # for expense account_ledger details
        major_heads = accounts_model.MajorHeads.objects.get(major_head_name = 'Expense')
        acc_ledger_expense = accounts_model.AccGroups.objects.filter(Q(user = request.user) & Q(major_head = major_heads))
        data['acc_ledger_expense'] = acc_ledger_expense

        # link to purchase entry to debit note
        if(slug != 'NA'):
            purchase_entry = PurchaseEntry.objects.get(pk = int(slug))
            entry_item = PurchaseEntryItems.objects.filter(Q(user= request.user) & Q(purchase_entry_list = purchase_entry))
            # purchase_order = PurchaseOrder.objects.get(pk = int(purchase_entry.purchase_order_id))
            intproducts = ProductsModel.objects.filter(Q(user = request.user))
            intcontacts = Contacts.objects.filter(Q(user = request.user))
            # for purchase entry gst check active or inactive
            if(purchase_entry.purchase_org_gst_num != ''):
                org_tax = users_model.User_Tax_Details.objects.get(user = request.user, gstin = purchase_entry.purchase_org_gst_num)
                if(org_tax.is_active == True):
                    data['entry_gst'] = 'active'
                else:
                    data['entry_gst'] = 'inactive'
            else:
                data['entry_gst'] = 'inactive'

            data['purchase_entry'] = purchase_entry
            data['entry_item'] = entry_item
            # data['purchase_order'] = purchase_order
            data['intproducts'] = intproducts
            data['intcontacts'] = intcontacts
            data['item_count'] = len(entry_item)
            data['link_purchase_entry'] = 'yes'
        else:
            data['entry_gst'] = 'inactive'
            data['link_purchase_entry'] = 'no'
            
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
        address = users_model.User_Address_Details.objects.filter(Q(is_user = True) & Q(organisation = organization) & Q(is_organisation = True) & Q(is_active = True)).values('address_tag','contact_person','flat_no', 'street', 'city', 'state', 'country', 'pincode','organisation_tax')
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
        gst = users_model.User_Tax_Details.objects.get(Q(contact = contacts))
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
    data['gstin'] = ''
    contact = Contacts.objects.get(pk = int(ins))
    gst = User_Tax_Details.objects.get(contact = contact)
    address = users_model.User_Address_Details.objects.filter(Q(contact = contact) & Q(default_address = True))
    # if(contact.email is None):
    #     data['mail'] = 'null'
    # else:
    data['mail'] = contact.email
    data['gst_type'] = gst.gst_reg_type
    if(gst.gstin is not None):
        data['gstin'] = gst.gstin
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
    contact_tax = users_model.User_Tax_Details.objects.get(Q(contact = contact))
    data['gstin'] = contact_tax.gstin
    data['gst_type'] = contact_tax.get_gst_reg_type_display()
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
#   CHECK Debit_note UNIQUR AND SET DEFULT
#=====================================================================================
#

def unique_debit_number(request, ins, number):
    data = defaultdict()
    if(ins == 0):
        debit_note = debit_note_model.DebitNote.objects.filter(user = request.user)

        count = len(debit_note)

        if(count == 0):
            data['debit_note'] = 'DN-0001'
        else:
            inc = count+1
            for i in range(0,count):
                a = 'DN-000'+str(inc)
                result = debit_note.filter(Q(user = request.user) & Q(debit_note_number__iexact = a)).exists() 
                if(result == True):
                    inc += 1
                elif(result == False):
                    data['debit_note'] = 'DN-000'+str(inc)
                    break
        
        return JsonResponse(data)
    elif (ins == 1):
        # check credit note number is unquie
        debit_note = debit_note_model.DebitNote.objects.filter(Q(user = request.user) & Q(debit_note_number = number))
        count = len(debit_note)
        if(count == 0):
            data['unique'] = 0
        else:
            data['unique'] = 1
        return JsonResponse(data)

#=====================================================================================
#   SAVE DEBIT_NOTE
#=====================================================================================
#

def save_debit_note(request):

    if request.POST:
        vendor = request.POST.get("debit_vendor")
        debit_number = request.POST.get("debit_number")
        check_debit_number = request.POST.get("auto_debit_number","off")
        debit_date = request.POST.get("debit_date")
        
        # change order date formate
        debit_date = datetime.strptime(str(debit_date), '%d-%m-%Y').strftime('%Y-%m-%d')

        reference = request.POST.get("debit_reference")
        is_org =  request.POST.get("org_radio","off")
        is_cutomer =  request.POST.get("customer_radio" ,"off")
        customer = request.POST.get("choose_customer_address")
        attention = request.POST.get("debit_attention")
        country_code = request.POST.get("debit_contact_code")
        contact_no = request.POST.get("debit_contact")
        delivery_address = request.POST.get("debit_address")
        term_condition = request.POST.get("debit_MessageOnStatement")
        message = request.POST.get("debit_notes")
        
        subtotal = request.POST.get("SubTotal")
        distotal = request.POST.get("debit_Discountotal")
        cgst = request.POST.get("CGST")
        sgst = request.POST.get("SGST")
        igst = request.POST.get("IGST")
        total_amount = request.POST.get("Total")
        # freight_charges = request.POST.get("Freight_Charges")
        # advance = request.POST.get("advance")
        # total_balance = request.POST.get("total_balance")

        # state = request.POST.get("order_state")

         # for purhase gst number and type
        org_gst_number = request.POST.get("org_gst_number")
        org_gst_reg_type = request.POST.get("org_gst_reg_type")
        single_gst_code = request.POST.get("single_gst_code")
        
        is_tc = request.POST.get('debit_t&c','off')
        is_notes = request.POST.get('debit_default_notes','off')
        purchase_entry_id = request.POST.get('purchase_entry_id')
        # hidden_advance_date = request.POST.get("hidden_advance_date")
        # hidden_order_make_payment = request.POST.get('hidden_order_make_payment','off')
        # hidden_advance_method = request.POST.get('hidden_advance_method',)
        # hidden_advance_notes = request.POST.get('hidden_advance_notes')

        if(is_tc == 'on'):
            org = Organisations.objects.get(user = request.user)
            if(org.debit_terms_and_condition is None):
                org.debit_terms_and_condition = term_condition
                org.save()
            elif(org.debit_terms_and_condition is not None):
                Organisations.objects.get(user = request.user).update(debit_terms_and_condition = term_condition)

        if(is_notes == 'on'):
            org = Organisations.objects.get(user = request.user)
            if(org.debit_note is None):
                org.debit_note = message
                org.save()
            elif(org.debit_note is not None):
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
        purchase_entry = PurchaseEntry.objects.get(pk = int(purchase_entry_id))
        debit_note = DebitNote(
            user= request.user, 
            vendor = contact, 
            purchase_entry = purchase_entry,
            debit_note_number = debit_number, 
            debit_note_check = check_debit_number,
            save_type=save_type,
            debit_note_date = debit_date,
            debit_note_refrence = reference, 
            debit_delivery_address = delivery_address,
            is_organisation_delivary = is_org,
            is_customer_delivary = is_cutomer,
            customer= customer,
            attention= attention,
            country_code = country_code,
            contact_number=contact_no,
            terms_and_condition = term_condition, 
            Note=message,
            sub_total=subtotal,
            total_discount=distotal,
            cgst = cgst,
            sgst = sgst,
            igst = igst,
            total = total_amount,
            debit_org_gst_num = org_gst_number,
            debit_org_gst_type = org_gst_reg_type,
            debit_org_gst_state = single_gst_code,
            )
        if(cgst != '' or sgst != ''):
            debit_note.is_cs_gst = True
        elif(igst != ''):
            debit_note.is_cs_gst = False

        # if(hidden_advance_date != ''):
        #     purchase_order.advance_payment_date=hidden_advance_date

        # if(save_type == 3):  
        #     debit_note.debit_status=1
        # if(save_type == 2 or save_type == 4):
        #     debit_note.debit_status = 0
            
        debit_note.save()               

        # igst = list(filter(None, [igst_5, igst_12, igst_18, igst_28, igst_other]))
        # cgst = list(filter(None, [cgst_5, cgst_12, cgst_18, cgst_28,cgst_other]))
        # sgst = list(filter(None, [sgst_5, sgst_12, sgst_18, sgst_28, sgst_other]))

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
            if(product_name[i] !=''):
                products = ProductsModel.objects.get(pk = int(product_name[i]))
                account = accounts_model.AccGroups.objects.get(pk = int(account_ids[i]))
                debit_item = DebitNoteItems(
                    user= request.user,
                    debit_note_list = debit_note,
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
                debit_item.save()  


        # # for create make payment if some advance given
        # if(hidden_order_make_payment == 'on' and advance != ''):
        #     value = createPayment(request, purchase_order)

        # if(save_type == 4):  
        #     order = PurchaseOrder.objects.latest('pk')
        #     ins = '/debit_note/print/'+str(order.id)+'/'
        #     return redirect(ins, permanent = False)
        
        # change satuts of purcase entry when debit note credited then you can not make debit note twish with one purchase entry
        PurchaseEntry.objects.filter(pk = int(purchase_entry_id)).update(debit_note = 1)
        # Saving unused credit in contact type vendor
        
        credit = float(contact.unused_credit) + float(debit_note.total)
        contact.unused_credit = '%.2f' % credit
        contact.save()

        if(save_type == 1):  
            mail = request.POST.get('mail')    
            # if attach_check:
                # credit_note_mailer(request, creditnote, contact, send_attachments = True)
            # else:
            debit_note_mailer(request, debit_note, contact, mail)


        return redirect('/debitnote/', permanent = False)

#=====================================================================================
#   EDIT DEBIT_NOTE
#=====================================================================================
#
class EditDebitNote(View):

# Initialize 
    data = defaultdict()

    # Template 
    template_name = 'app/app_files/debit_note/edit_debit_note.html'
    
    # Custom CSS/JS Files For Inclusion into template
    data["css_files"] = []
    data["js_files"] = ['custom_files/js/debit_note.js','custom_files/js/product.js','custom_files/js/contacts.js', 'custom_files/js/common.js','custom_files/js/profile.js']

    # Set link as active in menubar
    data["active_link"] = 'Debit Note'
    data["breadcrumb_title"] = 'DEBIT NOTE'
    data['type'] = 'edit'

    # contact Forms
    data["contact_form"] = ContactsForm()
    data["tax_form"] = TaxForm()
    data["other_details_form"] = OtherDetailsForm()
    data["social_form"] = ContactsExtraForm()
    data["new_address_form"] = EditOrgAddressForm()

    # FORMSETS    
    data["address_formset"] = AddressFormset
    data["accounts_formset"] = AccountsFormset

    # gst form
    data["gst_form"] = OrganisationTaxForm()

    # ACCOUNT_LEDGER FORMS
    data["groups_form"] = AccGroupsForm()

    # constant
    data['gst_code'] = country_list.GST_STATE_CODE
    data['gst_r_type'] = user_constants.org_GST_REG_TYPE
    data['country_code'] = user_constants.PHONE_COUNTRY_CODE
    # data['ven_gst_type'] = user_constants.GST_REG_TYPE

    def get(self, request, *args, **kwargs):

        try:
            debit_note = debit_note_model.DebitNote.objects.get(pk = int(kwargs["ins"]))
            contacts = Contacts.objects.filter(Q(user = request.user) & Q(is_active = True) & Q(contact_delete_status = 0))
            products = ProductsModel.objects.filter(Q(user = request.user) & Q(is_active = True) & Q(product_delete_status = 0))

            # inactive and delete product or contact
            intcontacts = Contacts.objects.filter(Q(user = request.user))
            intproducts = ProductsModel.objects.filter(Q(user = request.user))

            debit_item = debit_note_model.DebitNoteItems.objects.filter(Q(user= request.user) & Q(debit_note_list = debit_note))
            major_heads = accounts_model.MajorHeads.objects.get(major_head_name = 'Expense')
            acc_ledger_expense = accounts_model.AccGroups.objects.filter(Q(user = request.user) & Q(major_head = major_heads))

            # for income account_ledger details
            major_heads = accounts_model.MajorHeads.objects.get(major_head_name = 'Income')
            acc_ledger_income = accounts_model.AccGroups.objects.filter(Q(user = request.user) & Q(major_head = major_heads))

            default_term_condition = Organisations.objects.filter(user = request.user)
            gst = users_model.OrganisationGSTSettings.objects.filter(user = request.user)
        except:
            return redirect('/unauthorized/', permanent=False)
        
        if(len(default_term_condition) > 0):
            msg = default_term_condition[0].debit_terms_and_condition
            debit_msg = default_term_condition[0].debit_note
            self.data['term_msg'] = msg
            self.data['debit_msg'] = debit_msg

        self.data["contacts"] = contacts
        self.data['gst'] = gst

        # inactive and delete product or contact
        self.data["intproducts"] = intproducts
        self.data["intcontacts"] = intcontacts

        self.data["products"] = products
        self.data["debit_note"] = debit_note
        self.data["debit_item"] = debit_item
        self.data['acc_ledger_expense'] = acc_ledger_expense
        self.data['acc_ledger_income'] = acc_ledger_income
        self.data["item_count"] = len(debit_item)

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
            debit_note = debit_note_model.DebitNote.objects.get(pk = int(kwargs["ins"]))
            # debit_item = debit_note_model.DebitNoteItems.objects.filter(Q(user= request.user) & Q(debit_note_list = debit_note))
            previous_debit_amount = debit_note.total
            previous_contact_id = debit_note.vendor_id
        except:
            # pass
            return redirect('/unauthorized/', permanent=False)

        if request.method == 'POST':
            vendor = request.POST.get("debit_vendor")
            debit_number = request.POST.get("debit_number")
            check_debit_number = request.POST.get("auto_debit_number","off")
            debit_date = request.POST.get("debit_date")
            
            # change order date formate
            debit_date = datetime.strptime(str(debit_date), '%d-%m-%Y').strftime('%Y-%m-%d')

            reference = request.POST.get("debit_reference")
            is_org =  request.POST.get("org_radio","off")
            is_cutomer =  request.POST.get("customer_radio" ,"off")
            customer = request.POST.get("choose_customer_address")
            attention = request.POST.get("debit_attention")
            country_code = request.POST.get("debit_contact_code")
            contact_no = request.POST.get("debit_contact")
            delivery_address = request.POST.get("debit_address")
            term_condition = request.POST.get("debit_MessageOnStatement")
            message = request.POST.get("debit_notes")
            
            subtotal = request.POST.get("SubTotal")
            distotal = request.POST.get("debit_Discountotal")
            cgst = request.POST.get("CGST")
            sgst = request.POST.get("SGST")
            igst = request.POST.get("IGST")
            total_amount = request.POST.get("Total")
            # freight_charges = request.POST.get("Freight_Charges")
            # advance = request.POST.get("advance")
            # total_balance = request.POST.get("total_balance")

            # state = request.POST.get("order_state")

            # for purhase gst number and type
            org_gst_number = request.POST.get("org_gst_number")
            org_gst_reg_type = request.POST.get("org_gst_reg_type")
            single_gst_code = request.POST.get("single_gst_code")
            
            is_tc = request.POST.get('debit_t&c','off')
            is_notes = request.POST.get('debit_default_notes','off')

            # hidden_advance_date = request.POST.get("hidden_advance_date")
            # hidden_order_make_payment = request.POST.get('hidden_order_make_payment','off')
            # hidden_advance_method = request.POST.get('hidden_advance_method',)
            # hidden_advance_notes = request.POST.get('hidden_advance_notes')

            if(is_tc == 'on'):
                org = Organisations.objects.get(user = request.user)
                if(org.debit_terms_and_condition is None):
                    org.debit_terms_and_condition = term_condition
                    org.save()
                elif(org.debit_terms_and_condition is not None):
                    Organisations.objects.get(user = request.user).update(debit_terms_and_condition = term_condition)

            if(is_notes == 'on'):
                org = Organisations.objects.get(user = request.user)
                if(org.debit_note is None):
                    org.debit_note = message
                    org.save()
                elif(org.debit_note is not None):
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
            debit_note_model.DebitNote.objects.filter(pk = int(kwargs["ins"])).update(
                user= request.user, 
                vendor = contact, 
                debit_note_number = debit_number, 
                debit_note_check = check_debit_number,
                save_type=save_type,
                debit_note_date = debit_date,
                debit_note_refrence = reference, 
                debit_delivery_address = delivery_address,
                is_organisation_delivary = is_org,
                is_customer_delivary = is_cutomer,
                customer= customer,
                attention= attention,
                country_code = country_code,
                contact_number=contact_no,
                terms_and_condition = term_condition, 
                Note=message,
                sub_total=subtotal,
                total_discount=distotal,
                cgst = cgst,
                sgst = sgst,
                igst = igst,
                total = total_amount,
                debit_org_gst_num = org_gst_number,
                debit_org_gst_type = org_gst_reg_type,
                debit_org_gst_state = single_gst_code,
                )
            if(cgst != '' or sgst != ''):
                debit_note_model.DebitNote.objects.filter(pk = int(kwargs["ins"])).update(is_cs_gst = True)
            elif(igst != ''):
                debit_note_model.DebitNote.objects.filter(pk = int(kwargs["ins"])).update(is_cs_gst = False)


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

            debit_note_model.DebitNoteItems.objects.filter(Q(user= request.user) & Q(debit_note_list = debit_note)).delete()

            count = len(product_name)
            for i in range(0,count):
                if(product_name[i] !=''):
                    products = ProductsModel.objects.get(pk = int(product_name[i]))
                    account = accounts_model.AccGroups.objects.get(pk = int(account_ids[i]))
                    debit_item = debit_note_model.DebitNoteItems(
                        user= request.user,
                        debit_note_list = debit_note,
                        product = products,
                        description=product_desc[i],
                        account=account,
                        price=product_price[i],
                        unit=product_unit[i],
                        quantity=product_quantity[i],
                        discount_type = product_discount_type[i],
                        discount=product_discount[i],
                        tax= product_tax[i],
                        cgst_amount = product_cgst[i],
                        sgst_amount = product_sgst[i],
                        igst_amount = product_igst[i],
                        amount=product_amount[i],
                        amount_inc = product_amount_inc[i],
                        )
                # if(len(product_tax) == 0):
                #     purchase_item.tax=''
                # else:
                #    purchase_item.tax= product_tax[i]
                debit_item.save()   
            
            # for create make payment if some advance given
            # if(hidden_order_make_payment == 'on' and advance != ''):
            #     order = PurchaseOrder.objects.get(pk = int(kwargs["ins"]))
            #     value = createPayment(request, order)

            # if(save_type == 4):  
            #     ins = '/purchase_order/print/'+str(kwargs["ins"])+'/'
            #     return redirect(ins, permanent = False)

            # for adding unused amount in contact
            debit = debit_note_model.DebitNote.objects.get(pk = int(kwargs["ins"]))
            con = Contacts.objects.get(Q(user = request.user) & Q(pk = int(previous_contact_id)))
            if(previous_contact_id == debit.vendor_id):
                if(float(previous_debit_amount) > float(debit.total) or float(previous_debit_amount) < float(debit.total)):
                    cal = float(con.unused_credit) - float(previous_debit_amount)
                    cal += float(debit.total)
                    con.unused_credit = '%.2f' % cal
                    con.save()
            elif(previous_contact_id != debit.vendor_id):
                cal = float(con.unused_credit ) - float(previous_debit_amount)
                con.unused_credit = '%.2f' % cal
                con.save()
                cal = float(debit.total) + float(contact.unused_credit)
                contact.unused_credit = '%.2f' % cal
                contact.save()

            if(save_type == 1):  
                mail = request.POST.get('mail')   
                debit_note_mailer(request, debit_note, contact, mail)
            
        return redirect('/debitnote/', permanent = False)
#=====================================================================================
#   MAKE PAYMENT
#=====================================================================================
#

def createPayment(request, order = None):
    payment_count = PurchasePayment.objects.filter(user = request.user).count()
    payment_number = None
    if(payment_count > 0 ):
        payment_number = 'PM-000'+str(payment_count + 1)
    else:
        payment_number = 'PM-0001'

    if order is not None:
        payment = PurchasePayment(
            user = request.user,
            vendor = order.vendor,
            payment_number = payment_number,
            payment_date = order.advance_payment_date,
            payment_reference = order.debit_note_number,
            payment_mode = order.advacne_payment_method,
            Note = order.advacne_note,
            Amount = order.advance,
        )

        # if(entry.purchase_order.advance_payment_date != None):
        #     payment.payment_date = entry.purchase_order.advance_payment_date 
        # if(entry.purchase_order.advacne_payment_method != ''):
        #     payment.payment_mode = int(entry.purchase_order.advacne_payment_method)

        payment.save()
    return 'done'  


#   
#****************************************************************************************
# Code By : Roshan
# Common mailer function for sending credit note mail_send
# pass request, creditnote and contact instances as arguments
#****************************************************************************************

def debit_note_mailer(request, debit_note = None, contact = None, mail = None):

    if debit_note is not None and contact is not None: 
        # DebitNote.objects.filter(pk = int(debit_note.id))
        if mail is not None:
    
            organisation = None

            try:
                organisation = Organisations.objects.get(user = request.user)
                subject = "Debit Note - {} from {} to {}".format(debit_note.debit_note_number, organisation.organisation_name, contact.organization_name)
            except:
                subject = "Debit Note - {} to {}".format(debit_note.debit_note_number,contact.organization_name)
        
            msg_body = ["Dear {},".format(contact.contact_name)]
            # msg_body.append("Please find attached the Credit Note {} for your reference.".format(creditnote.credit_number))
            msg_body.append("<div style='padding:10px; border:1px solid #000000'>")
            msg_body.append("Debit Note - {}".format(debit_note.debit_note_number))
            msg_body.append("Debit Note Date - {}".format(debit_note.debit_note_date))
            msg_body.append("Amount - {}".format(debit_note.total)) 
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


#=====================================================================================
#   PRINT Debit_note
#=====================================================================================
#
def print_debit_note(request, ins):

    template_name = 'app/app_files/debit_note/print_debit_note.html'
    # Initialize 
    data = defaultdict()
    try:
        debit_note = DebitNote.objects.get(pk = int(ins))
        organisation = Organisations.objects.get(user = request.user)
        organisation_contact = Organisation_Contact.objects.filter(organisation = organisation)
        
        purchase_item = Purchase_Items.objects.filter(Q(user= request.user) & Q(purchase_item_list = purchase_order))
        contact = Contacts.objects.get(pk = int(debit_note.vendor_id))
        address = users_model.User_Address_Details.objects.filter(Q(organisation = organisation) & Q(is_organisation = True) & Q(is_user = True) & Q(default_address = True))

        vendor_gst = User_Tax_Details.objects.get(contact = debit_note.vendor_id)
        vendor_address = users_model.User_Address_Details.objects.filter(Q(contact = debit_note.vendor_id) & Q(default_address = True))

            
    except:
        return redirect('/unauthorized/', permanent=False)

    

    data["contact_name"] = debit_note.vendor
        
    data["debit_note"] = debit_note
    a = str(debit_note.delivery_address)
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
        address_first = users_model.User_Address_Details.objects.filter(Q(contact = debit_note.vendor_id))
        if(len(address_first) != 0):
            data['vendor_address'] = address_first[0]
    
    return render(request,template_name,data)




def vendor_gst_save(request):
    contact_ids = request.POST.get("vendor_ids")
    contact_gst_type = request.POST.get("vendor_gst_type")
    contact_gst = request.POST.get("vendor_gst")
    try:
        contact = contacts_model.Contacts.objects.get(pk = int(contact_ids))
        User_Tax_Details.objects.filter(contact = contact).update(gst_reg_type = contact_gst_type,gstin = contact_gst)
    except:
        return HttpResponse(0) 
    return HttpResponse(1)

#=====================================================================================
#   DELETE DEBIT_NOTE
#=====================================================================================
#

def delete_debit_note(request, ins):
    if ins is not None:
        try:
            DebitNote.objects.filter(pk = int(ins)).update(debit_delete_status = 1)
        
        except:
            return redirect('/unauthorized/', permanent=False)

        # Purchase_Items.objects.filter(Q(user= request.user) & Q(purchase_item_list = purchase_order)).delete()
        # PurchaseOrder.objects.get(pk = int(ins)).delete()

        return redirect('/debitnote/', permanent=False)
    return redirect('/unauthorized/', permanent=False)

#=====================================================================================
#  get quantity data for edit debit note for product line item validation
#=====================================================================================
#
def edit_debit_quantity(request):

    if request.method == 'POST':
        # Initialize 
        data = defaultdict()
        debit_note = debit_note_model.DebitNote.objects.get(pk = int(request.POST.get('debit_note_id')))
        purchase_entry = PurchaseEntry.objects.get(pk = int(debit_note.purchase_entry_id))
        entry_item = PurchaseEntryItems.objects.filter(purchase_entry_list = purchase_entry).values('quantity')
        entry_dic = {}
        if(len(entry_item) != 0):
            val = 1
            for i in range(0,len(entry_item)):
                a = entry_item[i]
                entry_dic['Quantity'+ str(val)] = a['quantity']
                val += 1
        data['entry_dic'] = entry_dic
        return JsonResponse(data)

#=====================================================================================
#   PRINT DEBIT_NOTE VOUCHER
#=====================================================================================
#
def print_debit_note(request, ins):

    template_name = 'app/app_files/debit_note/print_debit_note.html'
    # Initialize 
    data = defaultdict()
    try:
        debit_note = debit_note_model.DebitNote.objects.get(pk = int(ins))
        organisation = Organisations.objects.get(user = request.user)
        organisation_contact = Organisation_Contact.objects.filter(organisation = organisation)
        
        debit_item = debit_note_model.DebitNoteItems.objects.filter(Q(user= request.user) & Q(debit_note_list = debit_note))
        # contact = Contacts.objects.get(pk = int(invoice.invoice_customer_id))
        address = users_model.User_Address_Details.objects.filter(Q(organisation = organisation) & Q(is_organisation = True) & Q(is_user = True) & Q(default_address = True))
        # org_bank_details = users_model.User_Account_Details.objects.filter(Q(organisation = organisation) & Q(is_organisation = True) & Q(is_user = True) & Q(default_bank = True)) 

        # customer_gst = User_Tax_Details.objects.get(contact = invoice.invoice_customer_id)
        # customer_address = users_model.User_Address_Details.objects.filter(Q(contact = invoice.invoice_customer_id) & Q(default_address = True))

            
    except:
        return redirect('/unauthorized/', permanent=False)

    

    # data["contact_name"] = invoice.invoice_customer
        
    data["debit_note"] = debit_note
    
    data["debit_item"] = debit_item
    data['organisation'] = organisation

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
    if(len(organisation_contact) != 0):
        data['organisation_contact'] = organisation_contact[0]
    # data['contact'] = contact
    
    
    return render(request,template_name,data)