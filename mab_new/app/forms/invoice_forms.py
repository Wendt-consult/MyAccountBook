from django.forms import *
from django.contrib.auth.models import User
from app.models.invoice_model import *
from app.models.users_model import *


#=======================================================================
#   INVOICE DESIGNER FORM
#=======================================================================

class InvoiceDesignerForm(ModelForm):
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(InvoiceDesignerForm, self).__init__(*args, **kwargs)
        self.fields['billing_address'].queryset = User_Address_Details.objects.filter(user = self.user, is_billing_address = True)

    class Meta:
        IS_ACTIVE = ((True, 'YES'), (False, 'NO'))

        TEMPLATE_DESIGN = (
            (1, 'GREEN TEMPLATE'),
            (2, 'ORANGE TEMPLATE'),
            (3, 'BLUE TEMPLATE'),
            (4, 'WHITE TEMPLATE'),
            (5, 'GREY TEMPLATE'),
            (6, 'CUSTOM TEMPLATE'),
        )

        USER_NAME_ON_TEMPLATE = (
            (True, 'USE USER FIRSTNAME LASTNAME'),
            (False,'USE CUSTOM USERNAME'),
        )

        model = Invoice_Templates

        fields = (
            'template_name', 'design_number', 'logo', 'header_bgcolor', 'header_fgcolor', 
            'other_design_colors', 'is_active', 'user_display_name', 'user_custom_name',
            'user_phone', 'user_email', 'billing_address',
        )
        
        widgets = {
            'template_name' : TextInput(attrs={'class':'form-control input-sm', 'required':'true'}),
            'design_number' : Select(attrs={'class': 'form-control input-sm',}, choices = TEMPLATE_DESIGN),
            'logo' : FileInput(attrs={'class':'form-control input-sm',}),
            'header_bgcolor' : TextInput(attrs={'class':'form-control input-sm','type':'color'}),
            'header_fgcolor' : TextInput(attrs={'class':'form-control input-sm','type':'color'}),
            'other_design_colors' : TextInput(attrs={'class':'form-control input-sm','type':'color'}),
            'is_active' : Select(attrs={'class':'form-control input-sm',}, choices = IS_ACTIVE),
            'user_display_name' : Select(attrs={'class':'form-control input-sm',}, choices = USER_NAME_ON_TEMPLATE),
            'user_custom_name' : TextInput(attrs={'class':'form-control input-sm',}),
            'billing_address' : Select(attrs={'class':'form-control input-sm','required':'true'}, ),
        }


#=======================================================================
#   INVOICE FORM
#=======================================================================
class InvoiceForm(ModelForm):
    
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(InvoiceForm, self).__init__(*args, **kwargs)
        self.fields['service_recipient'].queryset = Contacts.objects.filter(user = self.user,)

    class Meta:

        model = InvoiceModel
        fields = (
                    'service_recipient', 'provider_state_code', 'recipient_state_code', 
                    'sac_code', 'service_description', 'cgst', 'igst', 'sgst', 'total_gst', 'shipping', 'discount',
                )

        widgets = {
            'service_recipient' : Select(attrs={'class':'form-control input-sm',}),            
            'provider_state_code' : TextInput(attrs={'class':'form-control input-sm', 'disabled' : 'true'}),
            'recipient_state_code' : TextInput(attrs={'class':'form-control input-sm', 'disabled' : 'true'}),
            'shipping' : TextInput(attrs={'class':'form-control input-sm',}),
            'discount' : TextInput(attrs={'class':'form-control input-sm',}),
            'sac_code' : TextInput(attrs={'class':'form-control input-sm', 'disabled' : 'true'}),
            'service_description' : TextInput(attrs={'class':'form-control input-sm',}),
            'cgst' : TextInput(attrs={'class':'form-control input-sm',}),
            'igst' : TextInput(attrs={'class':'form-control input-sm',}),
            'sgst' : TextInput(attrs={'class':'form-control input-sm',}),
            'total_gst' : TextInput(attrs={'class':'form-control input-sm',}),            
        }

#=======================================================================
#   LESS INVOICE FORM
#=======================================================================
class LessInvoiceForm(ModelForm):
    
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(LessInvoiceForm, self).__init__(*args, **kwargs)
        self.fields['service_recipient'].queryset = Contacts.objects.filter(user = self.user, customer_type__in = [1, 2, 4])
        self.fields['sales_person'].queryset =  Contacts.objects.filter(user = self.user, customer_type = 3)
    

    class Meta:

        model = InvoiceModel
        fields = ('service_recipient', 'service_recipient_address', 'invoice_no', 'sales_person', 'invoice_type', 'recipient_state_code', 
                'due_date', 'terms_invoice', 'message', 'attachments', 'start_date', 'subtotal_inc_tax',
                'frequency', 'repeat_for', 'shipping', 'adjustment', 'subtotal', 'total')

        widgets = {
            'invoice_no' : TextInput(attrs = {'class':'form-control input-sm', 'placeholder': 'Optional'}),
            'terms_invoice' : TextInput(attrs = {'class':'form-control input-sm',}),
            'message' : Textarea(attrs = {'class':'form-control input-sm',}),
            'due_date' : TextInput(attrs = {'class':'form-control input-sm', 'placeholder': 'yyyy-mm-dd'}),
            'recipient_state_code' : Select(attrs = {'class':'form-control input-sm',}, choices = country_list.STATE_LIST_CHOICES),
            'service_recipient' : Select(attrs={'class':'form-control input-sm',}),            
            'service_recipient_address' : Select(attrs={'class':'form-control input-sm',}),            
            'sales_person' : Select(attrs={'class':'form-control input-sm',}),            
            'invoice_type' : Select(attrs={'class':'form-control input-sm',}, choices = products_constant.INVOICE_TYPE),            
            'attachments' : FileInput(attrs = {'class':'form-control input-sm',}),
            'start_date' : TextInput(attrs = {'class':'form-control input-sm', 'placeholder': 'yyyy-mm-dd'}),
            'frequency' : Select(attrs = {'class':'form-control input-sm', }, choices = products_constant.INVOICE_FREQUENCY),
            'shipping' : TextInput(attrs = {'class':'form-control input-sm', 'value':'0',}),
            'repeat_for' : TextInput(attrs = {'class':'form-control input-sm',}),
            'adjustment' : TextInput(attrs = {'class':'form-control input-sm', 'value':'0',}),
            'subtotal' : TextInput(attrs = {'class':'form-control input-sm', 'value':'0', 'readonly':'true'}),
            'subtotal_inc_tax' : TextInput(attrs = {'class':'form-control input-sm', 'value':'0', 'readonly':'true'}),
            'total' : TextInput(attrs = {'class':'form-control input-sm', 'value':'0', 'readonly':'true'}),
        }        
        
class InvoiceProductForm(ModelForm):
    
    class Meta:
        model = InvoiceProducts

        fields = (
                    'product', 'quantity', 'inventory', 
                )

        widgets = {
            'product' : Select(attrs = {'class':'form-control input-sm'},),
            'inventory' : Select(attrs = {'class':'form-control input-sm'},),
            'quantity' : NumberInput(attrs = {'class':'form-control input-sm'},),
        }

        