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

        return render(request, self.template_name, self.data)

#=====================================================================================
#   ADD DEBIT_NOTE
#=====================================================================================
#
def add_debit_note(request):

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

    return render(request, template_name, data)