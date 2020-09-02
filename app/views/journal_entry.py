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
from app.models.journalentry_model import JournalEntry,JournalEntry_Items


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
#   view journal entry
#=====================================================================================
#

def view_journalentry(request):
    # Template 
    template_name = 'app/app_files/journal_entry/base.html'
    
    # Initialize 
    data = defaultdict()
    data["view"] = ""
    data["contacts"] = {}
    data["active_link"] = 'Journal Entry'
    data["breadcrumb_title"] = 'JOURNAL ENTRY'
    data['type'] = 'view'

    # Custom CSS/JS Files For Inclusion into template
    data["css_files"] = []
    data["js_files"] = ['custom_files/js/customize_view.js']
    
    data["included_template"] = 'app/app_files/journal_entry/view_journal_entry.html' 
    journalentry_var = journalentry_model.JournalEntry.objects.filter(user = request.user, journal_delete_status = 0)

    data['entry'] = journalentry_var

    return render(request,template_name,data)


#=====================================================================================
#   Journal_entry VIEW
#=====================================================================================
#

def JournalEntry(request,ins):
    # Template 
    template_name = 'app/app_files/journal_entry/add_journal_entry.html'
    
    # Initialize 
    data = defaultdict()
    data["view"] = ""
    data["contacts"] = {}
    data["active_link"] = 'Journal Entry'
    data["breadcrumb_title"] = 'Journal Entry'
    data['type'] = 'add'

    # Custom CSS/JS Files For Inclusion into template
    data["css_files"] = []
    data["js_files"] = ['custom_files/js/customize_view.js','custom_files/js/journal_entry.js']

    # data["included_template"] = 'app/app_files/journal_entry/view_journal_entry.html'     
    if(int(ins) == 0):
        account = accounts_model.MajorHeads.objects.all()
        contacts = Contacts.objects.filter(Q(user = request.user) & Q(is_active = True))
        data['contacts'] = contacts
        data['account_header'] = account
        return render(request, template_name,data)
    elif(int(ins) == 1):
        # for account header
        account = accounts_model.MajorHeads.objects.all()
        account_name = []
        account_ids =[]
        count = len(account)
        for i in range(0,count):
            account_name.append(account[i].major_head_name)
            account_ids.append(account[i].id)
        # for contact
        contacts = Contacts.objects.filter(Q(user = request.user) & Q(is_active = True))
        contact_name = []
        contact_ids =[]
        contact_count = len(contacts)
        for i in range(0,contact_count):
            if(contacts[i].organization_name is not None):
                a = str(contacts[i].contact_name)+' - ('+str(contacts[i].organization_name)+')'
                contact_name.append(a)
            else:
                contact_name.append(contacts[i].contact_name)
            contact_ids.append(contacts[i].id)

        data = {'account_name': account_name, 'account_ids': account_ids, 'contact_name':contact_name,'contact_ids':contact_ids } 
        return JsonResponse(data)

def SaveJournalEntry(request):
    if request.POST:
        name = request.POST.get("journalnumber")
        reference = request.POST.get("Reference")
        Journal_date = request.POST.get("Journalentrydate")
        journalentry_number_check  = request.POST.get("journal_checkbox","off")
        Message  = request.POST.get("Message")
        attachement = request.FILES.get("Attachment")
        debit_SubTotal  = request.POST.get("debit_SubTotal")
        credit_SubTotal  = request.POST.get("credit_SubTotal")
        journalentry_number_check  = request.POST.get("journal_checkbox")

        if 'save_close' in request.POST:
            save_type = 1
        elif 'save_draft' in request.POST:
            save_type = 2
        elif 'save_downaload' in request.POST:
            save_type = 3

        journal = journalentry_model.JournalEntry(
            user = request.user,
            save_type = save_type,
            journalentry_number = name,
            journalentry_date = Journal_date,
            journalentry_refrence = reference,
            journalentry_number_check  = journalentry_number_check,
            Note = Message,
            attachements = attachement,
            total_amount_debit = debit_SubTotal,
            total_amount_credit = credit_SubTotal,
        )
        journal.save()

        account_item = request.POST.getlist('account_header[]',None)
        details = request.POST.getlist('details[]',None)
        contact_name = request.POST.getlist('contactname[]',None)
        debit = request.POST.getlist('debit[]',None)
        credit =request.POST.getlist('credit[]',None)

        count = len(account_item)
        for i in range(0,count):
            accounts = accounts_model.MajorHeads.objects.get(pk = int(account_item[i]))
            contact = Contacts.objects.get(pk = int(contact_name[i]))

            journalentry_item = JournalEntry_Items(
                user = request.user,
                journalentry = journal,
                accounts_items = accounts,
                description = details[i],
                journal_entry_customer = contact,
                debit = debit[i],
                credit = credit[i],
            )
            journalentry_item.save()


        return redirect('/journalentry/', permanent = False)
    return redirect('/journalentry/', permanent = False)

#=====================================================================================
#   Edit JOURNAL ENTRY
#=====================================================================================
#

class EditJournal(View):

    # Template 
    template_name = 'app/app_files/journal_entry/edit_journal_entry.html'
    
    # Initialize 
    data = defaultdict()
    data["view"] = ""
    data["contacts"] = {}
    data["active_link"] = 'Journal Entry'
    data["breadcrumb_title"] = 'Journal Entry'
    data['type'] = 'edit'

    # Custom CSS/JS Files For Inclusion into template
    data["css_files"] = []
    data["js_files"] = ['custom_files/js/customize_view.js','custom_files/js/journal_entry.js']

    # data["included_template"] = 'app/app_files/journal_entry/view_journal_entry.html'


    def get(self, request, *args, **kwargs):
        journalentry_var = journalentry_model.JournalEntry.objects.get(pk = int(kwargs["ins"]))
        journalentry_items_var = journalentry_model.JournalEntry_Items.objects.filter(journalentry = journalentry_var)
        self.data["jornalentry"] = journalentry_var
        self.data["journal_lineitem"] = journalentry_items_var
        self.data['ids'] = journalentry_var.id

        account = accounts_model.MajorHeads.objects.all()
        contacts = Contacts.objects.filter(Q(user = request.user) & Q(is_active = True))
        self.data['contacts'] = contacts
        self.data['account_header'] = account
        self.data['line_count'] = len(journalentry_items_var)-1

        return render(request, self.template_name, self.data)
    
    def post(self, request, *args, **kwargs):
        try:
            journal = journalentry_model.JournalEntry.objects.get(pk = int(kwargs["ins"]))
            # journal_item = JournalEntry_Items.objects.filter(Q(user= request.user) & Q(journalentry = journal))
            
        except:
            # pass
            return redirect('/unauthorized/', permanent=False)
        if request.POST:
            name = request.POST.get("journalnumber")
            reference = request.POST.get("Reference")
            Journal_date = request.POST.get("Journalentrydate")
            journalentry_number_check  = request.POST.get("journal_checkbox","off")
            Message  = request.POST.get("Message")
            attachement = request.FILES.get("Attachment")
            debit_SubTotal  = request.POST.get("debit_SubTotal")
            credit_SubTotal  = request.POST.get("credit_SubTotal")
            journalentry_number_check  = request.POST.get("journal_checkbox")

            if 'save_close' in request.POST:
                save_type = 1
            elif 'save_draft' in request.POST:
                save_type = 2
            elif 'save_downaload' in request.POST:
                save_type = 3

            journalentry_model.JournalEntry.objects.filter(pk = int(kwargs["ins"])).update(
                user = request.user,
                save_type = save_type,
                journalentry_number = name,
                journalentry_date = Journal_date,
                journalentry_refrence = reference,
                journalentry_number_check  = journalentry_number_check,
                Note = Message,
                attachements = attachement,
                total_amount_debit = debit_SubTotal,
                total_amount_credit = credit_SubTotal,
            )

            account_item = request.POST.getlist('account_header[]',None)
            details = request.POST.getlist('details[]',None)
            contact_name = request.POST.getlist('contactname[]',None)
            debit = request.POST.getlist('debit[]',None)
            credit =request.POST.getlist('credit[]',None)

            journalentry_model.JournalEntry_Items.objects.filter(Q(user= request.user) & Q(journalentry = journal)).delete()

            count = len(account_item)
            for i in range(0,count):
                accounts = accounts_model.MajorHeads.objects.get(pk = int(account_item[i]))
                contact = Contacts.objects.get(pk = int(contact_name[i]))

                journalentry_item = JournalEntry_Items(
                    user = request.user,
                    journalentry = journal,
                    accounts_items = accounts,
                    description = details[i],
                    journal_entry_customer = contact,
                    debit = debit[i],
                    credit = credit[i],
                )
                journalentry_item.save()


        return redirect('/journalentry/', permanent = False)


#=====================================================================================
#   CHECK PURCHASE_ORDER UNIQUR AND SET DEFULT
#=====================================================================================
#

def unique_journal_number(request, ins, number):
    data = defaultdict()
    if(ins == 0):
        journal = journalentry_model.JournalEntry.objects.filter(user = request.user)

        count = len(journal)

        if(count == 0):
            data['journal'] = 'JE-0001'
        else:
            inc = count+1
            for i in range(0,count):
                a = 'JE-000'+str(inc)
                result = journal.filter(Q(user = request.user) & Q(journalentry_number__iexact = a)).exists() 
                if(result == True):
                    inc += 1
                elif(result == False):
                    data['journal'] = 'JE-000'+str(inc)
                    break
        
        return JsonResponse(data)
    elif (ins == 1):
        # check credit note number is unquie
        journal = journalentry_model.JournalEntry.objects.filter(Q(user = request.user) & Q(journalentry_number = number))
        count = len(journal)
        if(count == 0):
            data['unique'] = 0
        else:
            data['unique'] = 1
        return JsonResponse(data)

#=====================================================================================
#   SOFT DELETE JOURNAL ENTRY
#=====================================================================================
#
def journalentry_delete(request, ins):
    if ins is not None:
        try:
            journalentry_model.JournalEntry.objects.filter(pk = int(ins)).update(journal_delete_status = 1)
        
        except:
            return redirect('/unauthorized/', permanent=False)

        # Purchase_Items.objects.filter(Q(user= request.user) & Q(purchase_item_list = purchase_order)).delete()
        # PurchaseOrder.objects.get(pk = int(ins)).delete()

        return redirect('/journalentry/', permanent=False)
    return redirect('/unauthorized/', permanent=False)

#=====================================================================================
#   PRINT JOURNAL ENTRY VOUCHER
#=====================================================================================
#
def print_jounal_entry(request, ins):

    template_name = 'app/app_files/journal_entry/print_journal.html'
    # Initialize 
    data = defaultdict()
    try:
        journal_entry = journalentry_model.JournalEntry.objects.get(pk = int(ins))
        organisation = Organisations.objects.get(user = request.user)
        organisation_contact = Organisation_Contact.objects.filter(organisation = organisation)
        
        journal_entry_item = journalentry_model.JournalEntry_Items.objects.filter(Q(user= request.user) & Q(journalentry = journal_entry))
        # contact = Contacts.objects.get(pk = int(invoice.invoice_customer_id))
        address = users_model.User_Address_Details.objects.filter(Q(organisation = organisation) & Q(is_organisation = True) & Q(is_user = True) & Q(default_address = True))
        # org_bank_details = users_model.User_Account_Details.objects.filter(Q(organisation = organisation) & Q(is_organisation = True) & Q(is_user = True) & Q(default_bank = True)) 

        # customer_gst = User_Tax_Details.objects.get(contact = invoice.invoice_customer_id)
        # customer_address = users_model.User_Address_Details.objects.filter(Q(contact = invoice.invoice_customer_id) & Q(default_address = True))

            
    except:
        return redirect('/unauthorized/', permanent=False)

    

    # data["contact_name"] = invoice.invoice_customer
        
    data["journal_entry"] = journal_entry
    
    data["journal_entry_item"] = journal_entry_item
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

    data['organisation_contact'] = organisation_contact[0]
    # data['contact'] = contact
    
    
    return render(request,template_name,data)