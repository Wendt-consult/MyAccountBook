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

from app.other_constants import user_constants,country_list
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.db.models import Q
import datetime

import json, os, csv

from app.helpers import email_helper

from datetime import datetime

from django.conf import settings

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
    data["active_link"] = 'Payment Made'
    data["breadcrumb_title"] = 'PAYMENT MADE'
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