from django.forms import *
from app.models.accounts_model import *
from django.contrib.auth.models import User

from app.other_constants import *

#
#
#
class AccGroupsForm(ModelForm):

    class Meta:
        model = AccGroups
        fields = ('group_name', 'group_info')

        widgets = {
            'group_name' : TextInput(attrs = {'class':'form-control input-sm','onclick':'check()','style':'padding-left: 0px;',}),
            'group_info': Textarea(attrs={'class':'form-control input-sm','style':'padding-left: 0px;',}),
        }

#
#
#
class AccLedgerForm(ModelForm):

    class Meta:
        model = AccLedger

        fields = ('acc_group', 'accounts_name', 'major_heads', 'info_message', 'description')
        
        widgets = {
            'acc_group' : Select(attrs = {'class':'form-control input-sm select', 'onchange':'openNewGroupModal($(this)),check()'}),
            'accounts_name' : TextInput(attrs = {'class':'form-control input-sm','onclick':'check()','style':'text-transform: capitalize;',}),
            'major_heads' : Select(attrs = {'class':'form-control input-sm', 'onchange':'get_predefined_groups($(this)),check()'},),
            'info_message' : Textarea(attrs={'class':'form-control input-sm'}),
            'description' : Textarea(attrs={'class':'form-control input-sm'}),
        }