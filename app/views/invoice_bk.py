from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse
from django.views import View
from collections import OrderedDict, defaultdict
from django.contrib import messages

from django.conf import settings

from django.template.loader import get_template

from app.models.invoice_model import *
from app.models.collects_model import *
from app.forms.invoice_forms import *
from app.forms.products_form import *
from app.forms.contact_forms import *
from app.forms.tax_form import *

from django.forms import inlineformset_factory

from app.other_constants import country_list

import json

#=====================================================================================
#   CONTACT - INVOICE LIST
#=====================================================================================
#
class Invoice(View):

    # Template 
    template_name = 'app/app_files/invoice/index.html'

    # Initialize 
    data = defaultdict()
    data["view"] = ""
    data["active_link"] = 'Invoice'
    data["included_template"] = 'app/app_files/invoice/manage_invoices.html'
    data["breadcrumb_title"] = 'INVOICE'

    # Custom CSS/JS Files For Inclusion into template
    data["css_files"] = []
    data["js_files"] = []

    def get(self, request, *args, **kwargs):
        self.data["invoice_list"] = InvoiceModel.objects.filter(service_provider = request.user)
        return render(request, self.template_name, self.data)

#=====================================================================================
#   DESIGN INVOICE
#=====================================================================================
#
class InvoiceDesigner(View):
    # Template 
    template_name = 'app/app_files/invoice/index.html'

    # Initialize 
    data = defaultdict()
    data["view"] = ""
    data["active_link"] = 'Invoice'
    data["included_template"] = 'app/app_files/invoice/template_design_form.html'
    data["breadcrumb_title"] = 'INVOICE DESIGNER'

    # Custom CSS/JS Files For Inclusion into template
    data["css_files"] = []
    data["js_files"] = ['custom_files/js/design_template.js']
  
    def get(self, request, *args, **kwargs):

        #
        #   USER PHONE LIST
        #
        records = Profile.objects.filter(user = request.user)
            
        phone_records = records.values('official_phone', 'personal_phone',)    
        PHONE_NUMBERS = []
        for i in phone_records:
            for x in i: 
                if i[x] is not None:
                    PHONE_NUMBERS.append((x,i[x]))
        self.data["PHONE_NUMBERS"] = (tuple(PHONE_NUMBERS))

        #
        #   USER EMAIL ADDRESSES
        #
        email_records = records.values('official_email',) 
        EMAILS = []
        for i in email_records:
            for x in i: 
                if i[x] is not None:
                    EMAILS.append((x,i[x]))
        self.data["EMAILS"] = (tuple(EMAILS))

        #
        #   USER BILLING ADDRESSES
        #
        #billing_addresses = User_Address_Details


        self.data["invoice_design_form"] = InvoiceDesignerForm(request.user)
        return render(request, self.template_name, self.data)

    def post(self, request, *args, **kwargs):
        form = InvoiceDesignerForm(request.user, request.POST, request.FILES or None)
        if form.is_valid():
            obj = form.save(commit = False)
            obj.user = request.user
            obj.save()
            return redirect('/invoice/invoice_designer/manage/', permanent = True)
        return render(request, self.template_name, self.data)    

#=====================================================================================
#   BASE - CREATE INVOICE
#=====================================================================================
#

def manage_invoice_designs(request):
    
    # Template 
    template_name = 'app/app_files/invoice/index.html'

    # Initialize 
    data = defaultdict()
    data["view"] = ""
    data["active_link"] = 'Invoice'
    data["included_template"] = 'app/app_files/invoice/manage_invoice_designs.html'
    data["breadcrumb_title"] = 'INVOICE DESIGNER'

    # Custom CSS/JS Files For Inclusion into template
    data["css_files"] = []
    data["js_files"] = []

    data["designs"] = Invoice_Templates.objects.filter(user = request.user)

    return render(request, template_name, data)


#=====================================================================================
#   CONTACT - CREATE INVOICE
#=====================================================================================
#
class CreateContactInvoice(View):
    
    # Initialize 
    data = defaultdict()
    
    # Template 
    template_name = 'app/app_files/invoice/create_invoice.html'
    data["included_template"] = 'app/app_files/invoice/template_design_form.html'

    # Set link as active in menubar
    data["active_link"] = 'Invoice'

    # Custom CSS/JS Files For Inclusion into template
    data["css_files"] = []
    data['js_files'] = ['custom_files/js/design_template.js']

    # Initialize Forms
    data["invoice_template_design_form"] = ''

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.data)


#=====================================================================================
#   COLLECTIONS - CREATE INVOICE
#=====================================================================================
#
class CreateCollectionInvoice(View):
    
    # Initialize 
    data = defaultdict()
    
    # Template 
    template_name = 'app/app_files/invoice/create_invoice.html'
    data["included_template"] = 'app/app_files/invoice/create_collection_invoice_form.html'

    # Set link as active in menubar
    data["active_link"] = 'Invoice'

    # Custom CSS/JS Files For Inclusion into template
    data["css_files"] = []
    data['js_files'] = ['custom_files/js/design_template.js']

    data["balance_amount"] = 0.00
    data["paid_amount"] = 0.00
    data["discount"] = 0.00
    data["gst"] = 0.00
    data["igst"] = 0.00
    data["cgst"] = 0.00
    data["sgst"] = 0.00
    data["total_gst"] = 0.00
    data["shipping"] = 0.00
    data["total_amount"] = 0.00

    #
    #
    #
    def get(self, request, *args, **kwargs):

        ins = int(self.kwargs['ins'])

        try:
            collect = Collections.objects.get(pk = ins)
        except:
            return redirect('/unauthorized/', permanent = True)

        try:
            self.data["contact_details"] = Contacts.objects.get(pk = collect.contact.id)
        except:
            return redirect('/unauthorized/', permanent = True)

        #
        #   INVOICE TEMPLATE DETAILS
        #
        inv = Invoice_Templates.objects.filter(user = request.user)
        inv_details = inv.values()[0]

        self.data["template_logo"] = inv_details["logo"]

        #
        # Profile & Address Details
        #

        profile = Profile.objects.get(user = request.user)

        #
        # USER - FIRSTNAME & LASTNAME
        #
        self.data["template_username"] = ""

        if inv_details["user_display_name"]:
            self.data["template_username"] = request.user.first_name.upper()+" "+request.user.last_name.upper()
        else:
            self.data["template_username"] = inv_details["user_custom_name"]

        #
        # CONTACT - FIRSTNAME & LASTNAME
        #
        self.data["template_contact_name"] = self.data["contact_details"].contact_name.upper()
        
        #
        # EMAIL ON TEMPLATE
        #
        self.data["template_email"] = ""

        if inv_details["user_email"] is not None:
            if inv_details["user_email"] == 'official_email':
                self.data["template_email"] = profile.official_email
            else:
                self.data["template_email"] = profile.personal_email
        else:
            if request.user.email is not None: 
                self.data["template_email"] = request.user.email   

        self.data["invoice_templates"] = inv.values('id', 'template_name')

        #
        # PHONE ON TEMPLATE
        #
        self.data["template_phone"] = ""

        if inv_details["user_phone"] is not None:
            if inv_details["user_phone"] == 'official_phone':
                self.data["template_phone"] = profile.official_phone
            else:
                self.data["template_phone"] = profile.personal_phone

        #
        # BILLING ADDRESS OF USER ON THE TEMPLATE 
        #
        self.data["user_billing_address"] = []

        if inv_details["billing_address_id"] is not None:
            
            try:
                billing_address = User_Address_Details.objects.get(user = request.user, pk = inv_details["billing_address_id"])
                self.data["user_billing_address"].append(billing_address.flat_no)
                self.data["user_billing_address"].append(billing_address.street)
                self.data["user_billing_address"].append(billing_address.city+" - "+billing_address.pincode)
                self.data["user_billing_address"].append(billing_address.state)
                self.data["user_billing_address"].append(country_list.COUNTRIES_LIST_DICT[billing_address.country])
            except:    
                pass

        self.data["user_billing_address"] = ',<br>'.join(self.data["user_billing_address"]).upper()

        #
        # CONTACT BILLING & SHIPPING DETAILS
        #
        self.data["contact_shipping_address"] = []

        try:
            contact_shipping_address = Contact_Addresses.objects.get(contact = self.data["contact_details"], is_shipping_address = True)
             
            self.data["contact_shipping_address"].append(contact_billing_address.contact_name)
            self.data["contact_shipping_address"].append(contact_billing_address.flat_no)
            self.data["contact_shipping_address"].append(contact_billing_address.street)
            self.data["contact_shipping_address"].append(contact_billing_address.city+" - "+contact_billing_address.pincode)
            self.data["contact_shipping_address"].append(contact_billing_address.state)
            self.data["contact_shipping_address"].append(country_list.COUNTRIES_LIST_DICT[contact_billing_address.country])
        except:
            pass

        self.data["contact_shipping_address"] = ',<br>'.join(self.data["contact_shipping_address"]).upper()

        #
        # COLLECTION DETAILS
        #
        self.data["collections"] = collect
        self.data["partial_collections"] = CollectPartial.objects.filter(collect_part = collect)
        
        #
        # AMOUNTS CALCULATIONS
        #
        total_paid_qset = self.data["partial_collections"].filter(collection_status = 2).values()

        paid = 0
        for record in total_paid_qset:
            if record["collection_status"] == 2:
                paid += record["amount"]

        if collect.collection_status == 3:
            self.data["paid_amount"] = collect.amount
        else:
            balance_amount = collect.amount - paid
            if balance_amount > 0 :
                self.data["balance_amount"] = balance_amount
            else:
                self.data["paid_amount"] = paid 

        #
        # INVOICE FORM
        #      
        self.data["invoice_form"] = InvoiceForm()
        return render(request, self.template_name, self.data)

    #
    # 
    #     
    def post(self, request, *args, **kwargs):
        ins = int(self.kwargs['ins'])
        self.data["invoice_form"] = InvoiceForm()

        try:
            collect = Collections.objects.get(pk = ins)
        except:
            return redirect('/unauthorized/', permanent = True)

        try:
            contact_details = Contacts.objects.get(pk = collect.contact.id)
        except:
            return redirect('/unauthorized/', permanent = True)

        invoice_form = InvoiceForm(request.POST or None)

        if invoice_form.is_valid():
            obj = invoice_form.save()
            obj.service_provider = request.user
            obj.service_recipient = contact_details
            obj.collect = collect
            obj.save()

            return redirect('/invoice/create_invoice/collections/{}'.format(ins), permanent = False)
        return render(request, self.template_name, self.data)

#
#
#
def get_pdf(request, ins = None):
    
    if ins is None:
        return redirect('/unauthorized/', permanent = False)

    # Template 
    template_name = 'app/app_files/invoice/index.html'

    # Initialize 
    data = defaultdict()
    data["view"] = ""
    data["active_link"] = 'Invoice'
    data["included_template"] = 'app/app_files/invoice/temp_invoice.html'

    # Custom CSS/JS Files For Inclusion into template
    data["css_files"] = []
    data["js_files"] = ['custom_files/js/jspdf.js','custom_files/js/html2canvas.js', 'custom_files/js/download_pdf.js']

    data["balance_amount"] = 0.00
    data["paid_amount"] = 0.00
    data["discount"] = 0.00
    data["gst"] = 0.00
    data["igst"] = 0.00
    data["cgst"] = 0.00
    data["sgst"] = 0.00
    data["total_gst"] = 0.00
    data["shipping"] = 0.00
    data["total_amount"] = 0.00

    data["invoice"] = InvoiceModel.objects.get(pk = ins)

    collect = Collections.objects.get(pk = data["invoice"].collect.id)
    data["contact_details"] = Contacts.objects.get(pk = data["invoice"].service_recipient.id)
    
    #
    #   INVOICE TEMPLATE DETAILS
    #
    inv = Invoice_Templates.objects.filter(user = request.user)
    inv_details = inv.values()[0]

    #
    # Profile & Address Details
    #

    profile = Profile.objects.get(user = request.user)

    #
    # USER - FIRSTNAME & LASTNAME
    #
    data["template_username"] = ""

    if inv_details["user_display_name"]:
        data["template_username"] = request.user.first_name.upper()+" "+request.user.last_name.upper()
    else:
        data["template_username"] = inv_details["user_custom_name"]

    #
    # CONTACT - FIRSTNAME & LASTNAME
    #
    data["template_contact_name"] = data["contact_details"].contact_name.upper()
    
    #
    # EMAIL ON TEMPLATE
    #
    data["template_email"] = ""

    if inv_details["user_email"] is not None:
        if inv_details["user_email"] == 'official_email':
            data["template_email"] = profile.official_email
        else:
            data["template_email"] = profile.personal_email
    else:
        if request.user.email is not None: 
            data["template_email"] = request.user.email   

    data["invoice_templates"] = inv.values('id', 'template_name')

    #
    # PHONE ON TEMPLATE
    #
    data["template_phone"] = ""

    if inv_details["user_phone"] is not None:
        if inv_details["user_phone"] == 'official_phone':
            data["template_phone"] = profile.official_phone
        else:
            data["template_phone"] = profile.personal_phone

    #
    # BILLING ADDRESS OF USER ON THE TEMPLATE 
    #
    data["user_billing_address"] = []

    if inv_details["billing_address_id"] is not None:
        
        try:
            billing_address = User_Address_Details.objects.get(user = request.user, pk = inv_details["billing_address_id"])
            data["user_billing_address"].append(billing_address.flat_no)
            data["user_billing_address"].append(billing_address.street)
            data["user_billing_address"].append(billing_address.city+" - "+billing_address.pincode)
            data["user_billing_address"].append(billing_address.state)
            data["user_billing_address"].append(country_list.COUNTRIES_LIST_DICT[billing_address.country])
        except:    
            pass

    data["user_billing_address"] = ',<br>'.join(data["user_billing_address"]).upper()

    #
    # CONTACT BILLING & SHIPPING DETAILS
    #
    data["contact_shipping_address"] = []

    try:
        contact_shipping_address = Contact_Addresses.objects.get(contact = data["contact_details"], is_shipping_address = True)
            
        data["contact_shipping_address"].append(contact_billing_address.contact_name)
        data["contact_shipping_address"].append(contact_billing_address.flat_no)
        data["contact_shipping_address"].append(contact_billing_address.street)
        data["contact_shipping_address"].append(contact_billing_address.city+" - "+contact_billing_address.pincode)
        data["contact_shipping_address"].append(contact_billing_address.state)
        data["contact_shipping_address"].append(country_list.COUNTRIES_LIST_DICT[contact_billing_address.country])
    except:
        pass

    data["contact_shipping_address"] = ',<br>'.join(data["contact_shipping_address"]).upper()

    #
    # COLLECTION DETAILS
    #
    data["collections"] = collect
    data["partial_collections"] = CollectPartial.objects.filter(collect_part = collect)
    
    #
    # AMOUNTS CALCULATIONS
    #
    total_paid_qset = data["partial_collections"].filter(collection_status = 2).values()

    paid = 0
    for record in total_paid_qset:
        if record["collection_status"] == 2:
            paid += record["amount"]

    if collect.collection_status == 3:
        data["paid_amount"] = collect.amount
    else:
        balance_amount = collect.amount - paid
        if balance_amount > 0 :
            data["balance_amount"] = balance_amount
        else:
            data["paid_amount"] = paid 

    return render(request, template_name, data)


#
#
#
#
class CreateInvoice(View):

    # Template 
    template_name = 'app/app_files/invoice/index.html'

    # Initialize 
    data = defaultdict()
    data["view"] = ""
    data["active_link"] = 'Invoice'
    data["included_template"] = 'app/app_files/invoice/add_invoice.html'
     
    # Custom CSS/JS Files For Inclusion into template
    data["css_files"] = []
    data['js_files'] = ['custom_files/js/invoice.js', 'custom_files/js/contacts.js']
    
    ProductFormSet = inlineformset_factory(
            InvoiceModel, InvoiceProducts, extra = 1, 
            fields=('product', 'quantity', 'inventory'),
            widgets = {
                'product' : Select(attrs = {'class':'form-control input-sm product_dropdown_select', 'onchange':'get_product_details($(this))'},),
                'quantity' : NumberInput(attrs = {'class':'form-control input-sm', 'onchange': 'product_quantity($(this))'},),
            }    
        )


    #
    #
    #
    def get(self, request, *args, **kwargs):

        self.data["invoice_form"] = LessInvoiceForm(request.user)

        self.data["add_product_form"] = ProductForm(request.user)
        self.data["add_product_images_form"] = ProductPhotosForm()

        self.data["formset"] = self.ProductFormSet(queryset = ProductsModel.objects.filter(user = request.user))


        self.data["contact_form"] = ContactsForm()
        self.data["social_form"] = ContactsExtraForm()
        self.data["tax_form"] = TaxForm()
        self.data["other_details_form"] = OtherDetailsForm()
        self.data["contact_address_form_1"] = ContactsAddressForm(prefix = 'form1')
        self.data["contact_address_form_2"] = ContactsAddressForm(prefix = 'form2')
        self.data["contact_address_form_3"] = ContactsAddressForm(prefix = 'form3')
        self.data["contact_account_details_form"] = ContactAccountDetailsForm()

        return render(request, self.template_name, self.data)

    #
    #
    #
    def post(self, request):

        invoice_form = LessInvoiceForm(request.user, request.POST)
        if invoice_form.is_valid():
            invoice = invoice_form.save()

            formset = self.ProductFormSet(request.POST)
            if formset.is_valid():

                rownum = 0

                for form in formset:
                    if form.is_valid():
                        if form.data["invoiceproducts_set-"+str(rownum)+"-product"]:
                            obj = form.save(commit = False)
                            obj.invoice = invoice
                            obj.save()
                        rownum +=1

            return redirect('/invoice/view_invoice/{}/'.format(invoice.id), permanent = False)

        else:
            return render(request, self.template_name, self.data)

        
#
#
#
class ViewInvoice(View):

    # Template 
    template_name = 'app/app_files/invoice/index.html'

    # Initialize 
    data = defaultdict()
    data["view"] = ""
    data["active_link"] = 'Invoice'
    data["included_template"] = 'app/app_files/invoice/invoice_template.html'
    
    # Custom CSS/JS Files For Inclusion into template
    data["css_files"] = []
    data['js_files'] = ['custom_files/js/invoice.js']

    #
    #
    #
    def get(self, request, ins = None):

        if ins is not None:

            try:
                invoice = InvoiceModel.objects.get(pk = int(ins))
                self.data["invoice_details"] = invoice
            except:
                return redirect('/unauthorized/', permanent=False)

            contact_address = Contact_Addresses.objects.filter(contact_id = invoice.service_recipient.id)

            self.data["invoice_products"] = InvoiceProducts.objects.filter(invoice = invoice)

            return render(request, self.template_name, self.data)
        return redirect('/unauthorized/', permanent = False)

