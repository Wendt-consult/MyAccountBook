from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse
from django.views import View
from collections import OrderedDict, defaultdict
from django.db.models import *
from app.models import *
from app.forms.products_form import * 
from app.helpers import form_creator

import json


#========================================================================================
#   VIEW/LIST STOCK DETAILS
#========================================================================================
#
def view_inventory(request, *args, **kwargs):
    # Template 
    template_name = 'app/app_files/inventory/index.html'

    # Initialize 
    data = defaultdict()
    data["view"] = ""

    # Custom CSS/JS Files For Inclusion into template
    data["css_files"] = []
    data["js_files"] = []
    data["active_link"] = 'Inventory'
    data["breadcrumb_title"] = 'INVENTORY'

    data["included_template"] = 'app/app_files/inventory/view_inventory.html'

    #*****************************************************************************
    # PRODUCT LISTING
    #*****************************************************************************

    inventory = Inventory.objects.filter(user = request.user)
    data["inventory"] = inventory

    return render(request, template_name, data)    


#========================================================================================
#   ADD INVENTORY
#========================================================================================
#
class AddInventory(View):
    # Template 
    template_name = 'app/app_files/inventory/index.html'

    # Initialize 
    data = defaultdict()
    data["view"] = ""

    # Custom CSS/JS Files For Inclusion into template
    data["css_files"] = []
    data["js_files"] = []
    data["active_link"] = 'Inventory'
    data["breadcrumb_title"] = 'INVENTORY'

    data["included_template"] = 'app/app_files/inventory/add_inventory_form.html'

    data["inventory_form"] = InventoryForm() 

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.data)

    def post(self, request, *args, **kwargs):

        inventory_form = InventoryForm(request.POST)

        if inventory_form.is_valid():
            ins = inventory_form.save()
            ins.user = request.user
            ins.save()

            return redirect('/inventory/', permanent = False)
        return redirect('/inventory/add/', permanent = False)
        
#========================================================================================
#   INVENTORY PRODUCTS
#========================================================================================
#

class InventoryProducts(View):

    # Template 
    template_name = 'app/app_files/inventory/index.html'

    # Initialize 
    data = defaultdict()
    data["view"] = ""

    # Custom CSS/JS Files For Inclusion into template
    data["css_files"] = []
    data["js_files"] = ['custom_files/js/inventory_product.js']
    data["active_link"] = 'Inventory'
    data["breadcrumb_title"] = 'INVENTORY'

    data["included_template"] = 'app/app_files/inventory/view_inventory_products.html'

    #
    #
    #
    def get(self, request, *args, **kwargs):

        if 'ins' in kwargs:
            
            try:
                inv = Inventory.objects.get(pk = int(kwargs["ins"]))
                self.data["inventory_name"] = inv.inventory_name
            except:
                return redirect('/unauthorized/', permanent = False)

            self.data["inventory_products"] = InventoryProduct.objects.filter(inventory = int(kwargs["ins"]))
            self.data["inventory_product_form"] = InventoryProductForm(request.user, kwargs["ins"])
            self.data["ins"] = kwargs["ins"]

            return render(request, self.template_name, self.data)
        else:
            return redirect('/inventory/add/', permanent = False)

    #
    #
    #
    def post(self, request, *args, **kwargs):
        
        form = InventoryProductForm(request.user, kwargs["ins"], request.POST)

        if form.is_valid():
            obj = form.save()
            
            try:
                inventory = Inventory.objects.get(pk = int(kwargs["ins"]))
            except:
                return redirect('/unauthorized/', permanent = False)

            obj.inventory = inventory
            obj.save()
            return redirect('/inventory/products/{}/'.format(kwargs["ins"]), permanent = False)
            
        return render(request, self.template_name, self.data)

#========================================================================================
#   DELETE INVENTORY PRODUCTS
#========================================================================================
#
def delete_inventory_product(request, ins = None):
    if ins is not None:
        try:
            product = InventoryProduct.objects.get(pk = int(ins))
            obj = product.inventory_id            
        except:
            return redirect('/unauthorized/', permanent=False)      

        product.delete()
        return redirect('/inventory/products/{}/'.format(obj), permanent=False) 
    return redirect('/unauthorized/', permanent=False)


#========================================================================================
#   DELETE INVENTORY PRODUCTS
#========================================================================================
#
def get_edit_inventory_product_form(request):
    if request.is_ajax():
        if request.POST:
            product_inv = InventoryProduct.objects.get(pk = int(request.POST["ids"]))
            product_form = InventoryProductEditForm(instance = product_inv)
            return HttpResponse(form_creator.get_form_data(product_form))
           
        return HttpResponse('')
    return HttpResponse('')

#
#
#
def edit_inventory_product(request):
    if request.POST:
        product_inv = InventoryProduct.objects.get(pk = int(request.POST["obj_ins"]))
        product_form = InventoryProductEditForm(request.POST, instance = product_inv)

        if product_form.is_valid():
            product_form.save()
    return redirect('/inventory/products/{}/'.format(request.POST["ins"]), permanent = False)