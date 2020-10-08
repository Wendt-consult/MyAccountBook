from django.db import models
from django.contrib.auth.models import User
from app.other_constants import *

from app.models import *
from django.forms import *

#
# ADDRESS FORMSET
#
AddressFormset = inlineformset_factory(contacts_model.Contacts, users_model.User_Address_Details, extra = 2,
    fields = ('default_address', 'address_tag','contact_person', 'flat_no', 'street', 'city', 'state', 'country', 'pincode', 'is_shipping_address_diff', 'is_shipping_address', 'is_billing_address'),
    widgets = {
        'contact_person' : TextInput(attrs={'class':'form-control input-sm','maxlength':'50','style':'width:65%;text-transform: capitalize;',}),
        'flat_no' : TextInput(attrs={'class':'form-control input-sm','maxlength':'200','style':'width:65%;'}),
        'street' : TextInput(attrs={'class':'form-control input-sm','maxlength':'100','style':'width:65%;'}),
        'city' : TextInput(attrs={'class':'form-control input-sm','maxlength':'50','style':'width:65%;text-transform: capitalize;'}),
        'state' : Select(attrs={'class':'form-control input-sm','style':'width:65%;'}, choices = country_list.STATE_LIST_CHOICES),
        'country' : Select(attrs={'class':'form-control input-sm','style':'width:65%;'}, choices = country_list.COUNTRIES_LIST_CHOICES),
        'pincode' : TextInput(attrs={'class':'form-control input-sm','type':'number','maxlength':'10','style':'width:65%;'}),
        'is_shipping_address_diff' : Select(attrs={'class':'form-control input-sm hide','style':'width:40%;display:none;', 'required':'false'}),
        'is_shipping_address' : Select(attrs={'class':'form-control input-sm hide','style':'width:40%;display:none;', 'required':'false'}),
        'is_billing_address' : Select(attrs={'class':'form-control input-sm hide','style':'width:40%;display:none;', 'required':'false'}),
        'default_address' : Select(attrs={'class':'form-control input-sm default_address','style':'width:40%;','hidden':'true'}, choices = user_constants.IS_TRUE),
        'address_tag' : TextInput(attrs={'class':'form-control input-sm','maxlength':'50','style':'width:65%;text-transform: capitalize;'}),
    }
)

#
# ACCOUNTS FORMSET
#

class AccountDetailsForm(ModelForm):
    class Meta:
        model = users_model.User_Account_Details
        fields = ('account_number', 'account_holder_name', 'ifsc_code', 'bank_name', 'bank_branch_name')

        widgets = {
            'account_number' : NumberInput(attrs={'class':'form-control input-sm', 'pattern':'[0-9]',}),
            'account_holder_name' : TextInput(attrs={'class':'form-control input-sm','style':'text-transform: capitalize;'}),
            'ifsc_code' : TextInput(attrs={'class':'form-control input-sm','placeholder':'EX. ABCD1234567','onkeyup':'setMessage($(this))', 'onfocusout':'valid_IFSC($(this))'}),
            'bank_name' : TextInput(attrs={'class':'form-control input-sm','style':'text-transform: capitalize;',}),
            'bank_branch_name' : TextInput(attrs={'class':'form-control input-sm','style':'text-transform: capitalize;',}),
        }

# AccountsFormset = formset_factory(AccountDetailsForm, extra = 1)

class EditAccountDetailsForm(ModelForm):
    class Meta:
        model = users_model.User_Account_Details
        fields = ('account_number', 'account_holder_name', 'ifsc_code', 'bank_name', 'bank_branch_name')

        widgets = {
            'account_number' : NumberInput(attrs={'class':'form-control input-sm', 'pattern':'[0-9]',}),
            'account_holder_name' : TextInput(attrs={'class':'form-control input-sm','style':'text-transform: capitalize;'}),
            'ifsc_code' : TextInput(attrs={'class':'form-control input-sm','placeholder':'EX. ABCD1234567','onkeyup':'setMessage($(this))', 'onfocusout':'valid_IFSC($(this)),bank_details($(this))'}),
            'bank_name' : TextInput(attrs={'class':'form-control input-sm','style':'text-transform: capitalize;',}),
            'bank_branch_name' : TextInput(attrs={'class':'form-control input-sm','style':'text-transform: capitalize;',}),
        }

# AccountsFormset = formset_factory(EditAccountDetailsForm, extra = 1)

