from django.forms import *
from django.contrib.auth.models import User
from app.models.contacts_model import *
from app.models.users_model import *

class TaxForm(ModelForm):
    class Meta:
        model = User_Tax_Details
        fields = ('pan', 'gstin', 'gst_reg_type')

        widgets = {
            'pan' : TextInput(attrs = {'class':'form-control input-sm','placeholder':'Eg. ABCDE1234D','onkeyup':'setMessage($(this))', 'onfocusout':'valid_PAN($(this))'}), 
            'gstin' : TextInput(attrs = {'class':'form-control input-sm','placeholder':'Eg. 36ARVPS3698F1ZF','onkeyup':'setMessage($(this))', 'onfocusout':'valid_GST($(this))'}), 
            'gst_reg_type' : Select(attrs = {'class':'form-control input-sm','id':'gst_reg','onchange':'hide_gst($(this))',}, choices = user_constants.GST_REG_TYPE), 
        }


class OtherDetailsForm(ModelForm):
    class Meta:
        model = User_Tax_Details
        fields = (
            'preferred_currency', 'opening_balance', 'preferred_payment_method', 
            'invoice_terms', 'bills_terms',
        )

        widgets = {
            'preferred_currency' : Select(attrs = {'class':'form-control input-sm','style':'width:50%;',}, choices = currency_list.CURRENCY_CHOICES), 
            'opening_balance' : TextInput(attrs = {'class':'form-control input-sm','style':'width:50%;','onkeypress':'return restrictAlphabets(event)',}),
            'preferred_payment_method' : Select(attrs = {'class':'form-control input-sm','style':'width:50%;',}, choices = payment_constants.PREFERRED_PAYMENT_TYPE), 
            # 'preferred_delivery' : Select(attrs = {'class':'form-control input-sm','style':'width:50%;',}, choices = payment_constants.PREFERRED_DELIVERY), 
            'invoice_terms' : Select(attrs = {'class':'form-control input-sm','style':'width:50%;',}, choices = payment_constants.PAYMENT_DAYS), 
            'bills_terms' : Select(attrs = {'class':'form-control input-sm','style':'width:50%;',}, choices = payment_constants.PAYMENT_DAYS), 
        }
        
#
#
#
class OrganisationTaxForm(ModelForm):
    class Meta:
        model = User_Tax_Details
        fields = ('gstin', 'gst_reg_type')

        widgets = {
            'gstin' : TextInput(attrs = {'class':'form-control input-sm','placeholder':'Eg. 36ARVPS3698F1ZF','style':'width:70%;', 'onkeyup':'setMessage($(this))', 'onfocusout':'valid_GST($(this))','required':True}), 
            'gst_reg_type' : Select(attrs = {'class':'form-control input-sm','id':'gst_reg','onchange':'hide_gst($(this))','style':'width:70%;','required':True}, choices = user_constants.GST_REG_TYPE), 
        }        


#
#
#
class OrganisationCompositTaxForm(ModelForm):
    class Meta:
        model = User_Tax_Details
        fields = ('gstin', 'gst_reg_type')

        widgets = {
            'gstin' : TextInput(attrs = {'class':'form-control input-sm','placeholder':'Eg. 36ARVPS3698F1ZF','style':'width:110%;', 'onkeyup':'setMessage($(this)),valid_GST($(this)),multiple_state_code($(this))','required':True}), 
            'gst_reg_type' : Select(attrs = {'class':'form-control input-sm','id':'gst_reg','onchange':'hide_gst($(this))','style':'width:70%;','required':True}, choices = user_constants.GST_REG_TYPE), 
        }        

#
#
#
class OrganisationGSTSettingsForm(ModelForm):
    class Meta:
        model = OrganisationGSTSettings
        fields = ('taxname', 'taxname_percent')

        widgets = {
            'taxname' : TextInput(attrs = {'class':'form-control input-sm','required':True}), 
            'taxname_percent' : TextInput(attrs = {'class':'form-control input-sm','onkeypress':'return restrictAlphabets(event),float_profile(event,$(this))','onkeyup':'check_percent($(this))', 'required':True}),  
        }   
#
#
#
class OrganisationCompositeGSTSettingsForm(ModelForm):
    class Meta:
        model = OrganisationCompositeGSTSettings
        fields = ('taxname', 'taxname_percent')

        widgets = {
            'taxname' : TextInput(attrs = {'class':'form-control input-sm','required':True}), 
            'taxname_percent' : TextInput(attrs = {'class':'form-control input-sm','onkeypress':'return restrictAlphabets(event),float_profile(event,$(this))','onkeyup':'check_percent($(this))','required':True}),  
        }   