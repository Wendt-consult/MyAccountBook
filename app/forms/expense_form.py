from django import forms
from app.models.expense_model import Expense, ExpenseCategoryLineItem, ExpenseLineItem, PaymentMethod
from app.models.contacts_model import Contacts
from app.models.accounts_model import AccLedger
from app.models.products_model import ProductsModel
from app.other_constants.gst_slab import gst_slab_list
import os.path


class ExpenseForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		user = kwargs.pop('user', None)
		super(ExpenseForm, self).__init__(*args, **kwargs)
		self.fields['vendor'].queryset = Contacts.objects.filter(user=user._wrapped,customer_type__in = [2,4])
		self.fields['payment_method'].queryset = PaymentMethod.objects.filter(user=user._wrapped)

	vendor = forms.ModelChoiceField(queryset=Contacts.objects.none(), widget=forms.Select(attrs={'class':'form-control input-sm col-md-7', 'id':'select_vendor', 'onchange':'state_compare()'}))
	exp_date = forms.DateField(input_formats=['%d/%m/%Y'], widget=forms.DateInput(attrs={'class':'form-control col-md-7 input-sm datepicker1'}, format="%d/%m/%Y"))
	payment_date = forms.DateField(input_formats=['%d/%m/%Y'], widget=forms.DateInput(attrs={'class':'form-control col-md-7 input-sm datepicker2'}, format="%d/%m/%Y"), required=False)
	payment_method = forms.ModelChoiceField(queryset=PaymentMethod.objects.none(), widget=forms.Select(attrs={'class':'form-control col-md-7 input-sm','id':'add_payment_method'}))

	class Meta:
		model = Expense
		fields = ('exp_number','exp_date','exp_sub_total','exp_total','exp_bill','payment_date','payment_method','notes','vendor')
		widgets = {
			'exp_number' : forms.TextInput(attrs={'class':'form-control input-sm expense_num_inp','id':'exp_number','onfocusout':'check_expense_number($(this))'}),
			'exp_sub_total' : forms.NumberInput(attrs={'class':'form-control col-md-7 input-sm expense_sub_total','value':0,'readonly':True}),
			'exp_total' : forms.NumberInput(attrs={'class':'form-control col-md-7 input-sm expense_total','value':0,'readonly':True}),
			'exp_bill' : forms.FileInput(attrs={"onChange":"dragNdrop(event)", "ondragover":"drag()", "ondrop":"drop()", "id":"uploadFile",'accept':'image/jpeg, image/png, image/jpg, application/pdf'}),
			'notes' : forms.Textarea(attrs={'class':'','rows':6, "maxlength":"600"})
		}


class ExpenseCategoryForm(forms.ModelForm):
	def __init__(self, user, *args, **kwargs):
		super(ExpenseCategoryForm, self).__init__(*args, **kwargs)
		self.fields['account'].queryset = AccLedger.objects.filter(major_heads__major_head_name='Expense', user=user._wrapped)

	account = forms.ModelChoiceField(queryset=AccLedger.objects.none(), widget=forms.Select(attrs={'class':'form-control input-sm select_ledger','required': 'true'}))
	class Meta:
		model = ExpenseCategoryLineItem
		fields = ('id','account','category_description','amount','tax','total_amount','reference_id')
		widgets = {
			'category_description' : forms.Textarea(attrs={'class':'form-control input-sm desc','placeholder':'Description (Maximum 300 Charactors)','maxlength':"300"}),
			'amount' : forms.NumberInput(attrs={'class':'form-control input-sm cate_amount','required': 'true','placeholder':'Amount'}),
			'tax' : forms.Select(attrs={'class':'form-control input-sm cate_tax','required':'true'},choices=gst_slab_list),
			'total_amount' : forms.NumberInput(attrs={'class':'form-control input-sm cate_total_amount','required':'true','placeholder':'Total Amount','readonly':True}),
			'reference_id' : forms.HiddenInput(attrs={'value':1}),
		}


class ExpenseItemForm(forms.ModelForm):
	def __init__(self, user, *args, **kwargs):
		super(ExpenseItemForm, self).__init__(*args, **kwargs)
		self.fields['product'].queryset = ProductsModel.objects.filter(user=user._wrapped)

	product = forms.ModelChoiceField(queryset=ProductsModel.objects.none(), widget=forms.Select(attrs={'class':'form-control input-sm select_product','required': 'true'}))
	class Meta:
		model = ExpenseLineItem
		fields = ('id','product','item_description','quantity','rate','amount','tax','total_amount','reference_id')
		widgets = {
			'item_description' : forms.Textarea(attrs={'class':'form-control input-sm','placeholder':'Description (Maximum 300 Charactors)','maxlength':"300"}),
			'quantity' : forms.NumberInput(attrs={'class':'form-control input-sm item_quantity','required': 'true','placeholder':'Quantity'}),
			'rate' : forms.NumberInput(attrs={'class':'form-control input-sm item_rate','required':'true','placeholder':'Rate'}),
			'amount' : forms.NumberInput(attrs={'class':'form-control input-sm item_amount','required':'true','placeholder':'Amount','readonly':True}),
			'tax' : forms.Select(attrs={'class':'form-control input-sm item_tax','required': 'true'},choices=gst_slab_list),
			'total_amount' : forms.NumberInput(attrs={'class':'form-control input-sm item_total_amount','required': 'true','placeholder':'Total Amount','readonly':True}),
			'reference_id' : forms.HiddenInput(attrs={'value':1}),
		}
