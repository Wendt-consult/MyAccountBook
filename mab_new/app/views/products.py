from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse
from django.views import View
from collections import OrderedDict, defaultdict
from django.db.models import *
from app.models import *
from app.models import products_model 
from app.forms.products_form import * 
from app.forms import *

from django.conf import settings

import json, shutil


#========================================================================================
#   VIEW/LIST PRODUCTS
#========================================================================================
#

def check_existing_product(request):
    if request.GET["ins"]:
        product = products_model.ProductsModel.objects.filter(product_name__iexact = request.GET["ins"],user = request.user)
        value = ""
        if request.GET["add_form"] == "1" and request.GET["prod_id"]:
            product = product.exclude(pk = int(request.GET["prod_id"]))
            
            p_name = products_model.ProductsModel.objects.get(pk = int(request.GET["prod_id"]))
            value = p_name.product_name
            
        product = {"counter":product.count(), "pre_val":value}
        return JsonResponse(product)   

#========================================================================================
#   VIEW/LIST PRODUCTS
#========================================================================================
#
def view_products(request, *args, **kwargs):
    # Template 
    template_name = 'app/app_files/products/index.html'

    # Initialize 
    data = defaultdict()
    data["view"] = ""
    data["products"] = {}
    # Custom CSS/JS Files For Inclusion into template
    data["css_files"] = []
    data["js_files"] = ['custom_files/js/product.js',]
    data["active_link"] = 'Products'
    data["breadcrumb_title"] = 'PRODUCTS'

    data["included_template"] = 'app/app_files/products/view_products.html'

    #*****************************************************************************
    # PRODUCT LISTING
    #*****************************************************************************

    search = request.GET.get('search',False)

    product_type = request.GET.getlist('product_type[]')

    is_active = request.GET.getlist('is_active[]')
    products = ProductsModel.objects.prefetch_related('productphotos_set').filter(Q(user = request.user) & Q(product_delete_status = 0))
    if search:
        products = products.filter(Q(sku__contains = search) | Q(product_name__contains = search))
   
    if product_type:
        products = products.filter(product_type__in = product_type)

    if is_active:
        products = products.filter(is_active__in = is_active)
    else:
        products = products.filter(is_active = True)   

    data["products"] = products

    return render(request, template_name, data)    

#========================================================================================
# ADD PRODUCT
#========================================================================================
# 
class AddProducts(View):

    # Template 
    template_name = 'app/app_files/products/add_products_form.html'

    # Initialize 
    data = defaultdict()
    data["view"] = ""

    # Custom CSS/JS Files For Inclusion into template
    data["css_files"] = []
    data["js_files"] = ['custom_files/js/product.js']
    data["active_link"] = 'Products'
    data["breadcrumb_title"] = 'PRODUCTS'

    data["included_template"] = 'app/app_files/products/add_products_form.html'

    data["add_product_images_form"] = ProductPhotosForm()
    data["ledger_form"] = accounts_ledger_forms.AccLedgerForm()
    data["groups_form"] = accounts_ledger_forms.AccGroupsForm()
    #
    #
    #
    def get(self, request, *args, **kwargs):
        self.data["add_product_form"] = ProductForm(request.user)
        return render(request, self.template_name, self.data)

    def post(self, request, *args, **kwargs):                         
        
        add_product = ProductForm(request.user, request.POST or None)
        add_images = ProductPhotosForm(request.FILES or None)
        ins = None

        if add_product.is_valid():
            ins = add_product.save()            
            ins.user = request.user
            ins.save()
        else:
            raise Http404             

        if add_images.is_valid() and ins is not None:
            for img in request.FILES.getlist('product_image'):
                img_save = ProductPhotos(
                    product_image = img,
                    product = ins
                )

                img_save.save()
        

        product_names = request.POST.getlist("prod_name[]")
        qty = request.POST.getlist("qty[]")

        for i in range(len(product_names)):
            try:
                product = ProductsModel.objects.get(pk = int(product_names[i]))

                obj = BundleProducts(
                    product_bundle = ins,
                    product = product,
                    quantity = int(qty[i]) if qty[i] != "" else 0
                )

                obj.save()
            except:
                pass

        return redirect('/products/', permanent = False)

#=========================================================================================
# PRODUCT DELETE
#=========================================================================================
#
def delete_product(request, ins = None):
    if ins is not None:
        try:
            product = ProductsModel.objects.get(pk = int(ins))
        except:
            return redirect('/unauthorized/', permanent=False)

        product.product_delete_status = 1
        product.save()
        return redirect('/products/', permanent=False)
    return redirect('/unauthorized/', permanent=False)


#===================================================================================================
# STATUS CHANGE
#===================================================================================================
#
def status_change(request, slug = None, ins = None):
    
    if slug is not None and ins is not None:
        try:
            product = ProductsModel.objects.get(pk = int(ins))        
        except:
           return redirect('/unauthorized/', permanent=False)

        if slug == 'deactivate':
            product.is_active = False
        elif slug == 'activate':
            product.is_active = True
        else:
            return redirect('/unauthorized/', permanent=False)

        product.save()
        return redirect('/products/', permanent=False)

    return redirect('/unauthorized/', permanent=False)


#===================================================================================================
# STATUS CHANGE
#===================================================================================================
#
class EditProducts(View):

    # Template 
    template_name = 'app/app_files/products/edit_products.html'

    # Initialize 
    data = defaultdict()
    data["view"] = ""

    # Custom CSS/JS Files For Inclusion into template
    data["css_files"] = []
    data["js_files"] = ['custom_files/js/product.js',]
    data["active_link"] = 'Products'
    data["breadcrumb_title"] = 'PRODUCTS'

    data["included_template"] = 'app/app_files/products/edit_products.html'

    data["add_product_images_form"] = ProductPhotosForm()
    
    #
    #
    #
    def get(self, request, *args, **kwargs):

        product = None
        self.data["bundle_products"] = {}

        try:
            product = ProductsModel.objects.get(pk = int(kwargs["ins"]))
        except:
            return redirect('/unauthorized/', permanent=False)

        self.data["product_type"] = product.product_type
        self.data["product_id"] = product.id
        self.data["product"] = product
        self.data["selling_GST"] = product.inclusive_tax
        self.data["purchase_GST"] = product.inclusive_purchase_tax
        self.data["add_product_form"] = EditProductForm(request.user, instance = product)
        if product is not None and product.product_type == 2:
            bundle_item = products_model.BundleProducts.objects.filter(product_bundle = product) 
            product = ProductsModel.objects.filter(Q(user = request.user) & Q(is_active = True) & Q(product_delete_status = 0))
            a = []
            for i in range(0,len(bundle_item)):
                result = product.filter(product_name__iexact = bundle_item[i].product).exists()
                if(result == True):
                    a.append(bundle_item[i])
            if(len(bundle_item) == len(a)):
                self.data['status'] = 'YES'
            else:
                self.data['status'] = 'NO'
            
            self.data["bundle_products"] = a
            self.data["add_bundle_product_form"] = BundleProductForm(request.user, kwargs["ins"])
            self.data['bundle_count'] = len(self.data["bundle_products"]) - 1

        
        return render(request, self.template_name, self.data)

    #
    #
    #
    def post(self, request, *args, **kwargs):
        try:
            product = ProductsModel.objects.get(pk = int(kwargs["ins"]))
        except:
            return redirect('/unauthorized/', permanent=False)

        add_product = EditProductForm(request.user, request.POST or None, instance = product)
        add_images = ProductPhotosForm(request.FILES or None)

        ins = None

        if request.POST.get('hidden_img') is not None:
            pid = request.POST.get('hidden_img')
            try:
                product = products_model.ProductsModel.objects.get(pk = int(pid))
                image = products_model.ProductPhotos.objects.filter(product = product).delete()
            except:
                pass

        if add_product.is_valid():
            ins = add_product.save()
            ins.user = request.user
            ins.save()
        else:
            # Do something in case if form is not valid
            print(add_product.errors.as_data())
            raise Http404             
        if add_images.is_valid() and ins is not None:
            for img in request.FILES.getlist('product_image'):
                img_save = ProductPhotos(
                    product_image = img,
                    product = ins
                )

                products_model.ProductPhotos.objects.filter(product = ins).delete()

                img_save.save()
        if product is not None and product.product_type == 2:
            products_model.BundleProducts.objects.filter(product_bundle = product).delete()

            product_names = request.POST.getlist("prod_name[]")
            qty = request.POST.getlist("qty[]")
            for i in range(len(product_names)):
                try:
                    product = ProductsModel.objects.get(pk = int(product_names[i]))
                    obj = BundleProducts(
                        product_bundle = ins,
                        product = product,
                        quantity = int(qty[i]) if qty[i] != "" else 0
                    )

                    obj.save()
                except:
                    pass

        
        return redirect('/products/', permanent = False)

#
#
#
def ajax_add_product(request):

    if request.POST and request.is_ajax():                        
        
        add_product = ProductForm(request.user, request.POST or None)
        add_images = ProductPhotosForm(request.FILES or None)

        ins = None

        if add_product.is_valid():
            ins = add_product.save()            
            ins.user = request.user
            ins.save()
        
        if add_images.is_valid() and ins is not None:
            for img in request.FILES.getlist('product_image'):
                img_save = ProductPhotos(
                    product_image = img,
                    product = ins
                )

                img_save.save()
        return HttpResponse(1)
    return HttpResponse(0)



#===================================================================================================
# BUNDLE - Commented by Lawrence
#===================================================================================================
#

def bundle(request):
    html = ['<option value="">------</option>']
    
    if request.GET:
        
        prod_type = request.GET["prod_type"]

        if prod_type != '':
            products = ProductsModel.objects.filter(user = request.user, product_type = prod_type).values("id","product_name")
            
            for product in products:
                html.append('<option value="{}">{}</option>'.format(product["id"], product["product_name"]))

    return HttpResponse(''.join(html))

#
#
#
def delete_bundle_product(request, ins = None, obj = None):
    try:
        products_model.BundleProducts.objects.get(pk = int(obj)).delete()
        return redirect('/products/edit/{}/'.format(ins), permanent=False)
    except:
        return redirect('/unauthorized/', permanent=False)

#
#
#
def edit_bundle_product_form(request):
    try:
        quantity = 0
        if request.POST["quantity"]:
            quantity = request.POST["quantity"]
        
        ins = products_model.BundleProducts.objects.get(pk = int(request.POST["obj"]), product_bundle_id = int(request.POST["ins"]))
        ins.quantity = quantity
        ins.save() 
    except:
        pass
    
    return redirect('/products/edit/{}/'.format(request.POST["ins"]), permanent=False)

# #
# #
# #
def add_bundle_product_form(request):
    
    ins = products_model.ProductsModel.objects.get(pk = int(request.POST["ins"]))
    
    quantity = 0
    if request.POST["quantity"]:
        quantity = request.POST["quantity"]

    obj = products_model.BundleProducts(
        product_bundle = ins,
        product_id = int(request.POST["product"]),
        quantity = quantity,
    )

    obj.save()

    return redirect('/products/edit/{}/'.format(request.POST["ins"]), permanent=False)



#****************************************************************************
#  CLONE PRODUCT
#*****************************************************************************
#

class CloneProduct(View):
    
    # Template 
    template_name = 'app/app_files/products/clone_product_form.html'
    
    # Initialize 
    data = defaultdict()
    data["view"] = ""
    data["contacts"] = {}
    data["active_link"] = 'Products'
    data["breadcrumb_title"] = 'PRODUCTS'

    # Custom CSS/JS Files For Inclusion into template
    data["css_files"] = []
    data["js_files"] = ['custom_files/js/product.js']

    data["included_template"] = 'app/app_files/products/clone_product_form.html'
    
    data["product"] = None
    data["add_product_images_form"] = ProductPhotosForm()

    #
    #
    #
    def get(self, request, *args, **kwargs):

        if kwargs["ins"] is not None:
            product = ProductsModel.objects.get(pk = int(kwargs["ins"]))
            self.data["product"] = ProductForm(instance = product, user = request.user)
            self.data["product_data"] = product
            self.data["selling_GST"] = product.inclusive_tax
            self.data["purchase_GST"] = product.inclusive_purchase_tax
            
            
        return render(request, self.template_name, self.data)

    #
    #
    #
    def post(self, request, *args, **kwargs):

        if kwargs["ins"] is not None:
            try:
                product = products_model.ProductsModel.objects.get(pk = int(kwargs["ins"]))
            except:
                return redirect('/unauthorized/', permanent=False)

            image_clone = None
            product_image = None
            
            try:
                image_clone = products_model.ProductPhotos.objects.get(product = product)
            except:
                pass
            
            product.pk = None
            product.product_name = request.POST["product_name"]
            product.sku = request.POST["sku"]
            product.hsn_code = request.POST["hsn_code"]
            product.unit = request.POST["unit"]
            product.product_description = request.POST["product_description"]
            product.tax = request.POST["tax"]
            product.gst = request.POST["gst"]
            product.preferred_currency = request.POST["preferred_currency"]
            product.selling_price = request.POST["selling_price"]
            product.selling_GST = request.POST["selling_GST"]
            product.sales_account = request.POST["sales_account"] if request.POST["sales_account"] else 1
            
            product.save()

            add_images = ProductPhotosForm(request.FILES or None)

            if add_images.is_valid():
                for img in request.FILES.getlist('product_image'):
                    img_save = ProductPhotos(
                        product_image = img,
                        product = product
                    )

                    products_model.ProductPhotos.objects.filter(product = product).delete()

                    img_save.save()   
            else:
                if image_clone is not None:
                    image_clone.pk = None
                    image_clone.product = product   

                    img = str(image_clone.product_image).split(".")
                    img_new = img[0]+"_copy."+img[1] 

                    shutil.copyfile(settings.MEDIA_ROOT+"/"+str(image_clone.product_image), settings.MEDIA_ROOT+"/"+img_new)

                    image_clone.product_image = img_new   
                    image_clone.save()
            
            return redirect('/products/', permanent=False)
        return redirect('/unauthorized/', permanent=False)


#****************************************************************************
#  DELETE PRODUCT IMAGE
#*****************************************************************************
#
def delete_product_image(request, pid = None, img_id = None):

    try:
        product = products_model.ProductsModel.objects.get(pk = int(pid))
        image = products_model.ProductPhotos.objects.filter(product = product).delete()
    except:
        pass

    return HttpResponse(1)