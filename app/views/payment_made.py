from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse
from django.views import View
from collections import OrderedDict, defaultdict
from django.contrib import messages

from app.models.contacts_model import Contacts
from app.models.users_model import *
# from app.models.products_model import *
from app.models.accounts_model import *
from app.models.purchase_model import *
from app.models.customize_model import *
from app.models.purchasentry_model import *
from app.models.payment_made_model import *
from app.models.expense_model import *

from app.forms.contact_forms import * 
from app.forms.tax_form import *
from app.forms.inc_fomsets import *
from app.forms.accounts_ledger_forms import *

from app.other_constants import user_constants,country_list,payment_constants
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.db.models import Q
import datetime

import json, os, csv

from app.helpers import email_helper

from datetime import datetime

from django.conf import settings
import math

#=====================================================================================
#   PAYMENT MADE VIEW
#=====================================================================================
#

class PaymentMade(View):

    # Template 
    template_name = 'app/app_files/payment_made/base.html'
    
    # Initialize 
    data = defaultdict()
    data["view"] = ""
    data["contacts"] = {}
    data["active_link"] = 'Make Payment'
    data["breadcrumb_title"] = 'MAKE PAYMENT'
    data['type'] = 'view'
    # Custom CSS/JS Files For Inclusion into template
    data["css_files"] = []
    data["js_files"] = ['custom_files/js/customize_view.js']

    data["included_template"] = 'app/app_files/payment_made/view_payment_made.html'
    
    #
    #
    def get(self, request):  
        pay =  PurchasePayment.objects.filter(user = request.user)
        self.data['pay'] = pay
        return render(request, self.template_name, self.data)

#=====================================================================================
#   PURCHASE ENTRY TO MAKE PAYMENT METHOD
#=====================================================================================
#

def makePayment(request,slug):
    if request.POST:
        payment_count = PurchasePayment.objects.filter(user = request.user).count()
        payment_number = None
        if(payment_count > 0 ):
            payment_number = 'PM-000'+str(payment_count + 1)
        else:
            payment_number = 'PM-0001'

        # entry_id = request.POST.get('entry_id')
        # venodr_id = request.POST.get('venodr_id')
        balance_due = request.POST.get('entry_balance')
        pay_amount = request.POST.get('pay_amount')
        payment_type = request.POST.get('payment_type')
        account_ids = request.POST.get("pay_account")
        pay_reference = request.POST.get('pay_reference')
        pay_date = request.POST.get('pay_date')
        # date convert
        pay_date = datetime.strptime(str(pay_date), '%d-%m-%Y').strftime('%Y-%m-%d')
        payment_type = request.POST.get('payment_type')
        pay_notes = request.POST.get('pay_notes')
        pay_file = request.POST.get('pay_file')

        if(slug == 'purchase_entry'):
            purchase_entry = PurchaseEntry.objects.get(pk = int(request.POST.get('entry_id')))
        elif(slug == 'expense'):
            expense = Expense.objects.get(pk = int(request.POST.get('entry_id')))
        contact = contact = Contacts.objects.get(user = request.user, pk = int(request.POST.get('venodr_id')))
        account = accounts_model.AccGroups.objects.get(pk = int(account_ids))
        pay = PurchasePayment(
                user = request.user,
                vendor = contact,
                payment_number = payment_number,
                payment_date = pay_date,
                payment_reference = pay_reference,
                payment_mode = payment_type,
                Note = pay_notes,
                attachements = pay_file,
                Amount = pay_amount,
                account = account,
        )
        if(slug == 'purchase_entry'):
            pay.purchase_entry_reference = purchase_entry
        elif(slug == 'expense'):
            pay.expense = expense

        pay.save()

        # some basic calculation after pay for purchase entry and expense

        if(slug == 'purchase_entry'):
            if(float(balance_due) == float(pay_amount)):
                PurchaseEntry.objects.filter(pk = int(request.POST.get('entry_id'))).update(balance_due = '0.00',entry_status = 3)
            elif(float(balance_due) > float(pay_amount)):
                a = float(balance_due) - float(pay_amount)
                if(purchase_entry.entry_status == 0):
                    PurchaseEntry.objects.filter(pk = int(request.POST.get('entry_id'))).update(balance_due = '%.2f' % a,entry_status = 4)
                else:
                    PurchaseEntry.objects.filter(pk = int(request.POST.get('entry_id'))).update(balance_due = '%.2f' % a)
            return redirect('/view_purchase_entry/', permanent = False)
        elif(slug == 'expense'):
            if(float(balance_due) == float(pay_amount)):
                Expense.objects.filter(pk = int(request.POST.get('entry_id'))).update(total_balance = '0.00',status = 3)
            elif(float(balance_due) > float(pay_amount)):
                a = float(balance_due) - float(pay_amount)
                if(expense.status == 0):
                    Expense.objects.filter(pk = int(request.POST.get('entry_id'))).update(total_balance = '%.2f' % a,status = 4)
                else:
                    Expense.objects.filter(pk = int(request.POST.get('entry_id'))).update(total_balance = '%.2f' % a)
            return redirect('/expense/', permanent = False)

    

#=====================================================================================
#   CHECK MAKE PAYMENT UNIQUR AND SET DEFULT
#=====================================================================================
#

def unique_payment_number(request, ins, number):
    data = defaultdict()
    if(ins == 0):
        payment = PurchasePayment.objects.filter(user = request.user)

        count = len(payment)

        if(count == 0):
            data['payment_number'] = 'PM-0001'
        else:
            inc = count+1
            for i in range(0,count):
                a = 'PM-000'+str(inc)
                result = payment.filter(Q(user = request.user) & Q(payment_number__iexact = a)).exists() 
                if(result == True):
                    inc += 1
                elif(result == False):
                    data['payment_number'] = 'PM-000'+str(inc)
                    break
        
        return JsonResponse(data)
    elif (ins == 1):
        # check credit note number is unquie
        payment = PurchasePayment.objects.filter(Q(user = request.user) & Q(payment_number = number))
        count = len(payment)
        if(count == 0):
            data['unique'] = 0
        else:
            data['unique'] = 1
        return JsonResponse(data)

#=====================================================================================
#   ADD MAKE PAYMENT
#=====================================================================================
#

class addMakePayment(View):
    # Template 
    template_name = 'app/app_files/payment_made/add_new_payment.html'
    
    # Initialize 
    data = defaultdict()
    data["view"] = ""
    data["contacts"] = {}
    data["active_link"] = 'Make Payment'
    data["breadcrumb_title"] = 'MAKE PAYMENT'
    data['type'] = 'add'
    # Custom CSS/JS Files For Inclusion into template
    data["css_files"] = []
    data["js_files"] = ['custom_files/js/make_payment.js','custom_files/js/contacts.js','custom_files/js/common.js',]

    # contact Forms
    data["contact_form"] = ContactsForm()
    data["tax_form"] = TaxForm()
    data["other_details_form"] = OtherDetailsForm()
    data["social_form"] = ContactsExtraForm()
    data["new_address_form"] = EditAddressForm()

    # FORMSETS    
    data["address_formset"] = AddressFormset
    data["accounts_formset"] = AccountsFormset

    # ACCOUNT_LEDGER FORMS
    data["groups_form"] = AccGroupsForm()

    def get(self, request):

        contacts = Contacts.objects.filter(Q(user = request.user) & Q(is_active = True) & Q(contact_delete_status = 0))
        self.data["contacts"] = contacts
        # 
        # for account_ledger details
        major_heads = accounts_model.MajorHeads.objects.get(major_head_name = 'Assets')
        acc_ledger_assets = accounts_model.AccGroups.objects.filter(Q(user = request.user) & Q(major_head = major_heads))
        self.data['acc_ledger_assets'] = acc_ledger_assets
        # for make payment
        self.data['payment_type'] = payment_constants.PAYMENT_TYPE
        return render(request, self.template_name, self.data)

    def post(self,request):
        if request.POST:

            unique_number = request.POST.get("make_pyament_number")
            is_check = request.POST.get("make_pyament_number",'off')
            pay_date = request.POST.get("make_payment_date")
            # change order date formate
            pay_date = datetime.strptime(str(pay_date), '%d-%m-%Y').strftime('%Y-%m-%d')

            vendor = request.POST.get("make_payment_vendor")
            reference = request.POST.get("make_pyament_reference")
            pay_type = request.POST.get("make_payment_type")
            amount = request.POST.get("make_pyament_amount")
            account_ids = request.POST.get("make_payment_account")
            notes = request.POST.get("make_payment_notes")

            contact = Contacts.objects.get(user = request.user, pk = int(vendor))
            account = accounts_model.AccGroups.objects.get(pk = int(account_ids))
            payment = PurchasePayment(
            user = request.user,
            vendor = contact,
            account = account,
            payment_number = unique_number,
            payment_number_check = is_check,
            payment_date = pay_date,
            payment_reference = reference,
            payment_mode = pay_type,
            Note = notes,
            Amount = amount,
            )

            payment.save()

            return redirect('/paymentmade/', permanent = False)