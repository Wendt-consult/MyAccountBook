from django.forms import *
from django.contrib.auth.models import User
from app.models import *
from app.other_constants import *

#
#
#
class ProfileForm(ModelForm):
    class Meta:
        model = users_model.Profile
        fields = ('app_id', 'display_name', 'salutation', 'customer_type', 'phone', 'fax', 'pan', 'website',
                'facebook', 'twitter', 'skype', 'linkedin')

        widgets = {
            'app_id' : TextInput(attrs={'class':'form-control input-sm','disabled':'true'}),
            'display_name' : TextInput(attrs={'class':'form-control input-sm', 'max_length':'200','style':'padding-left: 9px;',}),
            'salutation' : Select(attrs={'class':'form-control input-sm',}, choices = user_constants.SALUTATIONS),
            'customer_type': Select(attrs={'class':'form-control input-sm',}, choices = user_constants.CUSTOMER_TYPE),
            'phone':  NumberInput(attrs={'class':'form-control input-sm','placeholder':'10 digit phone number','style':'padding-left: 9px;','onkeyup':'setMessage($(this))', 'onfocusout':'valid_Phone($(this))'}),
            'fax' :  NumberInput(attrs={'class':'form-control input-sm','placeholder':'10 digit phone number','style':'padding-left: 9px;','onkeyup':'setMessage($(this))', 'onfocusout':'valid_Phone($(this))'}),
            'website': TextInput(attrs={'class':'form-control input-sm', 'onkeyup':'valid_URL($(this))', 'onfocusout':'valid_URL($(this))'}),
            'facebook' : TextInput(attrs={'class':'form-control input-sm', 'max_length':'200','onkeyup':'valid_URL($(this))', 'onfocusout':'valid_URL($(this))'}),
            'twitter' : TextInput(attrs={'class':'form-control input-sm', 'max_length':'200', 'onkeyup':'valid_URL($(this))', 'onfocusout':'valid_URL($(this))'}),
            'skype' :TextInput(attrs={'class':'form-control input-sm',}), 
            'linkedin' : TextInput(attrs={'class':'form-control input-sm', 'onkeyup':'valid_URL($(this))', 'onfocusout':'valid_URL($(this))'}),
            'pan' : TextInput(attrs = {'class':'form-control input-sm','placeholder':'Eg. ABCDE1234D','style':'padding-left: 9px;','onkeyup':'valid_PAN($(this))', 'onfocusout':'valid_PAN($(this))'}), 
        }

#
#
#
class OrganisationForm(ModelForm):
    class Meta:
        model = users_model.Organisations
        fields = ('organisation_name', 'organisation_legal_name', 'flat_no', 'logo', 'street', 'city', 
                'state', 'country', 'pincode', 'organisation_description', 'line_of_business', 
                'organisation_type', 'organisation_pan', 'organisation_cin')

        widgets = {
            'organisation_name' : TextInput(attrs={'class':'form-control input-sm', 'required':'true'}),
            'organisation_legal_name' : TextInput(attrs={'class':'form-control input-sm', 'required':'true'}),
            'flat_no' : TextInput(attrs={'class':'form-control input-sm',}),
            'street' : TextInput(attrs={'class':'form-control input-sm', }),
            'city' : TextInput(attrs={'class':'form-control input-sm', }),
            'state' : Select(attrs={'class':'form-control input-sm',}, choices = country_list.STATE_LIST_CHOICES),
            'country' : Select(attrs={'class':'form-control input-sm',}, choices = country_list.COUNTRIES_LIST_CHOICES),
            'pincode' : TextInput(attrs={'class':'form-control input-sm', }),
            'organisation_description' : Textarea(attrs={"rows":"4",'style':'line-height: 21px !important; width:100%'}),
            'line_of_business' : Select(attrs={'class':'form-control input-sm',}, choices = user_constants.LINE_OF_ORGANISATION),
            'organisation_type' : Select(attrs={'class':'form-control input-sm',}, choices = user_constants.ORGANIZATION_TYPE),
            'organisation_pan' : TextInput(attrs={'class':'form-control input-sm', }),
            'organisation_cin' : TextInput(attrs={'class':'form-control input-sm', }),
            'logo' : FileInput(attrs = {'type':'file', 'accept':'image/jpeg, image/png, image/gif,','style':'display:none'})
        }

#
#
#
class OrganisationContactForm(ModelForm):
    class Meta:

        model = users_model.Organisation_Contact
        fields = ('phone', 'email', 'website', 'fax', 'skype', 'linkedin', 'facebook')

        widgets = {
            'phone' : TextInput(attrs={'class':'form-control input-sm',}),
            'email' : TextInput(attrs={'class':'form-control input-sm',}),
            'website' : TextInput(attrs={'class':'form-control input-sm',}),
            'fax' : TextInput(attrs={'class':'form-control input-sm',}),
            'skype' : TextInput(attrs={'class':'form-control input-sm',}),
            'linkedin' : TextInput(attrs={'class':'form-control input-sm',}),
            'facebook' : TextInput(attrs={'class':'form-control input-sm',}),
        }
        
        
            
            