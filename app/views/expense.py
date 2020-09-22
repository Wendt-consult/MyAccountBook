from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.forms import inlineformset_factory
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.template.loader import render_to_string
from collections import OrderedDict, defaultdict
import pdfkit

from app.models.products_model import ProductsModel
from app.forms.products_form import *
from app.forms.contact_forms import *
from app.forms.tax_form import *
from app.forms.inc_fomsets import *
from app.forms.accounts_ledger_forms import *
from app.models.users_model import Organisations, Organisation_Contact
from app.models.customize_model import *
from app.models.accounts_model import *

from app.other_constants import user_constants,country_list

from app.forms.expense_form import ExpenseForm, ExpenseCategoryForm, ExpenseItemForm
from app.models.expense_model import Expense, ExpenseCategoryLineItem, ExpenseLineItem, PaymentMethod

from django.db.models import Q

import datetime
from datetime import datetime,date

@method_decorator(login_required, name='dispatch')
class ExpenseView(View):
	template_name = 'app/app_files/expense/expense.html'
	def get(self, request):
		all_expense = Expense.objects.filter(user=request.user)
		# CUSTOMIZE VIEW CODE
		customize_expense = CustomizeModuleName.objects.filter(Q(user = request.user) & Q(customize_name = 6))
		if(len(customize_expense) != 0):
			view_expense = CustomizeExpenseView.objects.get(customize_view_name = customize_expense[0].id)
			if(view_expense is not None):
				customize = view_expense
			else:
				customize = 'NA'
		else:
				customize = 'NA'

		context = {
			'all_expense' : all_expense,
			'expense_id':'', 
			'breadcrumb_title' : 'EXPENSES',
			'active_link' : 'Expense',
			'customize' : customize,
			'type' : 'view',
			'js_files' : ['custom_files/js/make_payment.js',],
		}

		# for make payment
		context['payment_type'] = payment_constants.PAYMENT_TYPE

        # for make payment account
		major_heads = accounts_model.MajorHeads.objects.get(major_head_name = 'Assets')
		acc_ledger_assets = accounts_model.AccGroups.objects.filter(Q(user = request.user) & Q(major_head = major_heads))
		context['acc_ledger_assets'] = acc_ledger_assets

		return render(request, self.template_name, context)


@method_decorator(login_required, name='dispatch')
class AddExpense(View):
	template_name = 'app/app_files/expense/add_expense.html'
	
	def get(self, request, pk=None, clone=None):
		item_formset_list = []
		edit = False
		total_cate_form = 1
		file = ''
		title = 'Add Expense'
		
		if pk:
			if clone:
				clone = True
				title = 'Make a Copy'
			else:
				clone = False
				title = 'Edit Expense'
			edit = True
			expense = get_object_or_404(Expense, id=pk)
			expense_form = ExpenseForm(instance=expense, user=request.user)
			if expense_form.initial['exp_bill']:
				file = expense_form.initial['exp_bill'].url
			
			ExpenseCategoryFormset = inlineformset_factory(Expense, ExpenseCategoryLineItem, form=ExpenseCategoryForm, extra=0)
			ExpenseItemFormset = inlineformset_factory(ExpenseCategoryLineItem, ExpenseLineItem, form=ExpenseItemForm, extra=0)
			ex_cat_form = ExpenseCategoryFormset(prefix='category', instance=expense, form_kwargs={'user': request.user})
			total_cate_form = len(ex_cat_form)
			
			for index, cate_obj in enumerate(expense.expensecategorylineitem_set.all(), 1):
				item_formset = ExpenseItemFormset(prefix='item'+str(index), instance=cate_obj, form_kwargs={'user': request.user})
				item_formset_list.append(item_formset)

		else:
			clone = False
			ExpenseCategoryFormset = inlineformset_factory(Expense, ExpenseCategoryLineItem, form=ExpenseCategoryForm, extra=1)
			ExpenseItemFormset = inlineformset_factory(ExpenseCategoryLineItem, ExpenseLineItem, form=ExpenseItemForm, extra=1)
			expense_form = ExpenseForm(user=request.user)
			ex_cat_form = ExpenseCategoryFormset(prefix='category', form_kwargs={'user': request.user})

		ex_item_form = ExpenseItemFormset(prefix='item', form_kwargs={'user': request.user})
		
		context = {
			'from_expense' : True,
			
			'add_product_form' : ProductForm(request.user),
			'add_product_images_form' : ProductPhotosForm(),
			
			'contact_form' : ContactsForm(),
			'tax_form' : TaxForm(),
			'other_details_form' : OtherDetailsForm(),
			'social_form' : ContactsExtraForm(),
			'address_formset' : AddressFormset,
			'accounts_formset' : AccountsFormset,

			'ledger_form' : AccLedgerForm(),
			'groups_form' : AccGroupsForm(),

			'product_js_files' : ['custom_files/js/product.js',],
			'contact_js_files' : ['custom_files/js/contacts.js'],
			'ledger_js_files' : ['custom_files/js/ledger.js'],

			'expense_form' : expense_form,
			'ex_cat_form' : ex_cat_form,
			'ex_item_form' : ex_item_form,

			'random_exp_number' : generate_random_exp_num(request.user),
			'edit' : edit,
			'item_formset_list' : item_formset_list,
			'total_cate_form' : total_cate_form,
			'file' : file,
			'clone' : clone,
			'breadcrumb_title' : 'EXPENSES',
			'active_link' : 'Expense',
			'type' : 'add',
			'title' : title,
			'js_files' : ['custom_files/js/add_expense.js', 
                            'custom_files/js/product.js', 
                            'custom_files/js/contacts.js',
                            'custom_files/js/ledger.js',                           
                        ],
			'css_files' : ['custom_files/css/add_expense.css'],
    		'gst_code' : country_list.GST_STATE_CODE,
		}

		context['is_add_clone'] = 'no'
		# org gst number
		if(title == 'Add Expense' or title == 'Make a Copy'):
			context['is_add_clone'] = 'yes'
			context['is_gst'] = 'no'
			context['is_signle_gst'] = 'no'
			context['org_gst_type'] = None
			org = Organisations.objects.get(user = request.user)

			org_gst_num = User_Tax_Details.objects.filter(organisation = org.id,is_active = True)

			context['org_id'] = org.id
			if(len(org_gst_num) == 1):
				context['is_signle_gst'] = 'yes'
				context['is_gst'] = org_gst_num[0].gstin
				context['org_gst_type'] = org_gst_num[0].gst_reg_type
			elif(len(org_gst_num) > 0):
				default = org_gst_num.filter(default_gstin = True,is_active = True)
				if(len(default) != 0):
					context['is_gst'] = default[0].gstin
					context['org_gst_type'] = default[0].gst_reg_type
				else:
					context['is_gst'] = org_gst_num[0].gstin
					context['org_gst_type'] = org_gst_num[0].gst_reg_type
		else:
			context['expense'] = expense

		# for sales account_ledger details
		major_heads = accounts_model.MajorHeads.objects.get(major_head_name = 'Income')
		acc_ledger_income = accounts_model.AccGroups.objects.filter(Q(user = request.user) & Q(major_head = major_heads))
		context['acc_ledger_income'] = acc_ledger_income
		
		# for purchase account_ledger details
		major_heads = accounts_model.MajorHeads.objects.get(major_head_name = 'Expense')
		acc_ledger_expense = accounts_model.AccGroups.objects.filter(Q(user = request.user) & Q(major_head = major_heads))
		context['acc_ledger_expense'] = acc_ledger_expense

		gst = users_model.OrganisationGSTSettings.objects.filter(user = request.user)
		context["gst"] = gst
	
		return render(request, self.template_name, context)

	def post(self, request, pk=None, clone=None):
		if pk:
			ex_item_form = []
			ExpenseCategoryFormset = inlineformset_factory(Expense, ExpenseCategoryLineItem, form=ExpenseCategoryForm, extra=0)
			ExpenseItemFormset = inlineformset_factory(ExpenseCategoryLineItem, ExpenseLineItem, form=ExpenseItemForm, extra=0)

			expense = get_object_or_404(Expense, id=pk)
			if clone:
				expense_form = ExpenseForm(request.POST, request.FILES, user=request.user)
				ex_cat_form = ExpenseCategoryFormset(request.POST, prefix='category', form_kwargs={'user': request.user})
				new_ex_item_form = ExpenseItemFormset(request.POST, prefix='item', form_kwargs={'user': request.user})
				
				for index, cate_obj in enumerate(expense.expensecategorylineitem_set.all(), 1):
					item_formset = ExpenseItemFormset(request.POST, prefix='item'+str(index), form_kwargs={'user': request.user})
					ex_item_form.append(item_formset)

			else:
				expense_form = ExpenseForm(request.POST, request.FILES, instance=expense, user=request.user)
				ex_cat_form = ExpenseCategoryFormset(request.POST, prefix='category', instance=expense, form_kwargs={'user': request.user})
				new_ex_item_form = ExpenseItemFormset(request.POST, prefix='item', form_kwargs={'user': request.user})
				
				for index, cate_obj in enumerate(expense.expensecategorylineitem_set.all(), 1):
					item_formset = ExpenseItemFormset(request.POST, prefix='item'+str(index), instance=cate_obj, form_kwargs={'user': request.user})
					ex_item_form.append(item_formset)
			if expense_form.is_valid() and ex_cat_form.is_valid() and new_ex_item_form.is_valid():
				button = int(request.POST.get('button')) if request.POST.get('button') !='' else 0 
                #button = int(request.POST.get('button'))
				remove_file = request.POST.get('remove_file')
				object_dict = {}

				expense = expense_form.save(commit=False)
				expense.user = request.user
				expense.expense_org_gst_num = request.POST.get('org_gst_number')
				expense.expense_org_gst_type = request.POST.get('org_gst_reg_type')
				expense.expense_org_gst_state = request.POST.get('single_gst_code')

				expense.cgst_5 = request.POST.get('CGST_5')
				expense.sgst_5 = request.POST.get('SGST_5')
				expense.igst_5 = request.POST.get('IGST_5')
				expense.cgst_12 = request.POST.get('CGST_12')
				expense.sgst_12 = request.POST.get('SGST_12')
				expense.igst_12 = request.POST.get('IGST_12')
				expense.cgst_18 = request.POST.get('CGST_18')
				expense.sgst_18 = request.POST.get('SGST_18')
				expense.igst_18 = request.POST.get('IGST_18')
				expense.cgst_28 = request.POST.get('CGST_28')
				expense.sgst_28 = request.POST.get('SGST_28')
				expense.igst_28 = request.POST.get('IGST_28')
				expense.total_balance = expense_form.data["exp_total"]

				#  for payment status
				current_date = date.today()
				due = datetime.strptime(str(expense_form.data["payment_date"]), '%d-%m-%Y').strftime('%Y-%m-%d')
				due = datetime.strptime(due, '%Y-%m-%d').date()
				if(due < current_date):
					delta = (current_date - due).days
					expense.status = 1
					expense.expense_date_count = delta
				else:
					expense.status = 0
				
				if remove_file == 'True':
					expense.exp_bill = ''
				expense.save()
		
				for form in ex_cat_form:
					if form.cleaned_data:
						if form.cleaned_data['DELETE']:
							cate_obj = form.cleaned_data['id']
							cate_obj.delete()
							continue	
						
						ex_cat = form.save(commit=False)
						ex_cat.expense = expense
						ex_cat.save()
						object_dict[ex_cat.reference_id] = ex_cat
				
				for forms in ex_item_form:
					if forms.is_valid():
						for index, form in enumerate(forms):
							if form.cleaned_data['DELETE']:
									item_obj = form.cleaned_data['id']
									item_obj.delete()
									continue
							if form.cleaned_data:
								ex_item = form.save(commit=False)
								ref_id = form.cleaned_data['reference_id']
								ex_cat_obj = object_dict[ref_id]
								ex_item.expense_category = ex_cat_obj
								ex_item.save()

				for form in new_ex_item_form:
					if form.cleaned_data:
						ex_item = form.save(commit=False)
						ref_id = form.cleaned_data['reference_id']
						ex_cat_obj = object_dict[ref_id]
						ex_item.expense_category = ex_cat_obj
						ex_item.save()

				if button == 0:
					return redirect('view_expenses')
				elif button == 1:
					return redirect('add_expense')
				else:
					all_expense = Expense.objects.filter(user=request.user)
					context = {
						'all_expense' : all_expense,
						'expense_id' : expense.id, 
						'breadcrumb_title' : 'EXPENSES',
						'active_link' : 'Expense'
					}
					return render(request, 'app/app_files/expense/expense.html', context)
		else:
			ExpenseCategoryFormset = inlineformset_factory(Expense, ExpenseCategoryLineItem, form=ExpenseCategoryForm, extra=1)
			ExpenseItemFormset = inlineformset_factory(ExpenseCategoryLineItem, ExpenseLineItem, form=ExpenseItemForm, extra=1)
			
			expense_form = ExpenseForm(request.POST, request.FILES, user=request.user)
			ex_cat_form = ExpenseCategoryFormset(request.POST, prefix='category', form_kwargs={'user': request.user})
			ex_item_form = ExpenseItemFormset(request.POST, prefix='item', form_kwargs={'user': request.user})

			if expense_form.is_valid() and ex_cat_form.is_valid() and ex_item_form.is_valid():
				button = int(request.POST.get('button'))
				object_dict = {}
				expense = expense_form.save(commit=False)
				expense.user = request.user
				expense.expense_org_gst_num = request.POST.get('org_gst_number')
				expense.expense_org_gst_type = request.POST.get('org_gst_reg_type')
				expense.expense_org_gst_state = request.POST.get('single_gst_code')
				
				expense.cgst_5 = request.POST.get('CGST_5')
				expense.sgst_5 = request.POST.get('SGST_5')
				expense.igst_5 = request.POST.get('IGST_5')
				expense.cgst_12 = request.POST.get('CGST_12')
				expense.sgst_12 = request.POST.get('SGST_12')
				expense.igst_12 = request.POST.get('IGST_12')
				expense.cgst_18 = request.POST.get('CGST_18')
				expense.sgst_18 = request.POST.get('SGST_18')
				expense.igst_18 = request.POST.get('IGST_18')
				expense.cgst_28 = request.POST.get('CGST_28')
				expense.sgst_28 = request.POST.get('SGST_28')
				expense.igst_28 = request.POST.get('IGST_28')
				expense.total_balance = expense_form.data["exp_total"]

				#  for payment status
				current_date = date.today()
				due = datetime.strptime(str(expense_form.data["payment_date"]), '%d-%m-%Y').strftime('%Y-%m-%d')
				due = datetime.strptime(due, '%Y-%m-%d').date()
				if(due < current_date):
					delta = (current_date - due).days
					expense.status = 1
					expense.expense_date_count = delta
				else:
					expense.status = 0

				expense.save()
				
				for form in ex_cat_form:
					if form.cleaned_data:
						ex_cat = form.save(commit=False)
						ex_cat.expense = expense
						ex_cat.save()
						object_dict[ex_cat.reference_id] = ex_cat
				
				for index, form in enumerate(ex_item_form):
					if form.cleaned_data:
						ex_item = form.save(commit=False)
						ref_id = form.cleaned_data['reference_id']
						ex_cat_obj = object_dict[ref_id]
						ex_item.expense_category = ex_cat_obj
						ex_item.save()

				if button == 0:
					return redirect('view_expenses')
				elif button == 1:
					return redirect(request.path)
				else:
					all_expense = Expense.objects.filter(user=request.user)
					context = {
						'all_expense' : all_expense,
						'expense_id' : expense.id, 
						'breadcrumb_title' : 'EXPENSES',
						'active_link' : 'Expense'
					}
					return render(request, 'app/app_files/expense/expense.html', context)
			else:
				print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
				print(expense_form.errors.as_data())

		return redirect(request.path)


@method_decorator(login_required, name='dispatch')
class DeleteExpense(View):
	def get(self, request, pk):
		expense = get_object_or_404(Expense, id=pk)
		expense.delete()
		return redirect('view_expenses')


@login_required
def generate_pdf_view(request, pk):
	expense = get_object_or_404(Expense, pk=pk)
	html_string = generate_pdf(expense, request)
	pdf_file = pdfkit.from_string(html_string, False)
	return HttpResponse(pdf_file, content_type='application/pdf')


def generate_random_exp_num(user):
	exp_number_list = []
	expense_objects = Expense.objects.filter(user=user, exp_number__icontains='Exp-')
	for obj in expense_objects:
		try:
			number = int(obj.exp_number.replace('Exp-',''))
		except:
			continue
		exp_number_list.append(number)

	if exp_number_list:
		exp_number = max(exp_number_list)
		return 'Exp-' + str(exp_number+1)
	else:
		return 'Exp-1'


def generate_pdf(expense, request):
	exp_category_list = []
	tax_data = {'0':0,'5':0,'12':0,'18':0,'28':0}

	for cate in ExpenseCategoryLineItem.objects.filter(expense=expense):
		exp_category_item_list = []
		each_cate_data = {}
		each_cate_data['account_name'] = cate.account.accounts_name
		each_cate_data['description'] = cate.category_description
		each_cate_data['amount'] = cate.amount
		each_cate_data['tax'] = int(cate.tax) if cate.tax else ''
		each_cate_data['total_amount'] = cate.total_amount
		if cate.tax != None:
			tax_data[str(cate.tax)] += float(cate.amount) * (float(cate.tax)/100)
		else:
			for item in cate.expenselineitem_set.all():
				tax_data[str(item.tax)] += float(item.amount) * (float(item.tax)/100)

		for item in cate.expenselineitem_set.all():
			each_item_data = {}
			each_item_data['product'] = item.product.product_name
			each_item_data['description'] = item.item_description
			each_item_data['quantity'] = item.quantity
			each_item_data['rate'] = item.rate
			each_item_data['amount'] = item.amount
			each_item_data['tax'] = int(item.tax)
			each_item_data['total_amount'] = item.total_amount
			exp_category_item_list.append(each_item_data)

		each_cate_data['item_list'] = exp_category_item_list

		exp_category_list.append(each_cate_data)

	org_object1 = Organisations.objects.filter(user=request.user).first() if Organisations.objects.filter(user=request.user).exists() else None
	org_object2 = Organisation_Contact.objects.filter(organisation=org_object1).first() if Organisation_Contact.objects.filter(organisation=org_object1).exists() else None

	try:
		logo = org_object1.logo.path
	except:
		logo = ""
	

	context = {
		'expense' : expense,
		'exp_category_list' : exp_category_list,
		'org_object1' : org_object1,
		'org_object2' : org_object2,
		'tax_data' : tax_data,
		'logo' : logo,
	}

	html_string = render_to_string('app/app_files/expense/expense_pdf.html', context)
	return html_string


# Ajax View
@login_required
def add_payment_method_view(request):
	name = request.GET.get('name')
	payment_method_object = PaymentMethod.objects.filter(name__iexact=name, user=request.user)
	created = False
	object_id = ''
	if not payment_method_object.exists():
		_object = PaymentMethod.objects.create(name=name, user=request.user)
		object_id = _object.id
		created = True
	return JsonResponse({'created':created,'id':object_id})

@login_required
def check_expense_number_view(request):
	exp_number = request.GET.get('exp_number')
	initial_exp_number = request.GET.get('initial_exp_number')
	expense = Expense.objects.filter(user=request.user, exp_number=exp_number)
	exists = False
	if expense.exists():
		exists = True
	if initial_exp_number and initial_exp_number == exp_number:
		exists = False
	return JsonResponse({'exists':exists})

@login_required
def get_product_details_view(request):
	product_id = request.GET.get('id')
	product = get_object_or_404(ProductsModel, id=product_id)
	data = {
		'product_description' : product.product_description,
		'product_rate' : int(float(product.selling_price)) if product.selling_price else 0,
		'product_tax' : int(float(product.tax)) if product.selling_tax else 0,
		'product_unit' : product.get_unit_display()
	}
	return JsonResponse(data)


#=====================================================================================
#   vendor state address
#=====================================================================================
#
def expenss_vendor_state(request, ins):
    # Initialize 
    data = defaultdict()
    contact = Contacts.objects.get(pk = int(ins))
    gst = User_Tax_Details.objects.get(contact = contact)
    address = users_model.User_Address_Details.objects.filter(Q(contact = contact) & Q(default_address = True))
    # if(contact.email is None):
    #     data['mail'] = 'null'
    # else:
    data['mail'] = contact.email
    data['gst_type'] = gst.gst_reg_type
    if(len(address) == 1):
        if(address[0].state is None):
            data['vendor_state'] = 'null'
        else:
            data['vendor_state'] = address[0].get_state_display()
    elif(len(address) == 0):
        address_first = users_model.User_Address_Details.objects.filter(Q(contact = contact))
        if(len(address_first) == 0 or address_first[0].state == 'None'):
            data['vendor_state'] = 'null'
        else:
            data['vendor_state'] = address_first[0].get_state_display()
        
    return JsonResponse(data)