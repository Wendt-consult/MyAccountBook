from django.forms import * 
from app.models.products_model import *
from app.other_constants import *

#===================================================================================
# PRODUCT FORM
#===================================================================================
#

class ProductForm(ModelForm):
        
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(ProductForm, self).__init__(*args, **kwargs)
        
    class Meta:
        model = ProductsModel

        fields = (
            'product_type', 'sku', 'product_name', 'product_description', 
            'purchase_price','selling_price', 'discount', 'tds', 'selling_tax', 'purchase_account',
            'hsn_code', 'abatement', 'unit', 'sales_account', 'inclusive_tax','hidden_img',
            'purchase_tax','inclusive_purchase_tax','reverse_charges','purchase_account','is_sales','is_purchase',
        )

        widgets = {
            
            'product_type' : Select(attrs = {'class':'form-control input-sm', 'onchange':'show_bundle($(this))'}, choices = products_constant.PRODUCT_TYPE),
            'sku' : TextInput(attrs = {'class':'form-control input-sm',}),
            'product_name' : TextInput(attrs = {'class':'form-control input-sm', 'onfocusout':'check_product_name($(this), true)'}),            
            'hsn_code' : TextInput(attrs = {'class':'form-control input-sm',}),
            'product_description' : Textarea(attrs = {'class':' input-sm', 'rows':'2', 'style':'width:100%;background-color: #202940;color: white;'}), 
            'tds' : TextInput(attrs = {'class':'form-control input-sm','onkeypress':'return restrictAlphabets(event)',}),      
            'unit' : Select(attrs = {'class':'form-control input-sm',}, choices = products_constant.UNITS), 
            'hidden_img' : TextInput(attrs = {'class':'form-control input-sm',}),     
            
            # Selling Information

            'is_sales' : CheckboxInput(attrs={'class':'form-check-input', 'style':'margin-left:1%',}),
            # 'preferred_currency' : Select(attrs = {'class':'form-control input-sm','onchange':'select_change()','style':'width: 15%;position: absolute;margin-top: 7px;color: black;background-color: silver;',}, choices = products_constant.Currency ),
            'selling_price' : TextInput(attrs = {'class':'form-control input-sm','onkeypress':'return restrictAlphabets(event), float_value(event,"id_selling_price")','onkeyup':'change_SP()','style':'margin-top:4px',}),
            'selling_tax' : TextInput(attrs = {'class':'form-control input-sm','onkeypress':'return restrictAlphabets(event), float_value(event,"id_selling_tax")', 'onkeyup':'change_SP()'}),
            'inclusive_tax' : TextInput(attrs = {'class':'form-control input-sm','onkeypress':'return restrictAlphabets(event)','style':'width: 100%;', }),
            'sales_account' : Select(attrs = {'class':'form-control input-sm',},),

            # Purchase Information
            'is_purchase' : CheckboxInput(attrs={'class':'form-check-input', 'style':'margin-left:1%',}),
            # 'purchase_currency' : Select(attrs = {'class':'form-control input-sm','onchange':'select_change()','style':'width: 15%;position: absolute;margin-top: 7px;color: black;background-color: silver;',}, choices = products_constant.Currency ),
            'purchase_price' : TextInput(attrs = {'class':'form-control input-sm','style':'margin-top:4px;', 'onkeyup':'change_PC()','onkeypress':'return restrictAlphabets(event), float_value(event,"id_purchase_price")',}),
            'purchase_tax' : TextInput(attrs = {'class':'form-control input-sm','onkeypress':'return restrictAlphabets(event), float_value(event,"id_purchase_tax")', 'onkeyup':'change_PC()'}),
            'inclusive_purchase_tax' : TextInput(attrs = {'class':'form-control input-sm','onkeypress':'return restrictAlphabets(event)','style':'width: 100%;', }),
            'reverse_charges' : TextInput(attrs = {'class':'form-control input-sm','onkeypress':'return restrictAlphabets(event), float_value(event,"id_reverse_charges")',}),
            'purchase_account' : Select(attrs = {'class':'form-control input-sm',},),

            # 
            'discount' : NumberInput(attrs = {'class':'form-control input-sm',}),
            'abatement' : NumberInput(attrs = {'class':'form-control input-sm',}),    
        }


class EditProductForm(ModelForm):
        
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(EditProductForm, self).__init__(*args, **kwargs)
        
    class Meta:
        model = ProductsModel

        fields = (
            'product_type', 'sku', 'product_name', 'product_description', 
            'purchase_price','selling_price', 'discount', 'tds', 'selling_tax', 'purchase_account',
            'hsn_code', 'abatement', 'unit', 'sales_account', 'inclusive_tax','hidden_img',
            'purchase_tax','inclusive_purchase_tax','reverse_charges','purchase_account','is_sales','is_purchase',
        )

        widgets = {
            'product_type' : Select(attrs = {'class':'form-control input-sm', 'onchange':'show_bundle($(this))'}, choices = products_constant.PRODUCT_TYPE),
            'sku' : TextInput(attrs = {'class':'form-control input-sm',}),
            'product_name' : TextInput(attrs = {'class':'form-control input-sm', 'onfocusout':'check_product_name($(this), true)'}),            
            'hsn_code' : TextInput(attrs = {'class':'form-control input-sm',}),
            'product_description' : Textarea(attrs = {'class':'input-sm','rows':'2', 'style':'width:100%;background-color: #202940;color: white;'}), 
            'tds' : TextInput(attrs = {'class':'form-control input-sm','onkeypress':'return restrictAlphabets(event)',}),      
            'unit' : Select(attrs = {'class':'form-control input-sm',}, choices = products_constant.UNITS), 
            'hidden_img' : TextInput(attrs = {'class':'form-control input-sm',}),     
            
            # Selling Information

            'is_sales' : CheckboxInput(attrs={'class':'form-check-input', 'style':'margin-left:1%',}),
            # 'preferred_currency' : Select(attrs = {'class':'form-control input-sm','onchange':'select_change()','style':'width: 15%;position: absolute;margin-top: 7px;color: black;background-color: silver;',}, choices = products_constant.Currency ),
            'selling_price' : TextInput(attrs = {'class':'form-control input-sm','onkeypress':'return restrictAlphabets(event), float_value(event,"id_selling_price")','onkeyup':'change_SP()','style':'margin-top:4px',}),
            'selling_tax' : TextInput(attrs = {'class':'form-control input-sm','onkeypress':'return restrictAlphabets(event), float_value(event,"id_selling_tax")', 'onkeyup':'change_SP()'}),
            'inclusive_tax' : TextInput(attrs = {'class':'form-control input-sm','onkeypress':'return restrictAlphabets(event)','style':'width: 100%;', }),
            'sales_account' : Select(attrs = {'class':'form-control input-sm',},),

            # Purchase Information
            'is_purchase' : CheckboxInput(attrs={'class':'form-check-input', 'style':'margin-left:1%',}),
            # 'purchase_currency' : Select(attrs = {'class':'form-control input-sm','onchange':'select_change()','style':'width: 15%;position: absolute;margin-top: 7px;color: black;background-color: silver;',}, choices = products_constant.Currency ),
            'purchase_price' : TextInput(attrs = {'class':'form-control input-sm','style':'margin-top:4px;', 'onkeyup':'change_PC()','onkeypress':'return restrictAlphabets(event), float_value(event,"id_purchase_price")',}),
            'purchase_tax' : TextInput(attrs = {'class':'form-control input-sm','onkeypress':'return restrictAlphabets(event), float_value(event,"id_purchase_tax")', 'onkeyup':'change_PC()'}),
            'inclusive_purchase_tax' : TextInput(attrs = {'class':'form-control input-sm','onkeypress':'return restrictAlphabets(event)','style':'width: 100%;', }),
            'reverse_charges' : TextInput(attrs = {'class':'form-control input-sm','onkeypress':'return restrictAlphabets(event), float_value(event,"id_reverse_charges")',}),
            'purchase_account' : Select(attrs = {'class':'form-control input-sm',},),

            # 
            'discount' : NumberInput(attrs = {'class':'form-control input-sm',}),
            'abatement' : NumberInput(attrs = {'class':'form-control input-sm',}),
        }


#==================================================================================
# PRODUCT IMAGE FORM
#==================================================================================
#

class ProductPhotosForm(ModelForm):

    class Meta:
        model = ProductPhotos

        fields= ('product_image',)

        widgets = {
            'product_image' : FileInput(attrs = {'class':'form-control input-sm', 'id':'files','name':'files[]','type':'file', 'accept':'image/jpeg, image/png, image/gif,', })
        }

#==================================================================================
# INVENTORY FORM
#==================================================================================
#

class InventoryForm(ModelForm):

    class Meta:    
        model = Inventory

        fields = ('inventory_name', 'in_date',)

        widgets = {
            'inventory_name' : TextInput(attrs = {'class':'form-control input-sm'}),
            'in_date' : DateInput(attrs={'class':'form-control input-sm', 'type':'date', 'data-toggle':'datepicker'}),
        }

#==================================================================================
# INVENTORY PRODUCT FORM
#==================================================================================
#

class InventoryProductForm(ModelForm):

    def __init__(self, user, inv, *args, **kwargs):
        self.user = user
        super(InventoryProductForm, self).__init__(*args, **kwargs)
        
        # Exclude product, if already assigned to the inventory instance
        #
        products_in_inv = InventoryProduct.objects.filter(inventory_id = inv)
        self.fields['product'].queryset = ProductsModel.objects.filter(user = self.user).exclude(inventoryproduct__in = products_in_inv)
        
    class Meta:
        model = InventoryProduct

        fields = (
            'product', 'quantity', 'unit', 'threshold', 'stop_at_min_hold', 'notify_on_threshold',
            'notify_on_min_hold', 'min_hold_notify_trigger', 'threshold_notify_trigger'
        )
        
        widgets = {
            'product' : Select(attrs = {'class':'form-control input-sm', 'required':'true'}),
            'quantity' : NumberInput(attrs = {'class':'form-control input-sm'}),
            'unit' : Select(attrs = {'class':'form-control input-sm'}, choices = products_constant.UNITS),
            'threshold' : NumberInput(attrs = {'class':'form-control input-sm'}),
            'stop_at_min_hold' : NumberInput(attrs = {'class':'form-control input-sm'}),
            'notify_on_threshold' : Select(attrs = {'class':'form-control input-sm'}, choices = user_constants.IS_TRUE),
            'notify_on_min_hold' : Select(attrs = {'class':'form-control input-sm'}, choices = user_constants.IS_TRUE),
            'threshold_notify_trigger' : Select(attrs = {'class':'form-control input-sm'}, choices = products_constant.PRODUCT_STOCK_NOTIFICATION_TRIGGERS),
            'min_hold_notify_trigger' : Select(attrs = {'class':'form-control input-sm'}, choices = products_constant.PRODUCT_STOCK_NOTIFICATION_TRIGGERS),
        }


#==================================================================================
# INVENTORY PRODUCT FORM
#==================================================================================
#

class InventoryProductEditForm(ModelForm):
    class Meta:
        model = InventoryProduct

        fields = (
            'quantity', 'unit', 'threshold', 'stop_at_min_hold', 'notify_on_threshold',
            'notify_on_min_hold', 'min_hold_notify_trigger', 'threshold_notify_trigger'
        )
        
        widgets = {
            'quantity' : NumberInput(attrs = {'class':'form-control input-sm'}),
            'unit' : Select(attrs = {'class':'form-control input-sm'}, choices = products_constant.UNITS),
            'threshold' : NumberInput(attrs = {'class':'form-control input-sm'}),
            'stop_at_min_hold' : NumberInput(attrs = {'class':'form-control input-sm'}),
            'notify_on_threshold' : Select(attrs = {'class':'form-control input-sm'}, choices = user_constants.IS_TRUE),
            'notify_on_min_hold' : Select(attrs = {'class':'form-control input-sm'}, choices = user_constants.IS_TRUE),
            'threshold_notify_trigger' : Select(attrs = {'class':'form-control input-sm'}, choices = products_constant.PRODUCT_STOCK_NOTIFICATION_TRIGGERS),
            'min_hold_notify_trigger' : Select(attrs = {'class':'form-control input-sm'}, choices = products_constant.PRODUCT_STOCK_NOTIFICATION_TRIGGERS),
        }

#==================================================================================
# BUNDLE EDIT PRODUCT FORM
#==================================================================================
#

class BundleProductForm(ModelForm):

    def __init__(self, user, inv, *args, **kwargs):
        self.user = user
        super(BundleProductForm, self).__init__(*args, **kwargs)
        
        # Exclude product, if already assigned to the bundle instance
        #
        products_in_inv = BundleProducts.objects.filter(product_bundle_id = inv)

        self.fields['product'].queryset = ProductsModel.objects.filter(user = self.user).exclude(pk__in = products_in_inv)
        

    class Meta:
        model = BundleProducts

        fields = ('product','quantity',)

        widgets = {
            'product_type' : Select(attrs = {'class':'form-control input-sm', 'id':'bundle_product_type'}),
            'product' : Select(attrs = {'class':'form-control input-sm'}),
            'quantity' : NumberInput(attrs = {'class':'form-control input-sm',}),
        }