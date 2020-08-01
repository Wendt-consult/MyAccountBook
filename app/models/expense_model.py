from django.db import models
from app.models.contacts_model import Contacts
from app.models.accounts_model import AccLedger
from app.models.products_model import ProductsModel
from django.contrib.auth.models import User


class PaymentMethod(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	name = models.CharField(max_length=64)

	def __str__(self):
		return self.name


class Expense(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	exp_number = models.CharField(max_length=24)
	exp_date = models.DateField()
	vendor = models.ForeignKey(Contacts, on_delete=models.CASCADE)
	exp_sub_total = models.DecimalField(max_digits=20, decimal_places=3)
	exp_total = models.DecimalField(max_digits=20, decimal_places=3)
	exp_bill = models.FileField(upload_to='expense_bills/', null=True, blank=True)
	payment_date = models.DateField(null=True, blank=True)
	payment_method = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, null=True, blank=True)
	notes = models.TextField(null=True, blank=True)

	cgst_5 = models.CharField(
        max_length=30,
        db_index = True,
        blank = True,
        null = True,
    )

	igst_5 = models.CharField(
        max_length=30,
        db_index = True,
        blank = True,
        null = True,
    )

	sgst_5 = models.CharField(
        max_length=30,
        db_index = True,
        blank = True,
        null = True,
    )

	cgst_12 = models.CharField(
        max_length=30,
        db_index = True,
        blank = True,
        null = True,
    )

	igst_12 = models.CharField(
        max_length=30,
        db_index = True,
        blank = True,
        null = True,
    )

	sgst_12 = models.CharField(
        max_length=30,
        db_index = True,
        blank = True,
        null = True,
    )

	cgst_18 = models.CharField(
        max_length=30,
        db_index = True,
        blank = True,
        null = True,
    )

	igst_18 = models.CharField(
        max_length=30,
        db_index = True,
        blank = True,
        null = True,
    )

	sgst_18 = models.CharField(
        max_length=30,
        db_index = True,
        blank = True,
        null = True,
    )

	cgst_28 = models.CharField(
        max_length=30,
        db_index = True,
        blank = True,
        null = True,
    )

	igst_28 = models.CharField(
        max_length=30,
        db_index = True,
        blank = True,
        null = True,
    )

	sgst_28 = models.CharField(
        max_length=30,
        db_index = True,
        blank = True,
        null = True,
    )

	def __str__(self):
		return self.exp_number


class ExpenseCategoryLineItem(models.Model):
	expense = models.ForeignKey(Expense, on_delete=models.CASCADE)
	account = models.ForeignKey(AccLedger, on_delete=models.CASCADE)
	category_description = models.TextField(null=True, blank=True)
	amount = models.DecimalField(max_digits=20, decimal_places=3)
	tax = models.IntegerField(null=True, blank=True)
	total_amount = models.DecimalField(max_digits=20, decimal_places=3)
	reference_id = models.PositiveIntegerField(null=True, blank=True)

	def __str__(self):
		return f'Expense {self.expense} - CategoryLineItem({self.id})'


class ExpenseLineItem(models.Model):
	expense_category = models.ForeignKey(ExpenseCategoryLineItem, on_delete=models.CASCADE)
	product = models.ForeignKey(ProductsModel, on_delete=models.SET_NULL, null=True)
	item_description = models.TextField(null=True, blank=True)
	quantity = models.DecimalField(max_digits=10, decimal_places=2)
	rate = models.DecimalField(max_digits=20, decimal_places=3)
	amount = models.DecimalField(max_digits=20, decimal_places=3)
	tax = models.IntegerField()
	total_amount = models.DecimalField(max_digits=20, decimal_places=3)
	reference_id = models.PositiveIntegerField(null=True, blank=True)

	def __str__(self):
		return f'Category {self.expense_category.id} - LineItems({self.id})'