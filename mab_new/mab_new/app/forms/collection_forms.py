from django.forms import *
from app.models.collects_model import *
from app.models.contacts_model import *
from django.contrib.auth.models import User

from app.other_constants import *

class CollectionsForm(ModelForm):

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(CollectionsForm, self).__init__(*args, **kwargs)
        self.fields['contact'].queryset = Contacts.objects.filter(user = self.user)

    class Meta:

        model = Collections
        fields = (
                    'contact', 'collection_due_date', 'amount', 'payment_type',
                    'collection_status', 'collection_date', 'currency_type',
                )

        widgets = {
            'contact' : Select(attrs={'class':'form-control input-sm'}),
            'collection_due_date' : DateInput(attrs={'class':'form-control input-sm', 'data-toggle':'datepicker'}),
            'amount' : NumberInput(attrs={'class':'form-control input-sm'}),
            'payment_type' : Select(attrs={'class':'form-control input-sm'}, choices = payment_constants.PAYMENT_TYPE),
            'collection_status' : Select(attrs={'class':'form-control input-sm'}, choices = payment_constants.COLLECTION_STATUS),
            'currency_type' : Select(attrs={'class':'form-control input-sm'}, choices = currency_list.CURRENCY_CHOICES),
            'collection_date' : DateInput(attrs={'class':'form-control input-sm','data-toggle':'datepicker'}),
        }

class CollectPartialForm(ModelForm):
    class Meta:

        model = CollectPartial
        fields = (
                    'collection_due_date', 'amount', 'payment_type',
                    'collection_status', 'collection_date', 'currency_type',
                )

        widgets = {
            'collection_due_date' : DateInput(attrs={'class':'form-control input-sm', 'data-toggle':'datepicker'}),
            'amount' : NumberInput(attrs={'class':'form-control input-sm'}),
            'payment_type' : Select(attrs={'class':'form-control input-sm'}, choices = payment_constants.PAYMENT_TYPE),
            'collection_status' : Select(attrs={'class':'form-control input-sm'}, choices = payment_constants.PARTIAL_COLLECTION_STATUS),
            'collection_date' : DateInput(attrs={'class':'form-control input-sm','data-toggle':'datepicker'}),
            'currency_type' : Select(attrs={'class':'form-control input-sm'}, choices = currency_list.CURRENCY_CHOICES),
        }